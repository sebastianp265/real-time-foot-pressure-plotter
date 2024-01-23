import dash
import dash_bootstrap_components as dbc
from dash import html

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    dbc.Row(
        dbc.Col(html.H1("Hello Dash"), width={"size": 6, "offset": 3}),
        className="mb-4",
    ),
    fluid=True,
)

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")
