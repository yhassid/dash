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