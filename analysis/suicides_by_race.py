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

    cur.execute(""" SELECT year, race
                    FROM suicides
                                    """)

    rows = cur.fetchall()
    
    col_names_suicides_by_race = [desc[0] for desc in cur.description]

    df_total_suicides_by_race_and_year = pd.DataFrame(rows, columns=col_names_suicides_by_race)
    print(df_total_suicides_by_race_and_year)

    df_number_of_suicides_by_race = df_total_suicides_by_race_and_year["race"].value_counts()

    df_number_of_suicides_by_race = pd.DataFrame({'race': df_number_of_suicides_by_race.index, 'amount_of_ suicides': df_number_of_suicides_by_race.values})
    print(df_number_of_suicides_by_race)

    df_number_of_suicides_by_race_between_2016_and_2019 = df_total_suicides_by_race_and_year.groupby(['year', 'race']).size().unstack().reset_index()

    print(df_number_of_suicides_by_race_between_2016_and_2019)

except psycopg2.Error as e:
    print("Database connection error:", e)

finally:
    if conn is not None:
        conn.close()
        print("Database connection closed")
