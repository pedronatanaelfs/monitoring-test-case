import sqlite3

def fetch_all_data_from_table(db_file, table_name):
    try:
        # Conectar ao banco de dados
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()

        # Consulta SQL para buscar todos os dados da tabela
        query = f"SELECT * FROM {table_name};"

        # Executar a consulta
        cursor.execute(query)

        # Buscar todos os dados
        data = cursor.fetchall()

        # Fechar a conexão com o banco de dados
        connection.close()

        return data

    except sqlite3.Error as e:
        print(f"Erro ao buscar dados da tabela {table_name}: {e}")
        return None

# Caminho para o arquivo do banco de dados SQLite
db_file_path = '../data/Database/transactions.db'

# Nome da tabela a ser consultada
table_to_query = 'realtime_trs_1'

# Chamar a função para buscar todos os dados da tabela
result = fetch_all_data_from_table(db_file_path, table_to_query)

# Exibir os resultados, se houverem
if result:
    for row in result:
        print(row)
else:
    print("Nenhum dado encontrado ou erro na consulta.")
