import dash
import plotly as plot 
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import backend
from backend import team_translation, dates
import atexit

app = Dash()

app.layout = html.Div([
    html.H1(children = 'NBA shots', style = {'textAlign':'center'}),
   
    html.Div([
        dcc.Dropdown(list(team_translation.keys()),
                     value = None, 
                     id = 'team-select', 
                     placeholder = "select a team",
                     style={'width': '50%', 'marginRight': '10px'}),       
        dcc.Dropdown(dates, 
                     "start-date", 
                     id = 'start', 
                     placeholder = "select a start date",
                     style={'width': '50%', 'marginRight': '10px'}), 
        dcc.Dropdown(dates, 
                     "end-date ", 
                     id = 'end', 
                     placeholder = "select an end date",
                     style = {'width' : '50%'}),
    ], style={'display': 'flex', 'width': '100%', 'justifyContent': 'space-between'}),

        dcc.Input(
            id='player-entry',
            type='text',
            placeholder = 'enter a player',
            debounce = True,
            style={'width': '50%', 'padding': '10px'}
        ),
    html.Div([
        dcc.Loading(
            id="loading-graph1",
            children=[dcc.Graph(id='heatmap', figure={})],
            type="default"
        ),
        dcc.Loading(
            id="loading-graph2",
            children=[dcc.Graph(id="stacked-bar", figure={})],
            type="default"
        )
    ], style={'display': 'flex', 'justifyContent': 'space-around'})
])


@app.callback(
    [Output("heatmap", "figure"),
     Output("stacked-bar", "figure")],
    [Input("team-select", "value"),
     Input("player-entry", "value"),
     Input("start", "value"),
     Input("end", "value")]
)

def plot(team, player, start, end): 
    if team and start and end and end > start: 
        return backend.team_query(team_translation[team], start, end)
    elif start and end and player and end > start: 
        return backend.player_query(player, start, end) 
    return {}, {}

atexit.register(backend.exit)

if __name__ == '__main__':
    app.run(debug=True)