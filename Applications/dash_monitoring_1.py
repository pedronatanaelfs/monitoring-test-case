import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import sqlite3
from sqlite3 import Error
from dash.exceptions import PreventUpdate


app = Dash(__name__)

app.layout = html.Div(style={'backgroundColor': 'black'}, children=[

    html.Div(style={'backgroundColor': 'black'}, children=[

        html.H1(style={'color': 'white'}, children='Transactions Monitoring Dashboard - Transactons 1'),

        dcc.Graph(id='approved_graph', style={'position': 'absolute', 'top': '80px', 'left': '10px', 'height': '300px',
                                              'width': '1800px', 'bgcolor': 'black'}),
        dcc.Interval(id="approved", interval=5000),

        dcc.Graph(id='denied_graph', style={'position': 'absolute', 'top': '380px', 'left': '10px', 'height': '300px',
                                            'width': '600px', 'bgcolor': 'black'}),
        dcc.Interval(id="denied", interval=5000),

        dcc.Graph(id='failed_graph', style={'position': 'absolute', 'top': '380px', 'left': '610px', 'height': '300px',
                                            'width': '600px', 'bgcolor': 'black'}),
        dcc.Interval(id="failed", interval=5000),
        dcc.Graph(id='reversed_graph', style={'position': 'absolute', 'top': '380px', 'left': '1210px', 'height': '300px',
                                               'width': '600px', 'bgcolor': 'black'}),
        dcc.Interval(id="reversed", interval=5000),

    ])
    
])

# Function to create a connection with the database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connection established with {sqlite3.version}")
        return conn
    except Error as e:
        print(e)
    return conn

# Function to execute a query and fetch data from the database
def fetch_data_from_db(conn, query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        return data
    except Error as e:
        print(e)
        return None

# Callback to update figures
@app.callback(
        
    [Output("approved_graph", "figure"),
    Output("denied_graph", "figure"),
    Output("failed_graph", "figure"),
    Output("reversed_graph", "figure")],

    [Input("approved", "n_intervals"),
    Input("denied", "n_intervals"),
    Input("failed", "n_intervals"),
    Input("reversed", "n_intervals")],

    )

def update_figures(n_intervals_approved, n_intervals_denied, n_intervals_failed, n_intervals_reversed):

    # Path to the SQLite database file
    database_file = './data/Database/transactions.db'

    # Name of the table to query
    table_name = 'realtime_trs_1'

    # Create a connection with the database
    connection = create_connection(database_file)

    if connection is not None:
        try:
            # Build the query to fetch data from the database
            query = f"SELECT time, status, count FROM {table_name} WHERE time >= datetime('now', '-10 hours');"

            # Fetch data from the database
            data = fetch_data_from_db(connection, query)

            if data:
                # Create a DataFrame from the fetched data
                df = pd.DataFrame(data, columns=['time', 'status', 'count'])

                # Filter data by status
                approved_data = df[df['status'] == 'approved']
                denied_data = df[df['status'] == 'denied']
                failed_data = df[df['status'] == 'failed']
                reversed_data = df[df['status'] == 'reversed']

                approved_fig = px.line(approved_data, x="time", y="count",
                                       labels={"count": "Transactions", "time": "Time"})
                approved_fig.update_xaxes(tickfont=dict(size=8, color='white'), showgrid=False)
                approved_fig.update_yaxes(tickfont=dict(size=8, color='white'), showgrid=False)
                approved_fig.update_traces(fill='tozeroy', line=dict(color='green'))
                approved_fig.update_layout(paper_bgcolor='black', xaxis_title_font=dict(color='white'),
                                           yaxis_title_font=dict(color='white'), plot_bgcolor="black",
                                           xaxis_title_text='', yaxis_title_text='',
                                           title_text="Approved", title_font=dict(color='green'))

                denied_fig = px.line(denied_data, x="time", y="count",
                                     labels={"count": "Transactions", "time": "Time"})
                denied_fig.update_xaxes(tickfont=dict(size=8, color='white'), showgrid=False)
                denied_fig.update_yaxes(tickfont=dict(size=8, color='white'), showgrid=False)
                denied_fig.update_traces(fill='tozeroy', line=dict(color='orange'))
                denied_fig.update_layout(paper_bgcolor='black', xaxis_title_font=dict(color='white'),
                                         yaxis_title_font=dict(color='white'), plot_bgcolor="black",
                                         xaxis_title_text='', yaxis_title_text='',
                                         title_text="Denied", title_font=dict(color='orange'))

                failed_fig = px.line(failed_data, x="time", y="count",
                                     labels={"count": "Transactions", "time": "Time"})
                failed_fig.update_xaxes(tickfont=dict(size=8, color='white'), showgrid=False)
                failed_fig.update_yaxes(tickfont=dict(size=8, color='white'), showgrid=False)
                failed_fig.update_traces(fill='tozeroy', line=dict(color='red'))
                failed_fig.update_layout(paper_bgcolor='black', xaxis_title_font=dict(color='white'),
                                         yaxis_title_font=dict(color='white'), plot_bgcolor="black",
                                         xaxis_title_text='', yaxis_title_text='',
                                         title_text="Failed", title_font=dict(color='red'))

                reversed_fig = px.line(reversed_data, x="time", y="count",
                                       labels={"count": "Transactions", "time": "Time"})
                reversed_fig.update_xaxes(tickfont=dict(size=8, color='white'), showgrid=False)
                reversed_fig.update_yaxes(tickfont=dict(size=8, color='white'), showgrid=False)
                reversed_fig.update_traces(fill='tozeroy', line=dict(color='purple'))
                reversed_fig.update_layout(paper_bgcolor='black', xaxis_title_font=dict(color='white'),
                                           yaxis_title_font=dict(color='white'), plot_bgcolor="black",
                                           xaxis_title_text='', yaxis_title_text='',
                                           title_text="Reversed", title_font=dict(color='purple'))

                return approved_fig, denied_fig, failed_fig, reversed_fig

        except Exception as e:
            print(e)

        finally:
            # Close the connection with the database
            connection.close()

    return PreventUpdate, PreventUpdate, PreventUpdate, PreventUpdate

if __name__ == '__main__':
    app.run(debug=True)