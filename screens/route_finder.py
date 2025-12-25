import os
import dash
from dash import html, dcc, Input, Output, State, callback
import pandas as pd
import dash_bootstrap_components as dbc

BLUE = "#0B63C5"
GREEN = "#28a745"
RED = "#dc3545"

ROUTES_CSV = "data/routes.csv"

# ---------------- Load Routes ----------------
def load_routes():
    if os.path.exists(ROUTES_CSV):
        df = pd.read_csv(ROUTES_CSV)

        df["distance_m"] = pd.to_numeric(df["distance_m"], errors="coerce")
        df["accessible"] = df["accessible"].astype(str).str.lower() == "true"

        return df

    return pd.DataFrame(columns=[
        "id", "start_location", "end_location", "distance_m", "accessible"
    ])

# ---------------- Layout ----------------
def layout():
    df = load_routes()
    locations = sorted(
        set(df["start_location"].tolist() + df["end_location"].tolist())
    ) if not df.empty else []

    return dbc.Container([

        html.H3("Route Distance Finder", className="mb-4 text-primary fw-bold"),

        dbc.Card([
            dbc.CardBody([

                dbc.Row([
                    dbc.Col([
                        html.Label("From", className="form-label fw-semibold"),
                        dcc.Dropdown(
                            id="start-location",
                            options=[{"label": l, "value": l} for l in locations],
                            placeholder="Select start location",
                            className="mb-3"
                        )
                    ], md=6),

                    dbc.Col([
                        html.Label("To", className="form-label fw-semibold"),
                        dcc.Dropdown(
                            id="end-location",
                            options=[{"label": l, "value": l} for l in locations],
                            placeholder="Select end location",
                            className="mb-3"
                        )
                    ], md=6),
                ], className="mb-4"),

                dbc.Button(
                    "Find Distance",
                    id="find-btn",
                    color="primary",
                    className="w-100 mb-3 py-2 fw-semibold"
                ),

                html.Div(id="route-result")

            ])
        ], className="shadow")

    ], fluid=True)

# ---------------- Find Route Callback ----------------
def register_find_routes_callbacks(app):
    @app.callback(
        Output("route-result", "children"),
        Input("find-btn", "n_clicks"),
        State("start-location", "value"),
        State("end-location", "value"),
        prevent_initial_call=True
    )
    def find_route(n_clicks, start, end):
        if not start or not end:
            return html.P(
                "Please select both locations",
                className="text-danger fw-bold"
            )

        df = load_routes()

        # Allow both directions and find the shortest route
        route = df[
            ((df["start_location"] == start) & (df["end_location"] == end)) |
            ((df["start_location"] == end) & (df["end_location"] == start))
        ]

        if route.empty:
            return html.P(
                f"No route found between {start} and {end}",
                className="text-danger fw-bold"
            )

        # Find the route with minimum distance
        shortest_route = route.loc[route["distance_m"].idxmin()]

        return dbc.Alert([
            html.H5("Shortest Route Found", className="mb-3"),
            html.P(f"Distance: {shortest_route['distance_m']} meters", className="mb-2 fw-semibold"),
            html.P(
                f"Accessible: {'Yes' if shortest_route['accessible'] else 'No'}",
                style={"color": GREEN if shortest_route["accessible"] else RED, "fontWeight": "500"}
            )
        ], color="success", className="mt-2 shadow-sm")

