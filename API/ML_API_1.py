import pickle
import uvicorn
import pandas as pd
from fastapi import FastAPI
import psycopg2
from datetime import datetime, timedelta

def get_current_time():
    current_datetime = datetime.now() - timedelta(minutes=1)
    current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:00-03")
    return current_datetime

def get_display_time():
    display_time = datetime.now() - timedelta(minutes=1)
    display_time = display_time.strftime("%H:%M")
    return display_time

# Function to get data from PostgreSQL
def get_data_from_postgres():
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(
        database='grafana',
        host='localhost',
        user='postgres',
        password='105916',
        port='5432'
    )

    # Create a cursor object to execute queries
    cursor = connection.cursor()

    # Query to retrieve data from the specified table
    query = f"SELECT time, status, count FROM realtime_trs_1 WHERE status = 'denied' AND time = '{get_current_time()}'"

    # Execute the query
    cursor.execute(query)

    # Fetch the result
    result = cursor.fetchone()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    return result

# Starts the API
app = FastAPI()

# Load model
with open('../models/IF_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Create start page
@app.get('/')
def home():
    return 'Welcome to denied anomaly detection API!'

# Detect anomaly using data from PostgreSQL
@app.get('/predict')
def predict():
    # Get data from PostgreSQL
    data_from_postgres = get_data_from_postgres()

    # Check if data is available
    if data_from_postgres:
        # Create DataFrame from the retrieved data
        df_input = pd.DataFrame([dict(status_num=2, count=data_from_postgres[2])])

        # Predict using the loaded model
        anomaly = model.predict(df_input)
        anomaly_scores = model.decision_function(df_input)

        if int(anomaly[0]) == 1:
            anomaly_status = "Normal"
        else: anomaly_status = "Anomaly Detected"

        return {f"time": get_display_time(),
                f"Anomaly Score": float(anomaly_scores[0]),
                f"Anomaly status": anomaly_status}

    return {f"time": get_display_time(),
            f"Anomaly Score": float(0),
            f"Anomaly status": "Normal"}

# Execute API
if __name__ == '__main__':
    uvicorn.run(app)