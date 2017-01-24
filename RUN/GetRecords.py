
# coding: utf-8

# In[1]:

import sqlite3, datetime

yesterday = (datetime.date.today() + datetime.timedelta(days=-1)) 
#yesterday = datetime.datetime.strptime('2013-03-07', '%Y-%m-%d')

if datetime.date.today().month > 9:
    season = datetime.date.today().year + 1
else:
    season = datetime.date.today().year

con = sqlite3.connect('C:\\NBA\\nba.db')
cur = con.cursor()
cur2 = con.cursor()
cur3 = con.cursor()

cur.execute("""
            SELECT DISTINCT player_id, game_id 
            FROM player_stats
            WHERE player_id IN
            (
            SELECT DISTINCT player_id
            FROM 
            (
            SELECT player_id, COUNT(*) 
            FROM player_stats 
            GROUP BY player_id 
            HAVING COUNT(*) > 19
            ) tab
            )
            AND game_date = '""" + yesterday.strftime("%Y-%m-%d") + "'"
            )


for game in cur:
    player_id = str(game[0])
    game_id = str(game[1])
    query = open('C:\\NBA\\SQL\\records_template.sql','r')
    query = query.read()
    query_new = query.replace('<player_id>',player_id)
    query_new = query_new.replace('<game_id>',str(game_id))
    
    cur2.execute(query_new)
    for record in cur2:
        record = list(record)
        record.append(season)
        record = tuple(record)
        
        cur3.execute('INSERT INTO records VALUES(?' + ',?'*84 + ')',record)

    con.commit()    # commit inserted rows
con.close()
            


# In[ ]:



