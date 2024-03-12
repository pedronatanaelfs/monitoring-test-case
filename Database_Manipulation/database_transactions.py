import sqlite3
import csv
from datetime import datetime, date
import time

# Caminho para o arquivo do banco de dados SQLite
database_file = './data/Database/transactions.db'

# Conectar ao banco de dados SQLite
connection = sqlite3.connect(database_file)

# Criar um cursor para executar comandos SQL
cursor = connection.cursor()

# Nome das tabelas
table_name_1 = "realtime_trs_1"
table_name_2 = "realtime_trs_2"

# Caminhos dos arquivos CSV
csv_file_path_1 = "./data/Transactions/transactions_1.csv"
csv_file_path_2 = "./data/Transactions/transactions_2.csv"

# Criar Tabela 1
cursor.execute("""
    CREATE TABLE IF NOT EXISTS {} (
        time timestamp,
        status text,
        count integer
    )
""".format(table_name_1))

# Criar Tabela 2
cursor.execute("""
    CREATE TABLE IF NOT EXISTS {} (
        time timestamp,
        status text,
        count integer
    )
""".format(table_name_2))

# Confirmar para salvar o progresso
connection.commit()

while True:
    # Obter a data e hora atual
    current_time = datetime.now().strftime("%Hh %M")
    current_date = date.today()

    # Lista para armazenar todas as linhas relacionadas à hora atual
    rows_to_insert_1 = []
    rows_to_insert_2 = []

    # Abrir o arquivo CSV 1 para encontrar todas as linhas que correspondem à hora atual
    with open(csv_file_path_1, 'r') as file_1:
        reader = csv.reader(file_1)

        # Ignorar cabeçalho
        next(reader)

        for row in reader:
            if row[0] == current_time:
                # Converter o formato da coluna de tempo e incluir a data atual
                time_str = f"{current_date.year}-{current_date.month:02d}-{current_date.day:02d} {row[0]}"
                time_format = "%Y-%m-%d %Hh %M"
                time_value = datetime.strptime(time_str, time_format)

                # Adicionar a linha à lista
                rows_to_insert_1.append((time_value, row[1], int(row[2])))

    # Inserir todas as linhas no SQLite
    for row in rows_to_insert_1:
        cursor.execute("""
            INSERT INTO {} (time, status, count)
            VALUES (?, ?, ?)
        """.format(table_name_1), row)

    # Abrir o arquivo CSV 2 para encontrar todas as linhas que correspondem à hora atual
    with open(csv_file_path_2, 'r') as file_2:
        reader = csv.reader(file_2)

        # Ignorar cabeçalho
        next(reader)

        for row in reader:
            if row[0] == current_time:
                # Converter o formato da coluna de tempo e incluir a data atual
                time_str = f"{current_date.year}-{current_date.month:02d}-{current_date.day:02d} {row[0]}"
                time_format = "%Y-%m-%d %Hh %M"
                time_value = datetime.strptime(time_str, time_format)

                # Adicionar a linha à lista
                rows_to_insert_2.append((time_value, row[1], int(row[2])))

    # Inserir todas as linhas no SQLite
    for row in rows_to_insert_2:
        cursor.execute("""
            INSERT INTO {} (time, status, count)
            VALUES (?, ?, ?)
        """.format(table_name_2), row)

    # Confirmar para salvar o progresso
    connection.commit()

    # Aguardar 60 segundos antes da próxima ação
    time.sleep(60)

# Fechar a conexão
cursor.close()
connection.close()