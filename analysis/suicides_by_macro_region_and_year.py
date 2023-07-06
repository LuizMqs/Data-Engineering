import psycopg2
import dotenv
import pandas as pd

DB_NAME = dotenv.get_key('.env', 'DB_NAME')
DB_USER = dotenv.get_key('.env', 'DB_USER')
DB_PASS = dotenv.get_key('.env', 'DB_PASS')
DB_HOST = dotenv.get_key('.env', 'DB_HOST')
DB_PORT = dotenv.get_key('.env', 'DB_PORT')

try:
    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)
    print("Database connection successfully")

    cur = conn.cursor()

    cur.execute(""" SELECT region, year, SUM(number_of_deaths::integer) AS total_deaths
                    FROM states
                    GROUP BY region, year
                    ORDER BY year;
                                  """)

    rows = cur.fetchall()

    col_names_suicides_by_macro_regions = [desc[0] for desc in cur.description]
    df_total_suicides_by_macro_regions_and_year = pd.DataFrame(rows, columns=col_names_suicides_by_macro_regions)
    df_total_suicides_by_macro_regions_and_year["region"] = df_total_suicides_by_macro_regions_and_year["region"].replace("Centro Oeste", "Centro-Oeste")
    print(df_total_suicides_by_macro_regions_and_year)

    cur.execute(""" SELECT * 
                    FROM macro_regions_populations""")
    
    rows = cur.fetchall()
    col_names_macro_regions = [desc[0] for desc in cur.description]
    df_total_population_macro_regions = pd.DataFrame(rows, columns=col_names_macro_regions)

    df_total_population_macro_regions["macro_region"] = df_total_population_macro_regions["macro_region"].replace("Centro_O", "Centro-Oeste")
    df_total_population_macro_regions = df_total_population_macro_regions.rename(columns={'macro_region':'region'})

    df_total_population_macro_regions = df_total_population_macro_regions.rename(columns=lambda x: x[-4:] if x.startswith('total_population_') else x)

    print(df_total_population_macro_regions)
 
    df_total_population_macro_regions = df_total_population_macro_regions.melt(id_vars=['region'], var_name='year', value_name='population')
    print(df_total_population_macro_regions)


    df_suicides_by_year_and_macro_regions_formated = pd.merge(df_total_suicides_by_macro_regions_and_year, df_total_population_macro_regions, on=['region', 'year'])

    df_suicides_by_year_and_macro_regions_formated['suicide_rate'] = (df_suicides_by_year_and_macro_regions_formated['total_deaths'] / df_suicides_by_year_and_macro_regions_formated['population']) * 100000

    df_suicides_by_year_and_macro_regions_formated['suicide_rate'] = df_suicides_by_year_and_macro_regions_formated['suicide_rate'].round(2)

    print(df_suicides_by_year_and_macro_regions_formated)


except psycopg2.Error as e:
    print("Database connection error:", e)

finally:
    if conn is not None:
        conn.close()
        print("Database connection closed")
