import sqlite3
import pandas as pd
import pickle
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# Database path
database_file = './data/Database/transactions.db'

# Table names
table_name_1 = "realtime_trs_1"
table_name_2 = "realtime_trs_2"

# Load machine learning model
with open('./models/IF_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Configuration of server email
email_address = 'pedronatanaelfs@gmail.com'
email_password = 'ceknakxfeioaabjc'

# Alerts Configuration

failed_transactions_limit = 1
failed_transactions_pending_period = 2

reversed_transactions_limit = 6
reversed_transactions_pending_period = 3

# Function to send email
def send_email(subject, message):
    from_email = email_address
    to_email = 'pedronatanaelfs@gmail.com'

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    body = message
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, email_password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

# Function to get data from database
def get_data_from_database(table_name, minutes_ago=1):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=minutes_ago)

    query = f"SELECT * FROM {table_name} WHERE time BETWEEN ? AND ?"
    cursor.execute(query, (start_time, end_time))

    data = cursor.fetchall()

    conn.close()

    return data

# Function to verify alerts
def check_alerts():
    # Failed Alert 1
    data_alert_failed_1 = get_data_from_database(table_name_1, minutes_ago=failed_transactions_pending_period)
    count_failed = sum(1 for _, status, count in data_alert_failed_1 if status == 'failed' and count > failed_transactions_limit)

    if count_failed >= 2:
        #send_email('Failed Alert', 'There were two or more failed cases for 2 consecutive minutes in transactions_1.')
        print('Failed Alert 1')

    # Failed Alert 2
    data_alert_failed_2 = get_data_from_database(table_name_2, minutes_ago=failed_transactions_pending_period)
    count_failed = sum(1 for _, status, count in data_alert_failed_2 if status == 'failed' and count > failed_transactions_limit)

    if count_failed >= 2:
        #send_email('Failed Alert', 'There were two or more failed cases for 2 consecutive minutes in transactions_2.')
        print('Failed Alert 2')

    # Reversed Alert 1
    data_alert_reversed_1 = get_data_from_database(table_name_1, minutes_ago=reversed_transactions_pending_period)
    count_reversed = sum(1 for _, status, count in data_alert_reversed_1 if status == 'reversed' and count > reversed_transactions_limit)

    if count_reversed >= 3:
        #send_email('Reversed Alert', 'There were three or more reversed cases with a count greater than 6 for 3 consecutive minutes in transactions_1.')
        print('Reversed Alert 1')

    # Reversed Alert 2
    data_alert_reversed_2 = get_data_from_database(table_name_2, minutes_ago=reversed_transactions_pending_period)
    count_reversed = sum(1 for _, status, count in data_alert_reversed_2 if status == 'reversed' and count > reversed_transactions_limit)

    if count_reversed >= 3:
        #send_email('Reversed Alert', 'There were three or more reversed cases with a count greater than 6 for 3 consecutive minutes in transactions_2.')
        print('Reversed Alert 2')

# Function to get data from database filtered by status
def get_data_from_database_with_status(table_name, status, minutes_ago=1):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=minutes_ago)

    query = f"SELECT * FROM {table_name} WHERE time BETWEEN ? AND ? AND status = ?"
    cursor.execute(query, (start_time, end_time, status))

    data = cursor.fetchall()

    conn.close()

    return data

# Function to apply the machine learning model in a specific status
def apply_ml_model_with_status(status, minutes_ago=1):
    # Verifying score in transactions_1
    data_from_database_1 = get_data_from_database_with_status(table_name_1, status, minutes_ago)

    if not data_from_database_1:
        data_from_database_1 = [(datetime.now(), status, 0)]  # If no data, use 0 for 'count'

    count_value = data_from_database_1[0][2]  # Get value from column 'count'

    df_input_1 = pd.DataFrame([dict(status_num=2, count=count_value)])
    anomaly_1 = model.predict(df_input_1)

    if anomaly_1 == -1:
        #send_email(f'Denied Alert - {status}', f'The machine learning model identified an anomaly for "{status}" Transactions 1.')
        print('Deinied Alert 1')

    # Verifying score in transactions_2
    data_from_database_2 = get_data_from_database_with_status(table_name_2, status, minutes_ago)

    if not data_from_database_2:
        data_from_database_2 = [(datetime.now(), status, 0)]  # If no data, use 0 for 'count'

    count_value = data_from_database_2[0][2]  # Get value from column 'count'

    df_input_2 = pd.DataFrame([dict(status_num=2, count=count_value)])
    anomaly_2 = model.predict(df_input_2)

    if anomaly_2 == -1:
        #send_email(f'Denied Alert - {status}', f'The machine learning model identified an anomaly for "{status}" Transactions 2.')
        print('Deinied Alert 2')

while True:
    check_alerts()
    apply_ml_model_with_status('denied', minutes_ago=1)
    time.sleep(60)