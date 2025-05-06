import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table, Input, Output, State
import pandas as pd
from datetime import datetime
import plotly.express as px
import random
from apscheduler.schedulers.background import BackgroundScheduler


# Global variable to store data
latest_data = {'df': None, 'timestamp': None, 'year': None}


def get_latest_data():
    global latest_data
    now = datetime.now()
    minutes = now.minute
    #number = random.randint(0, 1)
    year = 2007 if minutes % 2 == 0 else 1952
    print(f"get latest data at {now} - {year}")

    df = px.data.gapminder().query(f"year == {year}")
    latest_data['df'] = df
    latest_data['timestamp'] = now
    latest_data['year'] = year
    #latest_data = {'df': df, 'timestamp': now, 'year': year}
    return

def schedule_calculate():
    # Start scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(get_latest_data, trigger='interval', seconds=30, max_instances=1, coalesce=True)
    scheduler.start()

    # Run once at startup
    get_latest_data()

schedule_calculate()

# Sample data
#df = px.data.gapminder().query("year == 2007")

# Init app
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP,
    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css"],
    url_base_pathname='/my_app/',
)

def get_login_layout(hide):
    layout = dbc.Container([
        # Top Row with two logos
        dbc.Row([
            # dbc.Col(
            #     html.Img(
            #         src="assets/bnp_logo.jpg",
            #         style={
            #             "width": "100%",  # Stretch to fill left half
            #             "height": "80px",  # Limit vertical height
            #             "object-fit": "contain"  # Scale proportionally
            #         }
            #     ),
            #     width=5
            # ),
            dbc.Col(
                html.Div([
                    html.Img(src="assets/bnp_logo.jpg", style={
                        "display": "block",
                        "width": "auto",
                        "height": "80px",
                        "object-fit": "contain"
                    }),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Span("Powered by", className="credit-prefix"),
                                html.Span("\u00A0"),
                                html.Span("eFX Derivatives team", className="credit-main"),
                                html.Span("  🚀", className="credit-icon"),
                            ], className="credit-line"),
                            html.Div("Part of eFic group", className="credit-sub credit-line")
                        ], className="d-flex flex-column")
                    ], className="credit-text ms-2")
                ], className="d-flex align-items-center", style={"gap": "20px"}),
                width=4,
                className="d-flex align-items-center justify-content-start p-1 m-1"
            )
        ], className="mb-3 mt-2", justify="between", align="center"),

        # Centered middle logo and title
        dbc.Row([
            dbc.Col([
                html.Img(src='assets/hedging_cartoon.png',
                         style={"width": "500px", "height": "auto", "display": "block", "margin": "0 auto"}),
                html.Br(),
                html.H3("Welcome to the Portal", className="text-center mt-2"),
                html.Br(),
            ])
        ], className="mb-4"),

        # Login form
        dbc.Row([
            dbc.Col([
                dbc.Input(id="login-username", placeholder="Username", type="text", className="mb-2"),
                dbc.Input(id="login-password", placeholder="Password", type="password", className="mb-2"),
                dbc.Button("Login", id="login-button", color="primary", className="mb-2", n_clicks=0),
                dbc.Alert("Invalid username or password.", id="login-alert", color="danger", is_open=False),
                html.Div(
                    dbc.Button("Forgot password?", id="forgot-link", color="link", className="mt-2", n_clicks=0),
                    className="text-center"
                ),
                # Modal for password help
                dbc.Modal([
                    dbc.ModalHeader("Reset Your Password"),
                    dbc.ModalBody(
                        "Please contact the system administrator at support@example.com to reset your password."),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="close-modal", className="ml-auto", n_clicks=0)
                    )
                ], id="forgot-modal", is_open=False),
            ], width=6)
        ], justify="center")
    ], fluid=True)

    if hide:
        layout = html.Div(layout, style={'display': 'none'})
    return layout

def get_main_layout(hide):
    df = latest_data['df']
    continents = [] if df is None else sorted(df['continent'].unique())
    countries = [] if df is None else sorted(df['country'].unique())

    layout = dbc.Container([
        dcc.Store(id="theme-store", data={"dark": False}),
        dcc.Store(id="updateActiveItems", data=True),
        dcc.Interval(id="update-interval", interval=10*1000, n_intervals=0),  # every 60 sec

        html.Div(  # <-- THIS is the main container
            id="main-container",
            children=[
                dbc.Row([
                    # dbc.Col(html.Img(src="assets/bnp_logo.jpg", style={
                    #     "display": "block",
                    #     "width": "auto",  # Stretch to fill left half   30
                    #     "height": "80px",  # Limit vertical height
                    #     "object-fit": "contain"  # Scale proportionally
                    # }), width=4, className="d-flex align-items-center justify-content-start p-1 m-1"),
                    dbc.Col(
                        html.Div([
                            html.Img(src="assets/bnp_logo.jpg", style={
                                "display": "block",
                                "width": "auto",
                                "height": "80px",
                                "object-fit": "contain"
                            }),
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Span("Powered by", className="credit-prefix"),
                                        html.Span("\u00A0"),
                                        html.Span("eFX Derivatives team", className="credit-main"),
                                        html.Span("  🚀", className="credit-icon"),
                                    ], className="credit-line"),
                                    html.Div("Part of eFic group", className="credit-sub credit-line")
                                ], className="d-flex flex-column")
                            ], className="credit-text ms-2")
                        ], className="d-flex align-items-center", style={"gap": "20px"}),
                        width=4,
                        className="d-flex align-items-center justify-content-start p-1 m-1"
                    ),
                    dbc.Col(html.H1("My app title", className="text-center mt-0 mb-2")),
                    dbc.Col([
                        dbc.Button("Logout", color="danger", className="mb-3", id="logout-button", n_clicks=0),
                        html.Div(
                            [
                                dbc.Switch(id="dark-mode-toggle", value=False),
                                html.Span("Dark Mode", style={"fontSize": "10px"}),
                            ],
                            className="d-flex align-items-center"
                        )
                    ], width=2, className="d-flex flex-column align-items-end"),
                ], className="my-3", id="top-bar"),
                html.Div(id='toast-container', style={'position': 'fixed', 'top': 10, 'right': 10, 'zIndex': 9999}),
                dbc.Row([
                    # Left Panel
                    dbc.Col([
                        html.Div(
                            id="last-updated",
                            className="last-updated-box",
                            style={
                                "fontSize": "12px",
                                "marginBottom": "30px",
                                "padding": "6px 12px",
                                "borderRadius": "8px",
                                'width': 'fit-content'
                            }
                        ),
                        html.Div(
                            html.I(className="bi bi-list", id="hamburger-icon"),  # ☰ icon
                            id="hamburger-container",
                            style={
                                "cursor": "pointer",
                                "padding": "10px",
                            }
                        ),
                        dbc.Collapse(
                                id="collapse-panel",
                                is_open=True,
                                children= [
                                    dcc.Dropdown(
                                        id="continent-dropdown",
                                        options=[{"label": c, "value": c} for c in continents],
                                        multi=True,
                                        value=['Europe', 'Asia'],
                                        placeholder="Select Continents",
                                        className="mb-3"
                                    ),
                                    dcc.Dropdown(
                                        id="country-dropdown",
                                        options=[{"label": c, "value": c} for c in countries],
                                        multi=True,
                                        placeholder="Select Countries",
                                        className="mb-3"
                                    ),
                                    dcc.Dropdown(
                                        id="option-dropdown",
                                        options=[{"label": f"Option {x}", "value": x} for x in range(1, 6)],
                                        multi=True,
                                        placeholder="Select Options",
                                        className="mb-4"
                                    ),
                                    dbc.Button("Apply", id="apply-button", color="success", className="mb-2", n_clicks=0),
                                    dbc.Alert(
                                        [
                                            "If you have any issues, please contact ",
                                            html.A("thisemail@address.com", href="mailto:thisemail@address.com",
                                                   style={"color": "inherit", "textDecoration": "underline"})
                                        ],
                                        color="info",
                                        className="mt-4",
                                        style={"fontSize": "11px"}
                                    )

                                    # dbc.Card(
                                    #     dbc.CardBody([
                                    #         html.P("If you have any issues, please contact ", className="mb-1"),
                                    #         html.A("thisemail@address.com", href="mailto:thisemail@address.com", className="text-primary")
                                    #     ]),
                                    #     style={"padding": "10px", "marginTop": "40px", "fontSize": "11px"}
                                    # )
                                ])
                    ], width=2, id="left-panel", className="p-3", style={"transition": "width 0.5s ease"}),

                    # Divider
                    #dbc.Col(html.Div(style={"borderLeft": "1px solid #ccc", "height": "100%"}), width="auto"),

                    # Main Area
                    dbc.Col([
                        html.Div([
                            dbc.Accordion(id="accordion-container", always_open=True)
                        ], style={"padding": "70px"})
                    ], width=10, id="main-area", className="p-3")
                ],  align="start", className="g-0")
            ]
        )
    ], fluid=True)
    if hide:
        layout = html.Div(layout, style={'display': 'none'})
    return layout


login_layout = html.Div([get_login_layout(False), get_main_layout(True)])
main_layout = html.Div([get_main_layout(False), get_login_layout(True)])


app.layout = html.Div([
    dcc.Location(id="url"),
    html.Div(id="page-content"),
    # dcc.Store(id={'type': 'login-state', 'index': 'session'}, storage_type='session'),
    #dcc.Store(id="login-state", data=False, storage_type='session'),  # Track login state with a Store
    dcc.Store(id="login-state", storage_type='session'),  # Track login state with a Store
    #dcc.Store(id="user", data='')
    # hidden_main_layout
])


@app.callback(
    Output('page-content', 'children'),
    Output('url', 'pathname'),
    Input('url', 'pathname'),
    Input('login-state', 'data'),  # Track if user is logged in or not
    #State('user', 'data')
)
def display_page(pathname, is_logged_in):
    if is_logged_in and is_logged_in['logged_in']:
        # User is logged in, show dashboard
        toast = dbc.Toast(
            "You have successfully logged in.",
            id='auto-toast',
            header=f"Welcome {is_logged_in['username']}",
            icon="success",
            duration=5000,  # milliseconds
            is_open=True
        )
        return html.Div([
            main_layout,
            html.Div(toast, id='toast-container', style={'position': 'fixed', 'top': '10%', 'left': '50%', 'zIndex': 9999, 'transform': 'translateX(-50%'})
        ]), '/my_app/dashboard'
        #return main_layout, '/my_app/dashboard'
    # If not logged in, show login page
    return login_layout, '/my_app/login'


@app.callback(
    Output("forgot-modal", "is_open"),
    Input("forgot-link", "n_clicks"),
    Input("close-modal", "n_clicks"),
    State("forgot-modal", "is_open"),
    prevent_initial_call=True
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# Handle login button click (for login-page) and logout button click (for dashboard) actions in a single callback
@app.callback(
    Output('login-state', 'data'),  # Update login state to True or False
    Output('login-alert', 'is_open'),
    #Output('user', 'data'),
    Input('login-button', 'n_clicks'),
    Input('logout-button', 'n_clicks'),
    State('login-username', 'value'),
    State('login-password', 'value'),
    prevent_initial_call=True
)
def handle_login_logout(login_clicks, logout_clicks, username, password):
    # Check which button triggered the callback
    triggered = dash.callback_context.triggered_id  # Get the component that triggered the callback

    # If login button is clicked
    if triggered == 'login-button' and login_clicks > 0:
        if username == 'admin' and password == 'password':  # Dummy login check
            #return True, False  # Set login state to True
            return {'logged_in': True, 'username': username}, False
        return dash.no_update, True

    # If logout button is clicked (on dashboard)
    elif triggered == 'logout-button' and logout_clicks > 0:
        #return False, False  # Set login state to False (log out)
        return {'logged_in': False, 'username': ''}, False

    # If no button is clicked (or invalid trigger)
    return dash.no_update, False


@app.callback(
    Output("last-updated", "children"),
    Input("update-interval", "n_intervals"),
    #Input("logout-button", "n_clicks"),
)
def update_time(n_intervals):#,  n_clicks):
    #now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    now = latest_data['timestamp']
    year = latest_data['year']
    return f"Last updated: {now} - {year}"


def update_outputs(selectedContinents, theme, inputActiveItems, updateActiveItems):
    if not selectedContinents:
        return [], ([] if updateActiveItems else inputActiveItems)

    df = latest_data['df']
    if df is None:
        return [], ([] if updateActiveItems else inputActiveItems)

    dark = theme.get("dark", False)
    plot_theme = "plotly_dark" if dark else "plotly_white"
    header_color = "#343a40" if dark else "#f8f9fa"
    text_color = "#f8f9fa" if dark else "#212529"
    bg_color = "#212529" if dark else "#fff"
    border_color = "#495057" if dark else "#dee2e6"

    table_header = {"backgroundColor": header_color, "color": text_color, "fontWeight": "bold"}
    table_data = {"color": text_color, "backgroundColor": bg_color, "border": f"1px solid {border_color}"}

    accordion_items = [None] * len(selectedContinents) * 2
    active_items = []
    clickableCol = lambda x: x + " 📈" if x == "pop" else x

    for ix, continent in enumerate(selectedContinents):
        filtered = df[df['continent'] == continent]
        filtered.columns = [clickableCol(i) for i in filtered.columns]

        # Create Dash DataTable
        table = dash_table.DataTable(
            data=filtered.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in filtered.columns],
            style_table={'overflowX': 'auto'},
            style_cell={'fontSize': '10px', 'padding': '5px'},
            style_header=table_header,
            style_data=table_data,
            row_selectable=False,
            # css=[{
            #     'selector': '.dash-table-row:hover',
            #     'rule': 'background-color: rgba(0, 123, 255, 0.2) !important;'
            # }],
            style_data_conditional=[
                {
                    "if": {"column_id": col},
                    "cursor": "pointer"
                } for col in filtered.columns if "📈" in col
            ] + [
                # {
                #     'selector': 'tr:hover',
                #     'backgroundColor': 'rgba(0, 123, 255, 0.2)',
                #     # 'cursor': 'pointer',
                # }
            ],
        )

        linkBtc = html.P([
            "For more information, ",
            html.A("click here", href="#", id="popup-link-1", style={"fontSize": "11px"},
                   className="popup-link", **{"data-url": "https://www.google.com/finance/quote/BTC-USD?hl=en&window=5Y"})
        ], style={"fontSize": "11px"}),

        accordion_items[ix] = dbc.AccordionItem([
                html.Div(table, style={"marginBottom": "20px"}, className="table-hover-effect"),
                #html.Div(linkBtc, style={"marginBottom": "20px"}, className="table-hover-effect"),
            ] + [html.Div(linkBtc, style={"marginBottom": "20px"}, className="mb-4")] if ix == 0 else [],
            title=f"Table: {continent}",
            item_id=f"item-table-{continent}",
            className="accordion-item-dark" if dark else "accordion-item-light"
        )
        active_items.append(f"item-table-{continent}")

        # Create chart
        fig = px.bar(filtered.head(10), x='country', y='gdpPercap', title=f"GDP per Capita: {continent}", template=plot_theme)
        chart = dcc.Graph(figure=fig)

        accordion_items[len(selectedContinents) + ix] = dbc.AccordionItem([
                html.Div(chart, style={"marginBottom": "20px"}),
            ],
            title=f"Chart: {continent}",
            item_id=f"item-chart-{continent}",
            className="accordion-item-dark" if dark else "accordion-item-light"

        )
        active_items.append(f"item-chart-{continent}")

    return accordion_items, (active_items if updateActiveItems else inputActiveItems)



