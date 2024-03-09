import sqlite3
from sqlite3 import Error

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

# Function to create the transactions table
def create_transactions_table(conn):
    sql_create_transactions_table = """
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time TEXT NOT NULL,
        status TEXT NOT NULL,
        quantity INTEGER NOT NULL
    );
    """

    try:
        cursor = conn.cursor()
        cursor.execute(sql_create_transactions_table)
        print("Transactions table created successfully.")
    except Error as e:
        print(e)

# Function to insert data into the transactions table
def insert_transaction(conn, time, status, quantity):
    sql_insert_transaction = """
    INSERT INTO transactions (time, status, quantity)
    VALUES (?, ?, ?);
    """

    try:
        cursor = conn.cursor()
        cursor.execute(sql_insert_transaction, (time, status, quantity))
        conn.commit()
        print("Data inserted successfully.")
    except Error as e:
        print(e)

# Usage
if __name__ == '__main__':
    # Path to database file
    database_file = './data/Database/transactions.db'

    # Create a connection with the database
    connection = create_connection(database_file)

    # Create the transactions table
    if connection is not None:
        create_transactions_table(connection)

        # Example of inserting data
        insert_transaction(connection, '00h 00', 'approved', 9)
        insert_transaction(connection, '00h 01', 'denied', 8)

    # Close the connection with the database
    if connection is not None:
        connection.close()