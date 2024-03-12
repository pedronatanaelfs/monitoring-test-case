# Real-Time Monitoring System with Alerts

## Overview

This project is a real-time monitoring system equipped with two distinct alert mechanisms. The first set of alerts is based on simple rules, while the second employs a machine learning algorithm to detect anomalies. The implementation offers flexibility by supporting two different approaches: one using PostgreSQL as a database integrated with Grafana, and the other utilizing Python and its libraries with SQLite as the database.

## Features

- **Rule-based Alerts (Grafana):** Basic rules for alerting configured directly within Grafana.
- **Machine Learning Alerts (API):** Anomaly detection through a machine learning algorithm with alerts integrated into Grafana using an API.
- **Real-Time Dashboard:** Monitors and displays data in real-time on a dashboard.

## Setup and Usage

### PostgreSQL and Grafana Setup

1. Create a conda environment:

   ```bash
   conda create -n monitoring_env python=3.8
   
2. Activate the environment:
   
   ```bash
   conda activate monitoring_env

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   
4. Run PostgreeSQL connection:

   ```bash
   python Applications/postgree_connection.py

5. Run machine learning APIs:

   ```bash
   python API/ML_API_1.py
   python API/ML_API_1.py

6. Open Grafana and integrate the database and API as in the presentation

### Python and Dash Setup

1. Follow steps 1-3 above.

2. Run database transactions:

   ```bash
   python Database_Manipulation/database_transactions.py

3. Run Dash-based monitoring dashboards:

   ```bash
   python Applications/dash_monitoring_1.py
   python Applications/dash_monitoring_2.py

4. Run Python-based alerts:

   ```bash
   python Applications/alerts_monitoring.py
   
5. View dashboards in your browser in the adress given by the terminal

6. Customize alert configurations in Applications/alerts_monitoring.py

7. Optionally, change the input data in Database_Manipulation/database_transactions.py to test alerts with a different dataset.

### Additional Notes

- To receive email alerts, uncomment the relevant lines in Applications/alerts_monitoring.py.
- Adjust alert limits and pending periods in the same file.

Feel free to explore, customize, and contribute to this real-time monitoring system!
