import os
import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np


app = Dash(__name__)

app.layout = html.Div(style={'backgroundColor': 'black'}, children = [
     
        html.Div(style={'backgroundColor': 'black'}, children =[

        html.H1(style={'color': 'white'}, children='Transactions Monitoring Dashboard'),

        dcc.Graph(id='approved_graph', style={'position': 'absolute', 'top': '80px', 'left': '10px', 'height': '300px', 'width': '1800px', 'bgcolor': 'black'}),
        dcc.Interval(id="approved", interval=1000),

        dcc.Graph(id='denied_graph', style={'position': 'absolute', 'top': '380px', 'left': '10px', 'height': '300px', 'width': '600px', 'bgcolor': 'black'}),
        dcc.Interval(id="denied", interval=1000),
        
        dcc.Graph(id='failed_graph', style={'position': 'absolute', 'top': '380px', 'left': '610px', 'height': '300px', 'width': '600px', 'bgcolor': 'black'}),
        dcc.Interval(id="failed", interval=1000),
        dcc.Graph(id='reversed_graph', style={'position': 'absolute', 'top': '380px', 'left': '1210px', 'height': '300px', 'width': '600px', 'bgcolor': 'black'}),
        dcc.Interval(id="reversed", interval=1000),

        ])
])


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

    # For tansaction_new_data
    #data = pd.read_csv("./data/Transactions/transactions_new_data.csv")
    #data['time'] = pd.to_datetime(data['time'], format='%Hh %M %Ss')
    #last_two_hours = data[data['time'] >= data['time'].max() - pd.Timedelta(minutes=1)].copy()

    # For existing data
    data = pd.read_csv("./data/Transactions/transactions_2.csv")
    data.rename({'f0_':'count'}, axis = 1, inplace=True)
    today = datetime.now().date()
    yesterday = (datetime.now() - timedelta(days=1)).date()
    data['time'] = pd.to_datetime(today.strftime('%Y-%m-%d') + ' ' + data['time'], format='%Y-%m-%d %Hh %M')
    data['time'] = data['time'].apply(lambda x: x.replace(year=yesterday.year, month=yesterday.month, day=yesterday.day) if x.time() > datetime.now().time() else x)
    last_hours = data[data['time'] >= data['time'].max() - pd.Timedelta(hours=10)].copy()
    last_hours['time'] = last_hours['time'].dt.strftime('%H:%M')

    # Filtrar os dados por status
    approved_data = last_hours[last_hours['status'] == 'approved']
    denied_data = last_hours[last_hours['status'] == 'denied']
    failed_data = last_hours[last_hours['status'] == 'failed']
    reversed_data = last_hours[last_hours['status'] == 'reversed']

    approved_fig = px.line(approved_data, x="time", y="count", labels={"count": "Transactions", "time": "Time"})
    approved_fig.update_xaxes(tickfont=dict(size=8, color='white'), showgrid=False)
    approved_fig.update_yaxes(tickfont=dict(size=8, color='white'), showgrid=False)
    approved_fig.update_traces(fill = 'tozeroy', line=dict(color='green'))
    approved_fig.update_layout(paper_bgcolor='black', xaxis_title_font=dict(color='white'), yaxis_title_font=dict(color='white'), plot_bgcolor="black", xaxis_title_text='', yaxis_title_text='', title_text= "Approved", title_font=dict(color='green'))

    denied_fig = px.line(denied_data, x="time", y="count", labels={"count": "Transactions", "time": "Time"})
    denied_fig.update_xaxes(tickfont=dict(size=8, color='white'), showgrid=False)
    denied_fig.update_yaxes(tickfont=dict(size=8, color='white'), showgrid=False)
    denied_fig.update_traces(fill = 'tozeroy', line=dict(color='orange'))
    denied_fig.update_layout(paper_bgcolor='black', xaxis_title_font=dict(color='white'), yaxis_title_font=dict(color='white'), plot_bgcolor="black", xaxis_title_text='', yaxis_title_text='', title_text= "Denied", title_font=dict(color='orange'))

    failed_fig = px.line(failed_data, x="time", y="count", labels={"count": "Transactions", "time": "Time"})
    failed_fig.update_xaxes(tickfont=dict(size=8, color='white'), showgrid=False)
    failed_fig.update_yaxes(tickfont=dict(size=8, color='white'), showgrid=False)
    failed_fig.update_traces(fill = 'tozeroy', line=dict(color='red'))
    failed_fig.update_layout(paper_bgcolor='black', xaxis_title_font=dict(color='white'), yaxis_title_font=dict(color='white'), plot_bgcolor="black", xaxis_title_text='', yaxis_title_text='', title_text= "Failed", title_font=dict(color='red'))

    reversed_fig = px.line(reversed_data, x="time", y="count", labels={"count": "Transactions", "time": "Time"})
    reversed_fig.update_xaxes(tickfont=dict(size=8, color='white'), showgrid=False)
    reversed_fig.update_yaxes(tickfont=dict(size=8, color='white'), showgrid=False)
    reversed_fig.update_traces(fill = 'tozeroy', line=dict(color='purple'))
    reversed_fig.update_layout(paper_bgcolor='black', xaxis_title_font=dict(color='white'), yaxis_title_font=dict(color='white'), plot_bgcolor="black", xaxis_title_text='', yaxis_title_text='', title_text= "Reversed", title_font=dict(color='purple'))

    return approved_fig, denied_fig, failed_fig, reversed_fig

if __name__ == '__main__':
    app.run(debug=True)