import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Função para executar uma consulta SQL e retornar o resultado em um DataFrame
def execute_sql_query(conn, query):
    try:
        result = pd.read_sql_query(query, conn)
        return result
    except Exception as e:
        print(e)
        return None

# Função para exibir os resultados das consultas
def display_query_results(conn, query, table_name):
    result = execute_sql_query(conn, query)
    if result is not None:
        print(f"Results for {table_name}:")
        print(result)
    else:
        print(f"Error executing query for {table_name}.")

# Usage
if __name__ == '__main__':
    # Path to the new database file
    new_database_file = './data/Database/checkout_data.db'

    # Create a connection with the new database
    new_connection = sqlite3.connect(new_database_file)

    # SQL Query - Anomalies POS 1
    query_pos1 = '''
    WITH AnomalyCTE AS (
      SELECT
        time,
        today as anomalies,
        CASE
          WHEN (today < 0.5 * yesterday) AND
               (today < 0.5 * same_day_last_week) AND
               (today < 0.5 * avg_last_week) AND
               (today < 0.5 * avg_last_month) AND
               (avg_last_month > 1)
          THEN 'Anomaly'
          ELSE 'Normal'
        END AS anomaly_status
      FROM
        checkout_1
    )

    SELECT
      time,
      anomalies,
      anomaly_status
    FROM
      AnomalyCTE
    WHERE
      anomaly_status = 'Anomaly';
    '''

    # SQL Query - Anomalies POS 2
    query_pos2 = '''
    WITH AnomalyCTE AS (
      SELECT
        time,
        today as anomalies,
        CASE
          WHEN (today < 0.5 * yesterday) AND
               (today < 0.5 * same_day_last_week) AND
               (today < 0.5 * avg_last_week) AND
               (today < 0.5 * avg_last_month) AND
               (avg_last_month > 1)
          THEN 'Anomaly'
          ELSE 'Normal'
        END AS anomaly_status
      FROM
        checkout_2
    )

    SELECT
      time,
      anomalies,
      anomaly_status
    FROM
      AnomalyCTE
    WHERE
      anomaly_status = 'Anomaly';

    '''

    # Display results of the queries
    display_query_results(new_connection, query_pos1, 'checkout_1')
    display_query_results(new_connection, query_pos2, 'checkout_2')

    # Close the connection with the new database
    new_connection.close()
