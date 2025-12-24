import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output, State

from screens.login import login_layout, login_callback
from screens.dashboard import dashboard_layout

# ---------------- APP ----------------
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.MINTY],
)

# ---------------- LAYOUT ----------------
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    dcc.Store(id="session-user", storage_type="memory"),
    html.Div(id="page-content")
])

# ---------------- ROUTER ----------------
@app.callback(
    Output("page-content", "children"),
    Input("session-user", "data"),     # 🔑 MAIN trigger
    State("url", "pathname")           # 🔑 only state
)
def route_pages(user, pathname):

    # user logged in + dashboard url
    if user is not None and pathname == "/dashboard":
        return dashboard_layout(user)

    # default → login
    return login_layout()

# ---------------- LOGIN CALLBACK ----------------
login_callback(app)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
