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

    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    cur.execute(""" SELECT death_cause, COUNT(*) AS amount
                    FROM suicides
                    WHERE death_cause >= 'X600' AND death_cause <= 'X849'
                    GROUP BY death_cause
                    ORDER BY amount desc; """)
    
    
    
    rows = cur.fetchall()
    col_names_death_cause = [desc[0] for desc in cur.description]
    df_total_death_cause = pd.DataFrame(rows, columns=col_names_death_cause)
    
    intervals = {
    "X600": ["X600", "X699"],
    "X700": ["X700", "X709"],
    "X710": ["X710", "X719"],
    "X720": ["X720", "X749"],
    "X750": ["X750", "X759"],
    "X760": ["X760", "X769"],
    "X770": ["X770", "X779"],
    "X780": ["X780", "X799"],
    "X800": ["X800", "X819"],
    "X820": ["X820", "X829"],
    "X830": ["X830", "X849"]
    }

    # Create a list to store the data
    data = []

    # Calculate the quantity for each interval
    for interval, codes in intervals.items():
        start_code, end_code = codes
        filtered_data = df_total_death_cause.loc[df_total_death_cause['death_cause'].between(start_code, end_code)]
        quantity = filtered_data['amount'].sum()
        data.append([interval, quantity])

    # Create the new DataFrame
    df_total_death_cause = pd.DataFrame(data, columns=['death_cause', 'quantity'])
    df_total_death_cause= df_total_death_cause.sort_values(by='quantity', ascending=False)
    # Print the new DataFrame
    print(df_total_death_cause)
    
    cur.execute(""" 
                    SELECT id, description
                    FROM death_causes
                    WHERE id >= 'X600' AND id <= 'X849'; """)
    rows = cur.fetchall()
    col_names_death_cause_description = [desc[0] for desc in cur.description]
    df_death_cause_description = pd.DataFrame(rows, columns=col_names_death_cause_description)

    df_death_cause_description_and_amount = pd.merge(df_total_death_cause, df_death_cause_description, left_on='death_cause', right_on='id')

    print(df_death_cause_description_and_amount)

except psycopg2.Error as e:
    print("Database connection error:", e)

finally:
    if conn is not None:
        conn.close()
        print("Database connection closed")
