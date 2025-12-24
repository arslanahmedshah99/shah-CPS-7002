import csv
from dash import html, no_update
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

def read_users():
    users = []
    with open("data/users.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            users.append(row)
    return users

def login_layout():
    return dbc.Container(
        dbc.Row(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Login", className="text-center fw-bold"),
                    dbc.CardBody([
                        dbc.Input(id="username", placeholder="Username", className="mb-2"),
                        dbc.Input(id="password", placeholder="Password", type="password", className="mb-2"),
                        dbc.Button("Login", id="login-btn", color="success", className="w-100"),
                        html.Div(id="login-msg", className="text-danger mt-2 text-center")
                    ])
                ], className="shadow"),
                width=4
            ),
            justify="center",
            className="vh-100 align-items-center"
        ),
        fluid=True
    )

def login_callback(app):
    @app.callback(
        Output("session-user", "data"),
        Output("url", "pathname"),
        Output("login-msg", "children"),
        Input("login-btn", "n_clicks"),
        State("username", "value"),
        State("password", "value"),
        prevent_initial_call=True  # ⭐ MOST IMPORTANT
    )
    def login(n, username, password):

        # button not clicked yet
        if n is None:
            return no_update, no_update, ""

        if not username or not password:
            return no_update, no_update, "Please enter username and password"

        for user in read_users():
            if user["username"] == username:

                if user["password"] != password:
                    return no_update, no_update, "Incorrect password"

                if user["status"] != "active":
                    return no_update, no_update, "Account is not active"

                # ✅ SUCCESS
                return user, "/dashboard", ""

        return no_update, no_update, "User not found"