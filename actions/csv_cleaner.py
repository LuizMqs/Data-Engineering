import pandas as pd
import numpy as np
import random

# suicides_table
data_path = 'database/raw_data/suicidios_2010_a_2019.csv'

df = pd.read_csv(data_path)

# Create a new DataFrame with rows that have null values in 'DTNASC' and 'DTOBITO' columns
removed_rows = df[~df[['DTNASC', 'DTOBITO']].notnull().all(axis=1)]

df.dropna(subset=['DTNASC', 'DTOBITO'], inplace=True)

# Filter dates within valid limits
df = df[(df['DTNASC'] >= '1900-01-01') & (df['DTNASC'] <= '2099-12-31')]

# Calculate age in years and add it to the dataframe
df['age'] = pd.to_datetime(df['DTOBITO']).dt.year - \
    pd.to_datetime(df['DTNASC']).dt.year

# Concatenate the DataFrame with the removed rows back to the original DataFrame
df = pd.concat([df, removed_rows], ignore_index=True)

# Sort the DataFrame by the 'ano' (year) column in ascending order
df.sort_values('ano', inplace=True)

# Reindex the DataFrame consecutively, starting from 1
df.reset_index(drop=True, inplace=True)
df.index = df.index + 1

unnecessary_columns = ['Unnamed: 0', 'DTNASC', 'ASSISTMED', 'ESCMAE',
                       'ESTCIV', 'ESC', 'OCUP', 'CODMUNRES', 'CAUSABAS_O', 'CIRURGIA']
df.drop(columns=unnecessary_columns, inplace=True)


# Counting the existing values in the 'SEXO' column
sexo_counts = df['SEXO'].value_counts()

# Calculating the percentage of each value
percent_male = sexo_counts['Masculino'] / sexo_counts.sum()
percent_female = sexo_counts['Feminino'] / sexo_counts.sum()

# Filling in the null values based on the correct percentage
num_nulls = df['SEXO'].isnull().sum()
num_male = int(num_nulls * percent_male)
num_female = int(num_nulls * percent_female)

# Get the index of the first 17 null values of column 'SEXO'
null_indexes = df[df['SEXO'].isnull()].index[:num_male]

df.loc[null_indexes, 'SEXO'] = 'Masculino'
df.loc[df['SEXO'].isnull(), 'SEXO'] = 'Feminino'

# Counting the existing values in the 'RACACOR' column
racacor_counts = df['RACACOR'].value_counts()

# Calculating the percentage of each value
percent_Branca = racacor_counts['Branca'] / racacor_counts.sum()
percent_Parda = racacor_counts['Parda'] / racacor_counts.sum()
percent_Preta = racacor_counts['Preta'] / racacor_counts.sum()
percent_Indigena = racacor_counts['Indígena'] / racacor_counts.sum()
percent_Amarela = racacor_counts['Amarela'] / racacor_counts.sum()

# Filling in the empty values based on the correct percentage
num_nulls = df['RACACOR'].isnull().sum()
num_Branca = int(num_nulls * percent_Branca)
num_Parda = int(num_nulls * percent_Parda)
num_Preta = int(num_nulls * percent_Preta)
num_Indigena = int(num_nulls * percent_Indigena)
num_Amarela = int(num_nulls * percent_Amarela)

# Obtain the indices of the null values in the 'RACACOR' column
null_indexes = df[df['RACACOR'].isnull()].index.tolist()  # Convert to a list
# Shuffle the null indexes randomly
random.shuffle(null_indexes)

# Replace the null values with the correct values based on percentages
df.loc[null_indexes[:num_Branca], 'RACACOR'] = 'Branca'
df.loc[null_indexes[num_Branca:num_Branca+num_Parda], 'RACACOR'] = 'Parda'
df.loc[null_indexes[num_Branca+num_Parda:num_Branca +
                    num_Parda+num_Preta], 'RACACOR'] = 'Preta'
df.loc[null_indexes[num_Branca+num_Parda+num_Preta:num_Branca +
                    num_Parda+num_Preta+num_Indigena], 'RACACOR'] = 'Indígena'
df.loc[null_indexes[num_Branca+num_Parda+num_Preta+num_Indigena:num_Branca +
                    num_Parda+num_Preta+num_Indigena+num_Amarela], 'RACACOR'] = 'Amarela'
df.dropna(subset=['RACACOR'], inplace=True)

