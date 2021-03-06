
# coding: utf-8

# In[5]:

import sqlite3
import time, datetime
import sys

yesterday = (datetime.date.today() + datetime.timedelta(days=-1)) 
#yesterday = datetime.datetime.strptime('2016-11-15', '%Y-%m-%d')

# connect to database 
con = sqlite3.connect('C:\\NBA\\nba.db')
cur = con.cursor()
cur2 = con.cursor()
cur3 = con.cursor()
cur4 = con.cursor()


cur.execute("SELECT DISTINCT player_id FROM games WHERE game_date = '" + yesterday.strftime("%Y-%m-%d") + "'")

for player in cur:

    cur2.execute("SELECT DISTINCT game_id, game_date, season FROM games WHERE player_id = '" + player[0] + "' AND game_date = '" + yesterday.strftime("%Y-%m-%d") + "'")
    for game in cur2:
        game_id = str(game[0])
        game_date = str(game[1])
        season = str(game[2])
        query = open('C:\\NBA\\SQL\\player_template.sql','r')
        query = query.read()

        query_new = query.replace('<player>',player[0])
        query_new = query_new.replace('<season>',season)
        query_new = query_new.replace('<game_date>',str(game_date))
        cur3.execute(query_new)
        game_insert = [player[0], game_id, season, game_date]
        for game in cur3:
            game = list(game)
            for item in game:
                game_insert.append(item)
            #print game_insert
            cur4.execute('INSERT INTO player_stats VALUES(?' + ',?'*48 + ')',game_insert)
    con.commit()    # commit inserted rows

con.close()
            


# In[ ]:



