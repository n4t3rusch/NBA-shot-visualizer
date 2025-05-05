import dash
import plotly as plot 
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import backend
from backend import team_translation, dates
import atexit

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#DR. YU! THE DATABASE IS LOCAL NOT HOSTED AND WILL NOT RUN IF YOU TRY TO RUN IT !
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

app = Dash(external_stylesheets = [
            'https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap'
        ]
)

app.layout = html.Div([

    html.H1(children = 'NBA shot dashboard', style = {'textAlign':'center', 'fontFamily': 'Bebas Neue', 'fontSize': '60px'}),
   
    html.Div([
        dcc.Dropdown(list(team_translation.keys()),
                     value = None, 
                     id = 'team-select', 
                     placeholder = "select a team",
                     style = {'width': '200px', 'marginRight': '10px'}),       
        dcc.Dropdown(dates, 
                     "start-date", 
                     id = 'start', 
                     placeholder = "select a start date",
                     style = {'width': '200px', 'marginRight': '10px'}), 
        dcc.Dropdown(dates, 
                     "end-date ", 
                     id = 'end', 
                     placeholder = "select an end date",
                     style = {'width' : '200px'}),
    ], style = {
            'display': 'flex',
            'justifyContent': 'center',  
            'gap': '10px',
            'width': '100%'
        }),
        html.Div([
            dcc.Input(
                id = 'player-entry',
                type = 'text',
                placeholder = 'enter a player',
                debounce = True,
                style = {
                    'width': '25%',
                    'padding': '10px',
                    'borderRadius': '20px',
                    'overflow': 'hidden',
                    'marginTop': '20px',
                    'marginBottom': '20px'
                }
            )
        ], style = {
            'display': 'flex',
            'justifyContent': 'center'
        }),
    html.Div([
        dcc.Loading(
            id = "loading-graph1",
            children = [dcc.Graph(id = 'heatmap', 
                                figure = {}, 
                                style = {
                                'border': '2px solid white',
                                'borderRadius': '20px',
                                'overflow': 'hidden',
                                'width': '600px',
                                'height': '400px'})],
                                type="default"
        ),
        dcc.Loading(
            id = "loading-graph2",
            children = [dcc.Graph(id = "stacked-bar",
                                figure = {},
                                style = {
                                'border': '2px solid white',
                                'borderRadius': '20px',
                                'overflow': 'hidden',
                                'width': '600px',
                                'height': '400px'})],
                                type="default"
        )
    ], style = {'display': 'flex', 'justifyContent': 'space-around'}),
    html.Div(id = 'info',
            children = [
            html.P('Average Distance: ...', style = {'margin': '5px'}),
            html.P('Farthest Shot Made ...', style = {'margin': '5px'}),
            html.P(f"Accuracy: ...", style = {'margin': '5px'})
            ], 
            style = {'textAlign': 'center', 'fontFamily': 'Bebas Neue','fontSize': '20px', 'marginTop': '20px'})
], style = {'backgroundColor': '#DCDCDC', 'minHeight': '100vh'})

@app.callback(
    [Output("heatmap", "figure"),
     Output("stacked-bar", "figure"),
     Output("info", "children")],
    
    [Input("team-select", "value"),
     Input("player-entry", "value"),
     Input("start", "value"),
     Input("end", "value")]
)

def plot(team, player, start, end): 
    if team and start and end and end > start: 
        heatmap, bar, avg, acc = backend.team_query(team_translation[team], start, end)
        return heatmap, bar, [
            html.Div(f"Average Distance: {avg[0]:.2f} feet", style={'margin': '5px'}),
            html.Div(f"Farthest Shot Made: {avg[1]:.2f} feet", style={'margin': '5px'}),
            html.Div(f"Accuracy: {acc}%", style = {'margin': '5px'})
        ]
    elif start and end and player and end > start: 
        heatmap, bar, avg, acc = backend.player_query(player, start, end) 
        return heatmap, bar, [
            html.Div(f"Average Distance: {avg[0]:.2f} feet", style={'margin': '5px'}),
            html.Div(f"Farthest Shot Made: {avg[1]:.2f} feet", style={'margin': '5px'}),
            html.Div(f"Accuracy: {acc}%", style = {'margin': '5px'})
        ]
    return {}, {}, []

atexit.register(backend.exit)

if __name__ == '__main__':
    app.run(debug=True)