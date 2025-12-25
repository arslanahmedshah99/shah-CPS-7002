import csv
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State


def read_users():
    with open("data/users.csv", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def login_layout():
    return dbc.Container(
        dbc.Row(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Login", className="text-center fw-bold fs-4 py-3"),
                    dbc.CardBody([
                        dbc.Input(id="username", placeholder="Username", className="mb-3 form-control-lg"),
                        dbc.Input(id="password", placeholder="Password", type="password", className="mb-4 form-control-lg"),
                        dbc.Button("Login", id="login-btn", color="success", className="w-100 py-2 fw-semibold fs-5"),
                        html.Div(id="login-msg", className="text-danger mt-3 text-center fw-semibold")
                    ], className="px-4 py-3")
                ], className="shadow-lg border-0"),
                width=4
            ),
            justify="center",
            align="center",
            className="vh-100"
        ),
        fluid=True,
        className="bg-light"
    )


def login_callback(app):

    @app.callback(
        Output("session-user", "data"),
        Output("login-msg", "children"),
        Input("login-btn", "n_clicks"),
        State("username", "value"),
        State("password", "value"),
        prevent_initial_call=True
    )
    def login(n, username, password):

        if not username or not password:
            return None, "Enter username & password"

        for user in read_users():
            if user["username"] == username and user["password"] == password:
                if user["status"] != "active":
                    return None, "Account inactive"

                return {
                    "username": user["username"],
                    "full_name": user["full_name"],
                    "email": user["email"],
                    "role": user["role"],
                    "status": user["status"],
                }, ""

        return None, "Invalid username or password"
