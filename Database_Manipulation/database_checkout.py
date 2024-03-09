import sqlite3
from sqlite3 import Error
import pandas as pd

# Function to create a connection with the database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connection established with {sqlite3.version}")
        return conn
    except Error as e:
        print(e)
    return conn

# Function to create a checkout table
def create_checkout_table(conn, table_name):
    sql_create_checkout_table = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        time TEXT PRIMARY KEY,
        today INTEGER NOT NULL,
        yesterday INTEGER NOT NULL,
        same_day_last_week INTEGER NOT NULL,
        avg_last_week REAL NOT NULL,
        avg_last_month REAL NOT NULL
    );
    """

    try:
        cursor = conn.cursor()
        cursor.execute(sql_create_checkout_table)
        print(f"{table_name} table created successfully.")
    except Error as e:
        print(e)

# Function to insert data into a checkout table
def insert_checkout_data(conn, table_name, data_path):
    try:
        # Read CSV data into a DataFrame
        df = pd.read_csv(data_path)

        # Insert data into the checkout table
        df.to_sql(table_name, conn, index=False, if_exists='replace')
        print(f"Data inserted into {table_name} successfully.")
    except Error as e:
        print(e)

# Usage
if __name__ == '__main__':
    # Path to the new database file
    new_database_file = './data/Database/checkout_data.db'

    # Create a connection with the new database
    new_connection = create_connection(new_database_file)

    # Create checkout tables and insert data
    if new_connection is not None:
        create_checkout_table(new_connection, 'checkout_1')
        insert_checkout_data(new_connection, 'checkout_1', './data/POS/checkout_1.csv')

        create_checkout_table(new_connection, 'checkout_2')
        insert_checkout_data(new_connection, 'checkout_2', './data/POS/checkout_2.csv')

    # Close the connection with the new database
    if new_connection is not None:
        new_connection.close()
