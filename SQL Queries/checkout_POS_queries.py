import sqlite3
import pandas as pd

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

    # SQL Query - POS 1
    query_pos1 = '''
    SELECT *
    FROM checkout_1
    WHERE
        (today < 0.5 * yesterday) AND
        ((today > 1.5 * avg_last_week) OR (today < 0.5 * avg_last_week)) AND
        ((today > 1.5 * avg_last_month) OR (today < 0.5 * avg_last_month)) OR
        ((today = 0) AND (yesterday != 0) AND (avg_last_week != 0) AND (avg_last_month != 0));
    '''

    # SQL Query - POS 2
    query_pos2 = '''
    SELECT *
    FROM checkout_2
    WHERE
        (today < 0.5 * yesterday) AND
        ((today > 2 * avg_last_week) OR (today < 0.5 * avg_last_week)) AND
        ((today > 2 * avg_last_month) OR (today < 0.5 * avg_last_month)) OR
        ((today = 0) AND (yesterday != 0) AND (avg_last_week != 0) AND (avg_last_month != 0));
    '''

    # Display results of the queries
    display_query_results(new_connection, query_pos1, 'checkout_1')
    display_query_results(new_connection, query_pos2, 'checkout_2')

    # Close the connection with the new database
    new_connection.close()
