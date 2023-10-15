import pandas as pd
import sqlite3

# Define the CSV file and SQLite database names
csv_file = 'csv_flles\Meteorite_Landings.csv'
db_file = 'meteorite_landings.db'

# Create a connection to the SQLite database
conn = sqlite3.connect(db_file)

# Create a cursor to execute SQL commands
cur = conn.cursor()

# Define the SQL table name and columns
table_name = 'my_table'
# You should customize the column names and data types according to your CSV file
create_table_query = f'''
    CREATE TABLE IF NOT EXISTS {table_name} (
        column1 INTEGER,
        column2 TEXT,
        column3 REAL
    )
'''
cur.execute(create_table_query)

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv(csv_file)

# Insert the data from the DataFrame into the SQLite database
df.to_sql(table_name, conn, if_exists='replace', index=False)

# Commit the changes and close the database connection
conn.commit()
conn.close()

print(f"Data from {csv_file} has been imported into {table_name} table in {db_file}.")
