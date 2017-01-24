
# coding: utf-8

# In[5]:

import urllib, sqlite3
import time, datetime
from bs4 import BeautifulSoup


# connect to the database
con = sqlite3.connect('C:\\NBA\\nba.db') # create database in the directory where the .py file is saved
cur = con.cursor()

boxscore_links = []
#yesterday = datetime.datetime.strptime('2016-11-15', '%Y-%m-%d')
yesterday = (datetime.date.today() + datetime.timedelta(days=-1)) 


url = 'http://www.basketball-reference.com/boxscores/index.cgi?month=' + str(yesterday.month) + '&day=' + str(yesterday.day) + '&year=' + str(yesterday.year)

html = urllib.urlopen(url).read()
soup = BeautifulSoup(html, "lxml")
for p in soup.findAll('p'):
    if p.a != None:
        if p.a.string == 'Box Score':
            boxscore_links.append('http://www.basketball-reference.com' + p.a.get('href', None))

            
# collect the current max game in the table 
cur.execute('SELECT MAX(game_id) FROM games')
for g in cur:
    game_id = g[0]

for url in boxscore_links:
    game_id += 1

    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")

    # collect the game details
    titles = soup('title')

    for t in titles:
        if 'Box Score' in t.string:
            away = t.string.split(' at ')[0].strip()
            home = t.string.split(' at ')[1].split(' Box')[0].strip()
            date = t.string.split('Score, ')[1].split('|')[0].strip()
            year = date.split(', ')[1]
            month = date.split(' ')[0]
            day = date.split(' ')[1].split(',')[0].strip()
            day = '00' + day
            day = day[-2:]
            if month == 'January':
                month = '01'
            elif month == 'February':
                month = '02'
            elif month == 'March':
                month = '03'
            elif month == 'April':
                month = '04'
            elif month == 'May':
                month = '05'
            elif month == 'June':
                month = '06'
            elif month == 'July':
                month = '07'
            elif month == 'August':
                month = '08'
            elif month == 'September':
                month = '09'
            elif month == 'October':
                month = '10'
            elif month == 'November':
                month = '11'
            elif month == 'December':
                month = '12'
            date = year + '-' + month + '-' + day

            if int(month) > 9:
                season = int(year) + 1
            else:
                season = int(year) 


    stats_input = [] # empty list to store the tuples that will be inserted into the stats table
    for i in range(0,3,2): # tables 0 and 2
        if i == 0:
            team = away
            home_flag = 0
        else:
            team = home
            home_flag = 1
        for tr in soup('table')[i].findAll('tr'):
            if tr.th.get('data-stat', None) == 'player':
                if tr.th.get('scope', None) == 'row':
                    if tr.th.string != 'Team Totals':
                        player_id = tr.th.get('data-append-csv',None)
                        for td in tr.findAll('td'):
                            if td.get('data-stat',None) == 'mp':
                                minutes_played = td.string
                            elif td.get('data-stat',None) == 'fg':
                                field_goals = td.string
                            elif td.get('data-stat',None) == 'fga':
                                field_goal_attempts = td.string
                            elif td.get('data-stat',None) == 'fg3':
                                three_pointers = td.string
                            elif td.get('data-stat',None) == 'fg3a':
                                three_point_attempts = td.string
                            elif td.get('data-stat',None) == 'ft':
                                free_throws = td.string
                            elif td.get('data-stat',None) == 'fta':
                                free_throw_attempts = td.string
                            elif td.get('data-stat',None) == 'orb':
                                offensive_rebounds = td.string
                            elif td.get('data-stat',None) == 'drb':
                                defensive_rebounds = td.string
                            elif td.get('data-stat',None) == 'trb':
                                total_rebounds = td.string
                            elif td.get('data-stat',None) == 'ast':
                                assists = td.string
                            elif td.get('data-stat',None) == 'stl':
                                steals = td.string
                            elif td.get('data-stat',None) == 'blk':
                                blocks = td.string
                            elif td.get('data-stat',None) == 'tov':
                                turnovers = td.string
                            elif td.get('data-stat',None) == 'pf':
                                personal_fouls = td.string
                            elif td.get('data-stat',None) == 'pts':
                                points = td.string
                        player_stats = (game_id,date,team,home_flag,season,player_id,minutes_played,field_goals,field_goal_attempts,three_pointers,three_point_attempts,free_throws,free_throw_attempts,offensive_rebounds,defensive_rebounds,total_rebounds,assists,steals,blocks,turnovers,personal_fouls,points)
                        stats_input.append(player_stats)

    # update the database
    for input_row in stats_input:
        cur.execute('INSERT INTO games VALUES(?' + ',?'*21 + ')',input_row)

    con.commit()    # commit inserted rows
        
con.close()
                
                


# In[ ]:



