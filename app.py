# app.py

import pandas as pd
from dash import Dash, Input, Output, dcc, html

data = (
    pd.read_csv("coastalwater.csv")
    #.query("Characteristic == 'pH' and Site == 'Albion'")
    .assign(date=lambda data: pd.to_datetime(data["date"], format="%m/%d/%Y"))
    .sort_values(by="date")
)

sites = data["Site"].sort_values().unique()
characterisitics = data["Characteristic"].sort_values().unique()

external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Mauritius Coastal Water Data"

server = app.server

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🟥🟦🟨🟩", className="header-emoji"),
                html.H1(
                    children="Coastal Water Analytics", className="header-title"
                ),
                html.P(
                    children=(
                        "Physical and Chemical Characteristics of Coastal Water by Level and Monitoring Site in Mauritius"

                    ),
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Site", className="menu-title"),
                        dcc.Dropdown(
                            id="site-filter",
                            options=[
                                {"label": Site, "value": Site}
                                for Site in sites
                            ],
                            value="Albion",
                            clearable=False,
                            className="dropdown"
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Characteristics", className="menu-title"),
                        dcc.Dropdown(
                            id = "charac-filter",
                            options=[
                                {
                                    "label": char_type.title(),
                                    "value": char_type,
                                }
                                for char_type in characterisitics
                            ],
                            value="pH",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                
            ],
            className="wrapper",
        ),
         html.Div(
            children=[
                html.A("Created by Damian Perera", href="https://www.linkedin.com/in/damian-perera-3b7b88181/",target="_blank"),
            ],
            className="footer",
        ),
        html.Div(
            children=[
                html.A("Source: Open Data Mauritius", href="https://data.govmu.org/dkan/?q=dataset/physical-and-chemical-characteristics-coastal-water-level-and-monitoring-site-mauritius",target="_blank"),
            ],
            className="footer-source"
        )
    ],
    
)

@app.callback(
    Output("price-chart", "figure"),
   # Output("volume-chart", "figure"),
    Input("site-filter", "value"),
    Input("charac-filter", "value"),
)

def update_charts(Site, Characteristic):
    filtered_data = data.query(
        "Site == @Site and Characteristic == @Characteristic"
    )
    price_chart_figure = {
        "data": [
            {
                "x": filtered_data["date"],
                "y": filtered_data["Average"],
                "type": "lines",
                #"hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Coastal Water Data (Chosen characteristics are average values)",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"title": "Year"},
            "yaxis": {"title":  Characteristic},
            #"xaxis": {"fixedrange": False},
            #"yaxis": {"tickprefix": "$", "fixedrange": False},
            #"colorway": {"#17B897"}
        }
    }

   
    return price_chart_figure

if __name__ == "__main__":
    app.run_server(debug=True)