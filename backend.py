import pymysql
import pandas as pd 
from datetime import date 

def query(team: str, start_date, end_date):
    db = pymysql.connect(
        host = 'localhost',
        user = 'root', 
        password = 'szm6N5zm8vqwi$', 
        database= 'nba_shots'
    )
    cursor = db.cursor() 
    try: 
        select_statement = f""" 
            select shotX, shotY 
            from {team}
            where date >= %s and date <= %s
        """
        cursor.execute(select_statement,
                       create_date_obj(start_date),
                       create_date_obj(end_date))
        info = cursor.fetchall() 
        frame = pd.DataFrame(info, columns=['shotX', 'shotY'])
        return frame
    except Exception as e: 
        print("DataBase error, failed during selection", e) 
    finally: 
        db.close() 

def create_date_obj(date): 
    date = date(date, 1, 1) 
    return date
