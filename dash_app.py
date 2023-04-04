import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash import callback_context

import flask
import pandas as pd
import numpy as np
import random
import time
from datetime import datetime

START_DATE = pd.to_datetime('01/01/1900')
END_DATE = pd.to_datetime('today')
INTERVAL = (END_DATE - START_DATE).days
DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

server = flask.Flask('app')
app = dash.Dash('app', server=server)



app.layout = html.Div([
    dcc.Store(id='correct-answer'),
    dcc.Store(id='start-time'),

    html.H1('Doomsday Algorithm'),
    dbc.Button('New Date', id='generate-date-button'),
    html.H2(id='random-date'),
    dbc.Row([dbc.Button(day, id=day) for day in DAYS]),
    html.H2(id='result'),
    html.H2(id='time-to-answer')
    
], className="container")

def random_date():
    days = np.random.randint(low = 0, high = INTERVAL)
    date = START_DATE + pd.DateOffset(days = days)
    return date.strftime('%B %d, %Y'), DAYS[date.dayofweek]
    

@app.callback(
    Output('random-date', 'children'),
    Output('correct-answer', 'data'),
    Output('start-time', 'data'),
    [Input('generate-date-button', 'n_clicks')]
)
def generate_date(n_clicks):
    if "generate-date-button" == callback_context.triggered_id:
        date, weekday = random_date()
        start = time.time()
        return date, weekday, start
    else:
        return '', '', ''

@app.callback(
    Output('result', 'children'),
    Output('time-to-answer', 'children'),
    [Input('correct-answer', 'data'), Input('start-time', 'data')] + [Input(day, 'n_clicks') for day in DAYS]
)
def validate_answer(answer, start, *args):
    print(answer)
    if answer == callback_context.triggered_id:
        end = time.time()
        time_to_answer = round(end - start, 2)
        return 'Correct!', f'That took you {time_to_answer} seconds'
    else:
        return '', ''

if __name__ == '__main__':
    app.run_server(debug=True)