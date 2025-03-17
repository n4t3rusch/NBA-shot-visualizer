import dash
import plotly as plot 
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import backend

team_translations = {
    "atl": "hawks", "bos": "celtics", "chh": "hornets", "chi": "bulls",
    "cle": "cavaliers", "dal": "mavericks", "den": "nuggets", "det": "pistons", "gsw": 
    "golden state warriors", "hou": "rockets", "ind": "pacers", "lal": "lakers","lac": "clippers",
    "mem": "grizzlies", "mia": "heat","mil": "bucks","min": "timberwolves","njn": "nets", "nyk": "knicks",
    "nop": "pelicans","sea": "thunder", "orl": "magic","phi": "76ers","pho": "suns",
    "por": "blazers", "sac": "kings", "sas": "spurs","uta": "jazz","tor": "raptors","was": "wizards"
}
app = Dash() 

app.layout = [
    html.H1(children='NBA shots', style={'textAlign':'center'}),
    dcc.Dropdown(list(team_translations.values()), "select a team", id='dropdown-selection'),
]

#df = backend.query(team, start, end)

if __name__ == '__main__':
    app.run(debug=True)