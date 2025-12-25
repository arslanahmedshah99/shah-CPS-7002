import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import html, dcc
import dash_bootstrap_components as dbc
import random
import numpy as np

# Load locations data
def load_locations():
    df = pd.read_csv("data/locations.csv")
    return df

def reports_layout():
    df = load_locations()

    # Generate dummy visit data for demonstration
    df['visits'] = [random.randint(10, 100) for _ in range(len(df))]

    # Pie Chart: Percentage of visits by building
    building_visits = df.groupby('building')['visits'].sum().reset_index()
    pie_fig = px.pie(building_visits, values='visits', names='building', title='Visits by Building')

    # Bar Chart: Compare visits per location (top 10)
    top_locations = df.nlargest(10, 'visits')
    bar_fig = px.bar(top_locations, x='name', y='visits', title='Top 10 Locations by Visits')

    # Line Chart: Trends over time (dummy hourly data)
    hours = list(range(24))
    visits_over_time = [random.randint(50, 200) for _ in hours]
    line_fig = go.Figure()
    line_fig.add_trace(go.Scatter(x=hours, y=visits_over_time, mode='lines+markers', name='Visits'))
    line_fig.update_layout(title='Visits Over Time (Hourly)', xaxis_title='Hour', yaxis_title='Visits')

    # Heatmap: Route usage (dummy grid)
    heatmap_data = np.random.rand(10, 10) * 100
    heatmap_fig = go.Figure(data=go.Heatmap(z=heatmap_data, colorscale='Viridis'))
    heatmap_fig.update_layout(title='Route Usage Heatmap')

    # Scatter Plot: User activity vs time
    scatter_x = [random.randint(0, 23) for _ in range(100)]
    scatter_y = [random.randint(0, 100) for _ in range(100)]
    scatter_fig = px.scatter(x=scatter_x, y=scatter_y, title='User Activity vs Time')

    # Histogram: Distribution of visits
    hist_fig = px.histogram(df, x='visits', title='Distribution of Visits per Location')

    return dbc.Container(fluid=True, children=[
        html.H3("Reports & Analytics", className="mb-4 text-primary fw-bold"),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Visits by Building"),
                    dbc.CardBody(dcc.Graph(figure=pie_fig))
                ], className="mb-4")
            ], md=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Top Locations by Visits"),
                    dbc.CardBody(dcc.Graph(figure=bar_fig))
                ], className="mb-4")
            ], md=6)
        ]),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Visits Over Time"),
                    dbc.CardBody(dcc.Graph(figure=line_fig))
                ], className="mb-4")
            ], md=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Route Usage Heatmap"),
                    dbc.CardBody(dcc.Graph(figure=heatmap_fig))
                ], className="mb-4")
            ], md=6)
        ]),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("User Activity Scatter Plot"),
                    dbc.CardBody(dcc.Graph(figure=scatter_fig))
                ], className="mb-4")
            ], md=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Visits Distribution"),
                    dbc.CardBody(dcc.Graph(figure=hist_fig))
                ], className="mb-4")
            ], md=6)
        ])
    ])

def register_reports_callbacks(app):
    # No dynamic callbacks needed for now
    pass