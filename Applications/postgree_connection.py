import psycopg2
import csv
from datetime import datetime, date
import time

connection = psycopg2.connect(database = 'grafana',
                              host = 'localhost',
                              user = 'postgres',
                              password = '105916',
                              port = '5432')

# Create cursor to execute SQL commands
cursor = connection.cursor()

# Create Table name
table_name_1 = "realtime_trs_1"
table_name_2 = "realtime_trs_2"

# CSV File Path
csv_file_path_1 = "./data/Transactions/transactions_1.csv"
csv_file_path_2 = "./data/Transactions/transactions_2.csv"

# Create Table 1
cursor.execute("""
    CREATE TABLE IF NOT EXISTS {} (
        time timestamp with time zone,
        status character varying,
        count integer
    )
""".format(table_name_1))

# Create Table 2
cursor.execute("""
    CREATE TABLE IF NOT EXISTS {} (
        time timestamp with time zone,
        status character varying,
        count integer
    )
""".format(table_name_2))

# Commit to save progress
connection.commit()

while True:
    # Get the actual datetime
    current_time = datetime.now().strftime("%Hh %M")
    current_date = date.today()

    # List to keep all rows related to actual time
    rows_to_insert_1 = []
    rows_to_insert_2 = []

    # Open the CSV file 1 to find all the rows that correspond to actual time
    with open(csv_file_path_1, 'r') as file_1:
        reader = csv.reader(file_1)

        # Igonore Header
        next(reader)

        for row in reader:
            if row[0] == current_time:
                # Convert time column format and include current date
                time_str = f"{current_date.year}-{current_date.month:02d}-{current_date.day:02d} {row[0]}"
                time_format = "%Y-%m-%d %Hh %M"
                time_value = datetime.strptime(time_str, time_format)

                # Add the row to list
                rows_to_insert_1.append((time_value, row[1], int(row[2])))

    # Post all the rows in PostgreeSQL
    for row in rows_to_insert_1:
        cursor.execute("""
            INSERT INTO {} (time, status, count)
            VALUES (%s, %s, %s)
        """.format(table_name_1), row)

    # Open the CSV file 2 to find all the rows that correspond to actual time
    with open(csv_file_path_2, 'r') as file_2:
        reader = csv.reader(file_2)

        # Igonore Header
        next(reader)

        for row in reader:
            if row[0] == current_time:
                # Convert time column format and include current date
                time_str = f"{current_date.year}-{current_date.month:02d}-{current_date.day:02d} {row[0]}"
                time_format = "%Y-%m-%d %Hh %M"
                time_value = datetime.strptime(time_str, time_format)

                # Add the row to list
                rows_to_insert_2.append((time_value, row[1], int(row[2])))

    # Post all the rows in PostgreeSQL
    for row in rows_to_insert_2:
        cursor.execute("""
            INSERT INTO {} (time, status, count)
            VALUES (%s, %s, %s)
        """.format(table_name_2), row)

    # Commit to save progress
    connection.commit()

    # Wait 60 seconds before next action
    time.sleep(60)

# Fechar a conexão
cur.close()
conn.close()