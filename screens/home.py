from dash import html
import dash_bootstrap_components as dbc

def sidebar(user):
    user_role = user.get('role', 'student') if user else 'student'
    
    # Base menu items for all users
    menu_items = [
        dbc.Button(
            "Dashboard",
            id="btn-dashboard",
            color="light",
            className="w-100 mb-3",
            style={"textAlign": "left"}
        ),
        dbc.Button("Find Routes", id="btn-find-routes", color="light", className="w-100 mb-3", style={"textAlign": "left"}),
        dbc.Button("Notifications", id="btn-notifications", color="light", className="w-100 mb-3", style={"textAlign": "left"}),
    ]
    
    # Admin menu items - shown to all but disabled for non-admins
    admin_items = [
        dbc.Button(
            "Users",
            id="btn-users", 
            color="light" if user_role == 'admin' else "secondary",
            className="w-100 mb-3",
            style={"textAlign": "left"},
            disabled=(user_role != 'admin')
        ),
        dbc.Button(
            "Locations", 
            id="btn-locations", 
            color="light" if user_role == 'admin' else "secondary",
            className="w-100 mb-3", 
            style={"textAlign": "left"},
            disabled=(user_role != 'admin')
        ),
        dbc.Button(
            "Routes", 
            id="btn-routes", 
            color="light" if user_role == 'admin' else "secondary",
            className="w-100 mb-3", 
            style={"textAlign": "left"},
            disabled=(user_role != 'admin')
        ),
        dbc.Button(
            "Reports", 
            id="btn-reports", 
            color="light" if user_role == 'admin' else "secondary",
            className="w-100 mb-3", 
            style={"textAlign": "left"},
            disabled=(user_role != 'admin')
        ),
    ]
    
    menu_items.extend(admin_items)
    
    return html.Div([
        html.H4("Menu", className="text-white mb-4"),
        html.Div(menu_items)
    ], style={
        "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "padding": "20px",
        "height": "100vh",
        "borderRadius": "0 15px 15px 0"
    })

def dashboard_layout(user, content=None):
    if content is None:
        content = html.Div([
            html.H3(f"Welcome {user.get('username', 'User')}!"),
            html.P("This is your dashboard home page.", className="text-muted"),
        ])
    
    return dbc.Container([
        dbc.Navbar(
            dbc.Container([
                html.Div([
                    html.Span("Dashboard", style={"fontSize": "24px", "fontWeight": "bold", "color": "#2c3e50"})
                ]),
                html.Div([
                    html.Span(f"Hello, {user.get('username', 'User')}", className="me-3 text-dark fw-semibold"),
                    dbc.Button("Logout", id="logout-btn", color="danger", size="sm", className="px-3")
                ])
            ], className="d-flex justify-content-between w-100"),
            color="white",
            dark=False,
            className="mb-4 shadow-sm"
        ),

        dbc.Row([
            dbc.Col(sidebar(user), width=2),
            dbc.Col(
                html.Div(content, style={"padding": "20px"}), 
                width=10
            )
        ])
    ], fluid=True)

# No callbacks - all in app.py
def dashboard_callbacks(app):
    pass