import psycopg2
import dotenv

DB_NAME = dotenv.get_key('./.env', 'DB_NAME')
DB_USER = dotenv.get_key('./.env', 'DB_USER')
DB_PASS = dotenv.get_key('./.env', 'DB_PASS')
DB_HOST = dotenv.get_key('./.env', 'DB_HOST')
DB_PORT = dotenv.get_key('./.env', 'DB_PORT')

try:
    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)
    print("Database connection successfully")

    cur = conn.cursor()
    
    # Extract data from csv and put it in the database
    with open('./database/table_rows/death_causes_table.csv', 'r', encoding='utf8') as f:
        cur.copy_from(f, 'death_causes', sep=';', columns=('id', 'description'))

    with open('./database/table_rows/suicides_table.csv', 'r', encoding='utf8') as f:
        cur.copy_from(f, 'suicides', sep=',', columns=('state', 'year', 'month', 'date_of_death', 'gender', 'race', 'death_cause', 'place_of_death', 'age'))
    
    print("Data imported successfully")
    

    conn.commit()

except psycopg2.Error as e:
    print("Database connection error:", e)

finally:
    if conn is not None:
        conn.close()
        print("Database connection closed")