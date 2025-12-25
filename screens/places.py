import os
import pandas as pd
import dash
from dash import html, dcc, Input, Output, State
from dash.dependencies import ALL
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

# ------------------ Config ------------------
CSV_PATH = "data/locations.csv"
os.makedirs("data", exist_ok=True)

# ------------------ CSV Read / Write ------------------
def read_locations():
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)

        # FIX boolean from CSV
        df["accessible"] = df["accessible"].apply(
            lambda x: True if str(x).lower() == "true" else False
        )

        return df

    return pd.DataFrame(columns=["id", "name", "building", "floor", "accessible"])


def save_locations(df):
    df.to_csv(CSV_PATH, index=False)

# ------------------ Table ------------------
def generate_locations_table(df):
    if df.empty:
        return dbc.Alert("No locations found", color="warning")

    header = html.Tr([
        html.Th("ID"),
        html.Th("Name"),
        html.Th("Building"),
        html.Th("Floor"),
        html.Th("Accessible"),
        html.Th("Actions"),
    ])

    rows = []
    for _, row in df.iterrows():
        rows.append(
            html.Tr([
                html.Td(row.id),
                html.Td(row.name),
                html.Td(row.building),
                html.Td(row.floor),
                html.Td("Yes" if row.accessible else "No"),
                html.Td([
                    dbc.Button(
                        "Edit",
                        id={"type": "edit-loc", "index": row.id},
                        size="sm",
                        className="btn-edit me-1"
                    ),
                    dbc.Button(
                        "Delete",
                        id={"type": "delete-loc", "index": row.id},
                        size="sm",
                        className="btn-delete"
                    )
                ])
            ])
        )

    return dbc.Table(
        [header] + rows,
        bordered=True,
        hover=True,
        striped=True,
        responsive=True,
        className="shadow-sm"
    )

# ------------------ Layout ------------------
def locations_layout():
    df = read_locations()

    return dbc.Container(fluid=True, children=[

        html.H3("Locations Management", className="mb-4 text-primary fw-bold"),

        dbc.Card(className="mb-4 shadow-sm", children=[
            dbc.CardBody([
                html.H4("Add or Edit Location Details", className="mb-3 text-secondary"),
                dcc.Store(id="edit-loc-id"),

                dbc.Row([
                    dbc.Col(dcc.Input(
                        id="loc-name",
                        placeholder="Name",
                        className="form-control"
                    ), md=3),

                    dbc.Col(dcc.Input(
                        id="loc-building",
                        placeholder="Building",
                        className="form-control"
                    ), md=3),

                    dbc.Col(dcc.Input(
                        id="loc-floor",
                        placeholder="Floor",
                        className="form-control"
                    ), md=3),

                    dbc.Col(dcc.Dropdown(
                        id="loc-accessible",
                        options=[
                            {"label": "Accessible", "value": True},
                            {"label": "Not Accessible", "value": False},
                        ],
                        placeholder="Accessible"
                    ), md=3),
                ], className="mb-3"),

                dbc.Row(className="justify-content-end", children=[
                    dbc.Col(
                        dbc.Button("Add", id="add-loc-btn", color="primary", className="me-2"),
                        width="auto"
                    ),
                    dbc.Col(
                        dbc.Button("Reset", id="reset-loc-btn", color="secondary"),
                        width="auto"
                    ),
                ])
            ])
        ]),

        dbc.Card(className="p-3 shadow-sm", children=[
            html.Div(id="table-loc", children=generate_locations_table(df))
        ])

    ])

# ======================================================
# REGISTER CALLBACKS (REGISTER ONCE IN main.py)
# ======================================================
def register_locations_callbacks(app):

    # ------------------ DELETE ------------------
    @app.callback(
        Output("table-loc", "children", allow_duplicate=True),
        Input({"type": "delete-loc", "index": ALL}, "n_clicks"),
        prevent_initial_call=True
    )
    def delete_location(clicks):
        if not any(clicks):
            raise PreventUpdate

        ctx = dash.callback_context
        loc_id = ctx.triggered_id["index"]

        df = read_locations()
        df = df[df.id != loc_id]
        save_locations(df)

        return generate_locations_table(df)

    # ------------------ EDIT + RESET (SINGLE CALLBACK) ------------------
    @app.callback(
        Output("loc-name", "value"),
        Output("loc-building", "value"),
        Output("loc-floor", "value"),
        Output("loc-accessible", "value"),
        Output("add-loc-btn", "children"),
        Output("edit-loc-id", "data"),
        Input({"type": "edit-loc", "index": ALL}, "n_clicks"),
        Input("reset-loc-btn", "n_clicks"),
        prevent_initial_call=True
    )
    def handle_edit_reset(edit_clicks, reset_click):
        ctx = dash.callback_context

        if not ctx.triggered:
            raise PreventUpdate

        trigger = ctx.triggered[0]["prop_id"]

        # -------- RESET --------
        if trigger == "reset-loc-btn.n_clicks":
            return "", "", "", None, "Add", None

        # -------- EDIT --------
        loc_id = ctx.triggered_id["index"]
        df = read_locations()
        row = df[df.id == loc_id].iloc[0]

        return (
            row.name,
            row.building,
            row.floor,
            row.accessible,
            "Update",
            loc_id
        )

    # ------------------ ADD / UPDATE ------------------
    @app.callback(
        Output("table-loc", "children", allow_duplicate=True),
        Input("add-loc-btn", "n_clicks"),
        State("loc-name", "value"),
        State("loc-building", "value"),
        State("loc-floor", "value"),
        State("loc-accessible", "value"),
        State("edit-loc-id", "data"),
        prevent_initial_call=True
    )
    def save_location(_, name, building, floor, accessible, edit_id):
        if not name or not building or not floor or accessible is None:
            raise PreventUpdate

        df = read_locations()

        if edit_id is not None:
            df.loc[df.id == edit_id, ["name", "building", "floor", "accessible"]] = [
                name, building, floor, accessible
            ]
        else:
            new_id = int(df.id.max()) + 1 if not df.empty else 1
            df = pd.concat([
                df,
                pd.DataFrame([{
                    "id": new_id,
                    "name": name,
                    "building": building,
                    "floor": floor,
                    "accessible": accessible
                }])
            ], ignore_index=True)

        save_locations(df)
        return generate_locations_table(df)
