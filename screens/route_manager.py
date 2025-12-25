import os
import dash
import pandas as pd
from dash import html, dcc, Input, Output, State, callback
from dash.dependencies import ALL
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

CSV_PATH = "data/routes.csv"
NOTIF_CSV_PATH = "data/notification.csv"
BLUE = "#2f80ed"

os.makedirs("data", exist_ok=True)

# ---------------- CSV Read / Write ----------------
def read_routes():
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        df["accessible"] = df["accessible"].apply(lambda x: True if str(x).lower() == "true" else False)
        return df
    return pd.DataFrame(columns=["id", "start_location", "end_location", "distance_m", "accessible"])

def save_routes(df):
    df.to_csv(CSV_PATH, index=False)

def add_notification(message, user_id=1):
    if os.path.exists(NOTIF_CSV_PATH):
        df = pd.read_csv(NOTIF_CSV_PATH)
    else:
        df = pd.DataFrame(columns=["id","user_id","message","delivered"])
    new_id = int(df.id.max()) + 1 if not df.empty else 1
    df = pd.concat([df, pd.DataFrame([{"id": new_id, "user_id": user_id, "message": message, "delivered": False}])], ignore_index=True)
    df.to_csv(NOTIF_CSV_PATH, index=False)

# ---------------- Table ----------------
def generate_table(df):
    if df.empty:
        return dbc.Alert("No routes found", color="warning")
    header = html.Tr([html.Th(c) for c in ["ID","Start","End","Distance","Accessible","Actions"]])
    rows = []
    for _, r in df.iterrows():
        rows.append(html.Tr([
            html.Td(r.id),
            html.Td(r.start_location),
            html.Td(r.end_location),
            html.Td(r.distance_m),
            html.Td("Yes" if r.accessible else "No", style={"color": BLUE if r.accessible else "red", "fontWeight":"bold"}),
            html.Td([
                dbc.Button("Edit", id={"type":"edit","index":r.id}, className="btn-edit me-1", size="sm"),
                dbc.Button("Delete", id={"type":"delete","index":r.id}, className="btn-delete", size="sm")
            ])
        ]))
    return dbc.Table([header]+rows, bordered=True, hover=True, striped=True, responsive=True, className="shadow-sm")

# ---------------- Layout ----------------
def routes_layout():
    df = read_routes()
    return dbc.Container([
        html.H3("Routes Management", className="mb-4 text-primary fw-bold"),
        dbc.Card([
            dbc.CardBody([
                html.H4("Add or Edit Route Information", className="mb-3 text-secondary"),
                dcc.Store(id="edit-id", data=None),
                dbc.Row([
                    dbc.Col(dcc.Input(id="start", placeholder="Start location", className="form-control"), md=3),
                    dbc.Col(dcc.Input(id="end", placeholder="End location", className="form-control"), md=3),
                    dbc.Col(dcc.Input(id="distance", type="number", placeholder="Distance (m)", className="form-control"), md=3),
                    dbc.Col(dcc.Dropdown(id="accessible", options=[{"label":"Accessible","value":True},{"label":"Not Accessible","value":False}], placeholder="Accessible"), md=3)
                ], className="mb-3"),
                dbc.Row([
                    dbc.Col(dbc.Button("Add", id="add-btn", color="primary", className="me-2"), width="auto"),
                    dbc.Col(dbc.Button("Reset", id="reset-btn", color="secondary"), width="auto")
                ], className="justify-content-end")
            ])
        ], className="mb-4 shadow-sm"),
        dbc.Card([
            html.Div(id="table", children=generate_table(df))
        ])
    ], fluid=True)

# ---------------- REGISTER CALLBACKS ----------------
def register_routes_callbacks(app):

    # ---------------- Add / Update / Reset ----------------
    @app.callback(
        Output("table","children", allow_duplicate=True),
        Output("start","value"),
        Output("end","value"),
        Output("distance","value"),
        Output("accessible","value"),
        Output("add-btn","children"),
        Output("edit-id","data"),
        Input("add-btn","n_clicks"),
        Input("reset-btn","n_clicks"),
        State("start","value"),
        State("end","value"),
        State("distance","value"),
        State("accessible","value"),
        State("edit-id","data"),
        prevent_initial_call=True
    )
    def add_update_reset(add_click, reset_click, s, e, d, a, edit_id):
        ctx = dash.callback_context
        trigger = ctx.triggered[0]["prop_id"]

        df = read_routes()

        # Reset
        if trigger == "reset-btn.n_clicks":
            return generate_table(df), "", "", None, None, "Add", None

        # Add / Update
        if not all([s,e]) or d is None or a is None:
            raise PreventUpdate

        if edit_id is not None:
            df.loc[df.id == edit_id, ["start_location","end_location","distance_m","accessible"]] = [s,e,d,a]
            add_notification(f"Route '{s} → {e}' updated")
        else:
            new_id = int(df.id.max())+1 if not df.empty else 1
            df = pd.concat([df, pd.DataFrame([{"id":new_id,"start_location":s,"end_location":e,"distance_m":d,"accessible":a}])], ignore_index=True)
            add_notification(f"New route '{s} → {e}' added")

        save_routes(df)
        return generate_table(df), "", "", None, None, "Add", None

    # ---------------- Edit ----------------
    @app.callback(
        Output("start","value", allow_duplicate=True),
        Output("end","value", allow_duplicate=True),
        Output("distance","value", allow_duplicate=True),
        Output("accessible","value", allow_duplicate=True),
        Output("add-btn","children", allow_duplicate=True),
        Output("edit-id","data", allow_duplicate=True),
        Input({"type":"edit","index":ALL},"n_clicks"),
        prevent_initial_call=True
    )
    def edit_route(clicks):
        if not any(clicks):
            raise PreventUpdate
        route_id = dash.callback_context.triggered_id["index"]
        df = read_routes()
        r = df[df.id==route_id].iloc[0]
        return r.start_location, r.end_location, r.distance_m, r.accessible, "Update", route_id

    # ---------------- Delete ----------------
    @app.callback(
        Output("table","children", allow_duplicate=True),
        Input({"type":"delete","index":ALL},"n_clicks"),
        prevent_initial_call=True
    )
    def delete_route(clicks):
        if not any(clicks):
            raise PreventUpdate
        route_id = dash.callback_context.triggered_id["index"]
        df = read_routes()
        df = df[df.id != route_id]
        save_routes(df)
        add_notification(f"Route {route_id} deleted")
        return generate_table(df)
