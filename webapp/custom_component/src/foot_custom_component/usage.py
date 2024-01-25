from dash import Dash, callback, html, Input, Output

import foot_custom_component

app = Dash(__name__)

app.layout = html.Div([
    foot_custom_component.FootCustomComponent(
        id='foot-custom-component',
        data='data',
    ),
    html.Div(id='output')
])


@callback(Output('foot-custom-component', 'data'), Input('input', 'value'))
def display_output(value):
    return """[
        {
            "name": "L0",
            "value": 16,
            "anomaly": false
        },
        {
            "name": "L1",
            "value": 138,
            "anomaly": false
        },
        {
            "name": "L2",
            "value": 13,
            "anomaly": false
        },
        {
            "name": "R0",
            "value": 1023,
            "anomaly": false
        },
        {
            "name": "R1",
            "value": 1023,
            "anomaly": false
        },
        {
            "name": "R2",
            "value": 896,
            "anomaly": false
            }
    ]"""


if __name__ == '__main__':
    app.run_server(debug=True)
