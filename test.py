import dash
from dash import html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("Multiple Pop-up Links Example"),

    html.P([
        "For more information, ",
        html.A("click here", href="#", id="popup-link-1",
               className="popup-link", **{"data-url": "https://www.google.com/finance/quote/BTC-USD?hl=en&window=5Y"})
    ]),

    html.P([
        "Visit our docs, ",
        html.A("click here", href="#", id="popup-link-2",
               className="popup-link", **{"data-url": "https://www.lequipe.fr"})
    ]),

], fluid=True)

if __name__ == "__main__":
    app.run(debug=True)




dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Details Chart")),
        dbc.ModalBody(dcc.Graph(id="popup-chart")),
    ],
    id="chart-modal",
    size="lg",
    is_open=False,
)



@app.callback(
    Output("chart-modal", "is_open"),
    Output("popup-chart", "figure"),
    Input("my-table", "active_cell"),
    State("chart-modal", "is_open"),
    prevent_initial_call=True
)
def display_chart(active_cell, is_open):
    if active_cell:
        row = active_cell["row"]
        col = active_cell["column_id"]
        # Check if this column is one of the "special" ones
        if col in ["column_with_chart"]:
            # Build a custom figure based on that row
            fig = px.line(data_for_row(row))
            return True, fig
    return False, dash.no_update