@app.callback(
Output("accordion-container", "children"),
    Output("accordion-container", "active_item"),
    Output("updateActiveItems", "data"),
    Input("continent-dropdown", "value"),
    State("theme-store", "data"),
    #Input("update-interval", "n_intervals"),
    State("updateActiveItems", "data"),
    Input("accordion-container", "active_item"),
)
def update_outputs_continents(selected, theme, updateActiveItems, inputActiveItems):
    return update_outputs(selected, theme, inputActiveItems, updateActiveItems) + (False, )



@app.callback(
Output("accordion-container", "children", allow_duplicate=True),
    State("continent-dropdown", "value"),
    Input("theme-store", "data"),
    Input("update-interval", "n_intervals"),
    prevent_initial_call=True
)
def update_outputs_theme(selected, theme, n_intervals):
    out, _ = update_outputs(selected, theme, [], False)
    return out


@app.callback(
Output("updateActiveItems", "data", allow_duplicate=True),
       Input("continent-dropdown", "value"),
    prevent_initial_call=True
)
def update_active_items(selected):
    return True

@app.callback(
    Output("collapse-panel", "is_open"),
    Output("left-panel", "width"),
    Output("main-area", "width"),
    Output("updateActiveItems", "data", allow_duplicate=True),
    Input("hamburger-icon", "n_clicks"),
    State("collapse-panel", "is_open"),
    State("accordion-container", "active_item"),
    prevent_initial_call=True
)
def toggle_sidebar(n_clicks, is_open, activeItems):
    if is_open:
        return False, 0, 12, False  # Collapse sidebar
    else:
        return True, 2, 10, False   # Expand sidebar


@app.callback(
    Output("main-container", "className"),
    Input("theme-store", "data")
)
def toggle_dark_mode_class(theme_data):
    if theme_data.get("dark"):
        return "dark-mode"
    else:
        return "light-mode"

# Store dark mode setting
@app.callback(
    Output("theme-store", "data"),
    Input("dark-mode-toggle", "value")
)
def update_theme_store(is_dark):
    return {"dark": is_dark}



# Update country dropdown
@app.callback(
    Output("country-dropdown", "options"),
    Output("country-dropdown", "value"),
    Input("continent-dropdown", "value")
)
def update_countries(conts):
    df = latest_data['df']
    countries = [] if df is None else sorted(df['country'].unique())
    if not conts:
        return [{"label": c, "value": c} for c in countries], dash.no_update
    filtered = None if df is None else df[df["continent"].isin(conts)]
    filteredCountries = [] if filtered is None else sorted(filtered['country'].unique())
    return [{"label": c, "value": c} for c in filteredCountries], []


@app.callback(
    Output("continent-dropdown", "className"),
    Output("country-dropdown", "className"),
    Output("option-dropdown", "className"),
    Input("theme-store", "data")
)
def update_select_theme(theme):
    dark = theme.get("dark", False)
    base_class = "mb-3" if not dark else "mb-3 bg-dark text-white border-light"
    base_class_last = "mb-4" if not dark else "mb-4 bg-dark text-white border-light"

    return base_class, base_class, base_class_last

if __name__ == "__main__":
    app.run(debug=True)
