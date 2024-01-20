from dash import Dash, callback, html, dcc, Input, Output, State
import dash
import redis
from app import get_data_from_redis

# Get the pandas dataframe from redis
# dataframe is a static data, form of this data is the same as was in Ex7
df = get_data_from_redis(redis.Redis(host='localhost', port=6379))


def create_table(dataframe):
    return html.Table(
        [
            html.Tr([html.Td(col, style={"border": "1px solid grey"}) for col in dataframe.loc[idx]]) for idx in
            dataframe.index
        ]
    )


app = Dash(__name__)

app.layout = html.Div(children=[
    dcc.Store(id='memory-output'),
    html.H1(children='Paging Table from Pandas DataFrame'),
    html.Div([
        html.Button("< < Top Left", id="top-left", disabled=True),
        html.Button("<- Left", id="cmd-left", disabled=True),
        dcc.Input(id='nrows', value="10", size="3"),
        html.Button("Right ->", id="cmd-right", disabled=False),
        html.Button("Top Right > >", id="top-right", disabled=False),
    ]),

    html.Div(id='output')
])


@callback(
    Output('output', 'children'),
    Output('memory-output', 'data'),
    Output('top-left', 'disabled'),
    Output('cmd-left', 'disabled'),
    Output('cmd-right', 'disabled'),
    Output('top-right', 'disabled'),
    Input('nrows', 'value'),
    Input('top-left', 'n_clicks'),
    Input('cmd-left', 'n_clicks'),
    Input('cmd-right', 'n_clicks'),
    Input('top-right', 'n_clicks'),
    State('memory-output', 'data')
)
def update_table(nrows, clicks_tl, clicks_l, clicks_r, clicks_tr, data):
    print(data)
    data = data or {
        "start": 0,
    }
    try:
        nrows = int(nrows)
    except:
        nrows = 10

    if dash.ctx.triggered_id == "cmd-right":
        data['start'] = data['start'] + nrows
    if dash.ctx.triggered_id == "cmd-left":
        data['start'] = data['start'] - nrows
    if dash.ctx.triggered_id == "top-right":
        data['start'] = len(df) - nrows
    if dash.ctx.triggered_id == "top-left":
        data['start'] = 0

    return create_table(df.iloc[data['start']: data['start'] + nrows, :]), data, data['start'] <= 0, data['start'] <= 0, \
                                                                                 data['start'] + nrows >= len(df), data[
                                                                                     'start'] + nrows >= len(df)


if __name__ == '__main__':
    app.run_server(debug=True)