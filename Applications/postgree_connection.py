import psycopg2
import csv
from datetime import datetime, date
import time

connection = psycopg2.connect(database = 'grafana',
                              host = 'localhost',
                              user = 'postgres',
                              password = '105916',
                              port = '5432')

# Criar um cursor para executar comandos SQL
cursor = connection.cursor()

# Nome da tabela no PostgreSQL
table_name = "realtime_trs_1"

# Caminho para o arquivo CSV
csv_file_path = "./data/Transactions/transactions_1.csv"

# Criar a tabela se não existir
cursor.execute("""
    CREATE TABLE IF NOT EXISTS {} (
        time timestamp without time zone,
        status character varying,
        count integer
    )
""".format(table_name))

# Commit para garantir que as alterações são salvas
connection.commit()

while True:
    # Obter o horário atual e a data atual
    current_time = datetime.now().strftime("%Hh %M")
    current_date = date.today()

    # Lista para armazenar todas as linhas correspondentes ao horário atual
    rows_to_insert = []

    # Abrir o arquivo CSV e procurar todas as linhas correspondentes ao horário atual
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)

        # Pular o cabeçalho
        next(reader)

        for row in reader:
            if row[0] == current_time:
                # Converter o formato da coluna time incluindo a data atual
                time_str = f"{current_date.year}-{current_date.month:02d}-{current_date.day:02d} {row[0]}"
                time_format = "%Y-%m-%d %Hh %M"
                time_value = datetime.strptime(time_str, time_format)

                # Adicionar a linha à lista
                rows_to_insert.append((time_value, row[1], int(row[2])))

    # Inserir todas as linhas no PostgreSQL
    for row in rows_to_insert:
        cursor.execute("""
            INSERT INTO {} (time, status, count)
            VALUES (%s, %s, %s)
        """.format(table_name), row)

    # Commit para salvar as alterações no banco de dados
    connection.commit()

    # Aguardar 60 segundos antes de verificar novamente
    time.sleep(60)

# Fechar a conexão
cur.close()
conn.close()