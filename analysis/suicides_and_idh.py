import psycopg2
import dotenv
import pandas as pd

DB_NAME = dotenv.get_key('.env', 'DB_NAME')
DB_USER = dotenv.get_key('.env', 'DB_USER')
DB_PASS = dotenv.get_key('.env', 'DB_PASS')
DB_HOST = dotenv.get_key('.env', 'DB_HOST')
DB_PORT = dotenv.get_key('.env', 'DB_PORT')

import psycopg2

try:
    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)
    print("Database connection successfully")

    cur = conn.cursor()

    cur.execute(""" SELECT year, COUNT(*) AS amount
                    FROM suicides
                    GROUP BY year
                    ORDER BY year ASC """)

    rows = cur.fetchall()
    col_names_suicides_by_year = [desc[0] for desc in cur.description]
    df_total_suicides_by_year = pd.DataFrame(rows, columns=col_names_suicides_by_year)
    df_total_suicides_by_year.rename(columns={'amount': 'amount_of_suicides'}, inplace=True)

    cur.execute(""" SELECT * 
                    FROM macro_regions_populations""")
    
    rows = cur.fetchall()
    col_names_macro_regions = [desc[0] for desc in cur.description]
    df_total_population_macro_regions = pd.DataFrame(rows, columns=col_names_macro_regions)

    df_total_population_macro_regions["macro_region"] = df_total_population_macro_regions["macro_region"].replace("Centro_O", "Centro-Oeste")

    populacao_total_por_coluna = df_total_population_macro_regions.iloc[:, 1:].sum()
    df_populacao_total = populacao_total_por_coluna.to_frame(name='amount_total')
    df_populacao_total.reset_index(inplace=True)
    df_populacao_total.columns = ['year', 'total_population']
    df_populacao_total['year'] = df_populacao_total['year'].replace(to_replace='total_population_', value='', regex=True).astype(int)

    df_populacao_total['year'] = df_populacao_total['year'] .astype(str)
    df_total_suicides_by_year['year'] = df_total_suicides_by_year['year'].astype(str)

    df_merge_pop_total_suicides_total = pd.merge(df_populacao_total, df_total_suicides_by_year, on='year')

    df_merge_pop_total_suicides_total['suicide_rate'] = (df_merge_pop_total_suicides_total['amount_of_suicides'] / df_merge_pop_total_suicides_total['total_population']) * 100000


    print(df_merge_pop_total_suicides_total)

    cur.execute(""" SELECT reference_year,idh 
                    FROM idh
                            """)
    
    rows = cur.fetchall()
    col_names_idh = [desc[0] for desc in cur.description]
    df_idh = pd.DataFrame(rows, columns=col_names_idh)
    df_idh['reference_year'] = df_idh['reference_year'].astype(str)

    df_idh.rename(columns={'reference_year': 'year'}, inplace=True)

    df_idh_and_suicide_rate = pd.merge(df_merge_pop_total_suicides_total, df_idh, on='year')

    print(df_idh_and_suicide_rate)
  

except psycopg2.Error as e:
    print("Database connection error:", e)

finally:
    if conn is not None:
        conn.close()
        print("Database connection closed")