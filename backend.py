import pandas as pd 
import plotly.express as px
import numpy as np 
from datetime import date 
from credentials import db 

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#DR. YU! THE DATABASE IS LOCAL NOT HOSTED AND WILL NOT RUN IF YOU TRY TO RUN IT !
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def team_query(team: str, start_date:int, end_date:int):
    cursor = db.cursor() 
    try: 
        select_statement = f""" 
            select shotX, shotY, date, made
            from shots
            where date >= %s and date <= %s 
            and team = %s 
        """
        cursor.execute(select_statement,
                       (create_date_obj(start_date),
                       create_date_obj(end_date),
                       team))
        info = cursor.fetchall() 
        frame = pd.DataFrame(info, columns = ['shotX', 'shotY', 'date', 'made'])
        if frame.empty: 
            print("No data for query")
            return {}, {}, []
        filtered = frame[frame['made'] == 1]
        if filtered.empty: 
            return visualize_bar_chart(frame)
        return visualize_heat_map(filtered), visualize_bar_chart(frame), get_avg_distance(filtered), get_make_percentage(frame)
    except Exception as e: 
        print("DataBase error, failed during selection", e)

def player_query(player: str, start_date:int, end_date:int): 
    cursor = db.cursor() 
    try: 
        select_statement = f""" 
            select shotX, shotY, date, made
            from shots 
            where date >= %s and date <= %s
            and player = %s 
        """
        cursor.execute(select_statement, 
                       (create_date_obj(start_date),
                        create_date_obj(end_date), 
                        player))
        info = cursor.fetchall()
        frame = pd.DataFrame(info, columns=['shotX', 'shotY', 'date', 'made'])
        if frame.empty: 
            print("No data for query")
            return {}, {}, []
        filtered = frame[frame['made'] == 1]
        if filtered.empty: 
            return visualize_bar_chart(frame)
        return visualize_heat_map(filtered), visualize_bar_chart(frame), get_avg_distance(filtered), get_make_percentage(frame)
    except Exception as e: 
        print(f"failed to gather data on {player}, please try their full legal name", e)

def visualize_heat_map(dataframe): 
    try:
        fig = px.density_heatmap(
            dataframe,
            x = "shotX",
            y = "shotY",
            title = "HeatMap of made shots",
            color_continuous_scale = "RdBu",
            nbinsx = 50,
            nbinsy = 50,
            range_color = [0, 75]
        )
        return fig
    except Exception as e: 
        print("failed to generate heat map", e)
        return 
    
def visualize_bar_chart(dataframe): 
    try: 
        dataframe["year"] = pd.to_datetime(dataframe["date"]).dt.year
        yearly_counts = dataframe.groupby(["year", "made"]).size().unstack(fill_value=0)
        yearly_counts.columns = ["Missed", "Made"]
        fig = px.bar(
            yearly_counts.reset_index(),
            x = "year",
            y = ["Missed", "Made"],
            title = "Shots Made vs. Missed per Year",
            labels = {"value": "Shot Count", "year": "Year"},
            barmode = "group"
        )
        return fig
    except Exception as e: 
        print("failed to generate bar chart", e)
        return

def get_avg_distance(frame): 
    distances = np.sqrt((frame["shotX"] - 23.95) ** 2 + (frame["shotY"] - 4.95) ** 2)
    return [distances.mean(), max(distances)]

def get_make_percentage(frame): 
    makes = frame[frame['made'] == 1].shape[0]
    total = frame.shape[0]
    accuracy = (makes / total) * 100
    return int(accuracy)

def create_date_obj(year): 
    formatted = date(year, 1, 1) 
    return formatted

def exit(): 
    db.close()

dates = [
         2000, 2001, 2002, 2003, 2004, 
         2005, 2006, 2007, 2008, 2009,
         2010, 2011, 2012, 2013, 2014, 
         2015, 2016, 2017, 2018, 2019, 
         2020, 2021, 2022
         ]

team_translation = {
    'hawks': "ATL", 'celtics': "BOS", "hornets": 'CHH', 'bulls':"CHI", 'cavaliers': "CLE",
    'mavericks': "DAL", 'nuggets': "DEN", "pistons": 'DET', "golden state warriors": 'GSW', "rockets":'HOU', 
    "pacers":'IND', "clippers": 'LAC', "lakers": 'LAL', "grizzlies":'MEM', "heat":'MIA', 
    "bucks":'MIL', "timberwolves": 'MIN', "nets": 'NJN', "knicks": 'NYK', "magic": 'OLR',
    "76ers": 'PHI', "suns": 'PHO', "trailblazers": 'POR', "kings": 'SAC', "spurs": 'SAS', 
    "sonics (no longer the sonics)": 'SEA', "raptors": 'TOR', "jazz": 'UTA', "grizzlies (vancouver)": 'VAN', "wizards": 'WAS'
}