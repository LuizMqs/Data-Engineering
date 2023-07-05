import psycopg2
import dotenv

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
    
    # Extract data from csv and put it in the database
    with open('database/table_rows/death_causes_table.csv', 'r', encoding='utf8') as f:
        next(f)
        cur.copy_from(f, 'death_causes', sep=';', columns=('id', 'description'))

    with open('database/table_rows/suicides_table.csv', 'r', encoding='utf8') as f:
        next(f)
        cur.copy_from(f, 'suicides', sep=',', columns=('state', 'year', 'month', 'date_of_death', 'gender', 'race', 'death_cause', 'place_of_death', 'age'))
    
    with open('database/raw_data/total_population_of_macro_regions_projection.csv', 'r', encoding='utf8') as f:
        next(f)
        cur.copy_from(f, 'macro_regions_populations', sep=',', columns=('macro_region', 'total_population_2010', 'total_population_2011', 'total_population_2012', 'total_population_2013', 'total_population_2014', 'total_population_2015', 'total_population_2016', 'total_population_2017', 'total_population_2018', 'total_population_2019', 'total_population_2020', 'total_population_2021', 'total_population_2022'))

    with open('database/table_rows/idh_table.csv', 'r', encoding='utf8') as f:
        next(f)
        cur.copy_from(f, 'idh', sep=',', columns=('reference_year', 'idh', 'female_idh', 'male_idh', 'life_expectancy', 'female_life_expectancy', 'male_life_expectancy'))

    with open('database/table_rows/states_table.csv', 'r', encoding='utf8') as f:
        next(f)
        cur.copy_from(f, 'states', sep=',', columns=('state_abbreviation', 'state', 'region', 'year', 'number_of_deaths'))

    print("Data imported successfully")
    

    conn.commit()

except psycopg2.Error as e:
    print("Database connection error:", e)

finally:
    if conn is not None:
        conn.close()
        print("Database connection closed")