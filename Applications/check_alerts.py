import sqlite3
from datetime import datetime, timedelta
import random

# Database path
database_file = './data/Database/transactions.db'

# Table names
table_name_1 = "realtime_trs_1"
table_name_2 = "realtime_trs_2"

# Function to insert data into database
def insert_data_into_database(table_name, time, status, count):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    query = f"INSERT INTO {table_name} (time, status, count) VALUES (?, ?, ?)"
    cursor.execute(query, (time, status, count))

    conn.commit()
    conn.close()