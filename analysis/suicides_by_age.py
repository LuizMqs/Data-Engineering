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

    cur.execute(""" SELECT gender, age, death_cause
                    FROM suicides
                    WHERE death_cause >= 'X600' AND death_cause <= 'X849'
                    ORDER BY age DESC;""")
    
    rows = cur.fetchall()
    col_names_age = [desc[0] for desc in cur.description]
    df_total_population_age = pd.DataFrame(rows, columns=col_names_age)

    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    labels = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91-100']
    labels = [str(label) for label in labels]
    
    df_total_population_age['age'] = pd.to_numeric(df_total_population_age['age'], errors='coerce')

   
    df_total_population_age.dropna(subset=['age'], inplace=True)

    df_total_population_age['age_group'] = pd.cut(df_total_population_age['age'], bins=bins, labels=labels)

    age_counts = df_total_population_age['age_group'].value_counts() 

    gender_counts = df_total_population_age.groupby(['age_group', 'gender']).size().unstack()
    
    print(gender_counts)

    print(age_counts)
    
except psycopg2.Error as e:
    print("Database connection error:", e)

finally:
    if conn is not None:
        conn.close()
        print("Database connection closed")