# Fill missing values in the 'age' column with 'N/A'.
df['age'].fillna('N/A', inplace=True)

# Remove rows with missing values in the 'LOCOCOR' column.
df.dropna(subset=['LOCOCOR'], inplace=True)

# Rename columns to match our database
renamed_columns = {
    'estado': 'state',
    'ano': 'year',
    'mes': 'month',
    'DTOBITO': 'date_of_death',
    'SEXO': 'gender',
    'RACACOR': 'race',
    'CAUSABAS': 'death_cause',
    'LOCOCOR': 'place_of_death'
}
df.rename(columns=renamed_columns, inplace=True)

# Check the number of null values in each column
null_counts = df.isnull().sum()
print(null_counts)

# Save the cleaned data to a CSV file
clean_data_path = 'database/table_rows/suicides_table.csv'
df.to_csv(clean_data_path, index=False)

print(f"Cleaned data saved to {clean_data_path}")


# death_causes_table
# Path to the CSV file
data_path = 'database/raw_data/CID-10-SUBCATEGORIAS.csv'

# Decoding the file to ISO-8859-1
df = pd.read_csv(data_path, encoding='ISO-8859-1', sep=';')

# Removing unwanted columns
columns_to_drop = ['CLASSIF', 'RESTRSEXO',
                   'CAUSAOBITO', 'REFER', 'EXCLUIDOS', 'DESCRABREV']
df.drop(columns=columns_to_drop, inplace=True)

# Keep only the first two columns
df = df.iloc[:, :2]

# Rename columns to match our database
renamed_columns = {
    'SUBCAT': 'id',
    'DESCRICAO': 'description',
}
df.rename(columns=renamed_columns, inplace=True)

# Path to the output CSV file
output_path = 'database/table_rows/death_causes_table.csv'

# Saving the DataFrame to a CSV file with UTF-8 encoding
df.to_csv(output_path, encoding='utf-8', index=False, sep=';')

# Check if the file was saved successfully
try:
    pd.read_csv(output_path, sep=";")
    print("CSV file saved successfully.")
except FileNotFoundError:
    print("Error: CSV file was not saved.")


# states_table
data_path = 'database/raw_data/suicidios_por_estados_por_ano.csv'

# Read the CSV file
df = pd.read_csv(data_path)

# Check for null values
if df.isnull().values.any():
    print("Warning: Null values exist in the DataFrame.")

# Remove the first column
df.drop(df.columns[0], axis=1, inplace=True)

# Rename columns to match our database
renamed_columns = {
    'abrev_estado': 'state_abbreviation',
    'estado': 'state',
    'regiao': 'region',
    'ano': 'year',
    'n': 'number_of_deaths',
}
df.rename(columns=renamed_columns, inplace=True)

# Path for the output CSV file
output_path = 'database/table_rows/states_table.csv'

# Save the DataFrame to a clean CSV file
df.to_csv(output_path, index=False)

# Check if the file was successfully saved
try:
    pd.read_csv(output_path)
    print("Cleaned CSV file was saved successfully.")
except FileNotFoundError:
    print("Error: The CSV file was not saved.")


# idh_table
data_path = 'database/raw_data/idh.csv'

# Read the CSV file
df = pd.read_csv(data_path)

# Keep data starting from 2010
df = df[df['ano_referencia'] >= 2010]

# Check if the columns exist before removing them
columns_to_drop = ['expectativa_de_anos_escola',
                   'expectativa_de_anos_escola_feminina', 'expectativa_de_anos_escola_masculina']
existing_columns = df.columns.intersection(columns_to_drop)
df.drop(columns=existing_columns, inplace=True)

# Rename columns to match our database
renamed_columns = {
    'ano_referencia': 'reference_year',
    'idh_feminino': 'female_idh',
    'idh_masculino': 'male_idh',
    'expectativa_de_vida': 'life_expectancy',
    'expectativa_de_vida_feminina': 'female_life_expectancy',
    'expectativa_de_vida_masculina': 'male_life_expectancy',
}
df.rename(columns=renamed_columns, inplace=True)

# Path for the output CSV file
output_path = 'database/table_rows/idh_table.csv'

# Save the DataFrame to a clean CSV file
df.to_csv(output_path, index=False)

# Check if the file was successfully saved
try:
    pd.read_csv(output_path)
    print("Cleaned CSV file was saved successfully.")
except FileNotFoundError:
    print("Error: The CSV file was not saved.")
