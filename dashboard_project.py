from datetime import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import quandl
from dash.dependencies import Input, Output

app = dash.Dash()
server = app.server
eurnxt = pd.read_csv('./data/EURONEXT_metadata.csv')
eurnxt.set_index('code', inplace=True)
options = []
for code in eurnxt.index:
    mydict = {}
    mydict['label'] = eurnxt.loc[code]['name']
    mydict['value'] = code
    options.append(mydict)

quandl.ApiConfig.api_key = "y4Yy1Xb96bhB1exu3VEy"

app.layout = html.Div([
    html.H1('Euronext Stocks Dashboard'),
    html.Div([html.H3('Select Tickers', style={'paddingRight': '30px'}),
              dcc.Dropdown(id='my_stock_picker',
                           value=['RDSA', 'FP'],
                           options=options,
                           multi=True,
                           style={'fontSize': 12, 'width': 200}
                           )], style={'display': 'inline-block', 'verticalAlign': 'top'}),
    html.Div([html.H3('Start & End Date:'),
              dcc.DatePickerRange(id='my_date_picker',
                                  min_date_allowed=datetime(1999, 1, 1),
                                  max_date_allowed=datetime.today(),
                                  start_date=datetime(2019, 1, 1),
                                  end_date=datetime.today())
              ], style={'display': 'inline-block'}),
    dcc.Graph(id='my_graph',
              figure={'data': [{'x': [1, 2, 3], 'y': [4, 5, 6]}],
                      'layout': {'title': 'Default Title'}}),
    dcc.Graph(id='volume',
              figure={'data': [go.Histogram(x=[1, 2, 3],
                                            y=[4, 5, 6],
                                            marker_color='#cf1020')],
                      'layout': {'title': 'Volume'}})
])


@app.callback(Output('my_graph', 'figure'),
              [Input('my_stock_picker', 'value'),
               Input('my_date_picker', 'start_date'),
               Input('my_date_picker', 'end_date')
               ])
def update_graph(stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')

    trace = []
    for ticker in stock_ticker:
        df = quandl.get('EURONEXT/{}'.format(ticker), start_date=start, end_date=end)
        trace.append({'x': df.index, 'y': df['Last'], 'name': ticker})

    fig = {'data': trace,
           'layout': {'title': stock_ticker}
           }
    return fig


@app.callback(Output('volume', 'figure'),
              [Input('my_stock_picker', 'value'),
               Input('my_date_picker', 'start_date'),
               Input('my_date_picker', 'end_date')
               ])
def update_histogram(stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')

    trace = []
    for ticker in stock_ticker:
        df = quandl.get('EURONEXT/{}'.format(ticker), start_date=start, end_date=end)
        trace.append(go.Bar(x=df.index, y=df['Volume'],
                                  name=ticker,
                                  opacity=0.7,))

    fig = {'data': trace,
           'layout': {'title': 'Volume'}
           }
    return fig


if __name__ == '__main__':
    app.run_server()
