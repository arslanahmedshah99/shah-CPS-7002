from dash import html, dcc
import dash_bootstrap_components as dbc

# ---------- SIDEBAR ----------
def sidebar():
    return html.Div(
        [
            html.H4("Menu", className="text-white mb-4"),
            dbc.Nav(
                [
                    dbc.NavLink("Dashboard", href="/dashboard", active="exact"),
                    dbc.NavLink("Users", href="/dashboard/users", active="exact"),
                    dbc.NavLink("Locations", href="/dashboard/locations", active="exact"),
                    dbc.NavLink("Routes", href="/dashboard/routes", active="exact"),
                    dbc.NavLink("Notifications", href="/dashboard/notifications", active="exact"),
                    dbc.NavLink("Campus", href="/dashboard/campus", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        style={
            "backgroundColor": "#198754",
            "padding": "20px",
            "height": "100vh",
        },
    )

# ---------- MAIN DASHBOARD ----------
def dashboard_layout(user):
    return dbc.Container(
        fluid=True,
        children=[

            # URL for internal routing
            dcc.Location(id="dashboard-url"),

            # -------- TOP NAVBAR --------
            dbc.Navbar(
                dbc.Container([
                    dbc.NavbarBrand("Campus Management System", className="fw-bold"),
                    html.Div(
                        f"Logged in as: {user['full_name']}",
                        className="text-white"
                    )
                ]),
                color="success",
                dark=True,
                className="mb-4"
            ),

            # -------- BODY --------
            dbc.Row([

                # Sidebar
                dbc.Col(
                    sidebar(),
                    width=2,
                ),

                # Main Content Area
                dbc.Col(
                    html.Div(
                        id="dashboard-content",
                        children=[
                            dbc.Card(
                                [
                                    dbc.CardHeader("Welcome"),
                                    dbc.CardBody([
                                        html.H5(f"Hello {user['full_name']} 👋"),
                                        html.P("Select an option from the side menu."),
                                        html.Hr(),
                                        html.P(f"Role: {user['role']}"),
                                        html.P(f"Email: {user['email']}"),
                                        html.P(f"Status: {user['status']}"),
                                    ])
                                ],
                                className="shadow"
                            )
                        ],
                    ),
                    width=10,
                ),

            ])
        ]
    )
