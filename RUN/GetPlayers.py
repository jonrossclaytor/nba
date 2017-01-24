
# coding: utf-8

# In[1]:

import urllib, sqlite3
from bs4 import BeautifulSoup
import time, datetime

# create the database
con = sqlite3.connect('C:\\NBA\\nba.db') # create database in the directory where the .py file is saved
cur = con.cursor()

cur.execute('DROP TABLE IF EXISTS players')
cur.execute('''CREATE TABLE players
             (
              player_id TEXT
             ,player_name TEXT
             ,player_name_strip TEXT
             ,position TEXT
             ,team_id TEXT
             ,team_name TEXT
             ,dk_team_abbr TEXT
             )''')

if datetime.date.today().month > 9:
    season = datetime.date.today().year + 1
else:
    season = datetime.date.today().year

team_list = ['ATL','BOS','BRK','CHO','CHI','CLE','DAL','DEN','DET','GSW','HOU','IND','LAC','LAL','MEM','MIA','MIL','MIN','NOP','NYK','OKC','ORL','PHI','PHO','POR','SAS','SAC','TOR','UTA','WAS']

for team_id in team_list:
    if team_id == 'ATL': 
        team_name = 'Atlanta Hawks'
        dk_team_abbr = 'Atl'
    elif team_id == 'BOS': 
        team_name = 'Boston Celtics'
        dk_team_abbr = 'Bos'
    elif team_id == 'BRK':
        team_name = 'Brooklyn Nets'
        dk_team_abbr = 'Bkn'
    elif team_id == 'CHO':
        team_name = 'Charlotte Bobcats'
        dk_team_abbr = 'Cha'
    elif team_id == 'CHI': 
        team_name = 'Chicago Bulls'
        dk_team_abbr = 'Chi'
    elif team_id == 'CLE': 
        team_name = 'Cleveland Cavaliers'
        dk_team_abbr = 'Cle'
    elif team_id == 'DAL': 
        team_name = 'Dallas Mavericks'
        dk_team_abbr = 'Dal'
    elif team_id == 'DEN': 
        team_name = 'Denver Nuggets'
        dk_team_abbr = 'Den'
    elif team_id == 'DET': 
        team_name = 'Detroit Pistons'
        dk_team_abbr = 'Det'
    elif team_id == 'GSW': 
        team_name = 'Golden State Warriors'
        dk_team_abbr = 'GS'
    elif team_id == 'HOU': 
        team_name = 'Houston Rockets'
        dk_team_abbr = 'Hou'
    elif team_id == 'IND': 
        team_name = 'Indiana Pacers'
        dk_team_abbr = 'Ind'
    elif team_id == 'LAC': 
        team_name = 'Los Angeles Clippers'
        dk_team_abbr = 'LAC'
    elif team_id == 'LAL': 
        team_name = 'Los Angeles Lakers'
        dk_team_abbr = 'LAL'
    elif team_id == 'MEM': 
        team_name = 'Memphis Grizzlies'
        dk_team_abbr = 'Mem'
    elif team_id == 'MIA': 
        team_name = 'Miami Heat'
        dk_team_abbr = 'Mia'
    elif team_id == 'MIL': 
        team_name = 'Milwaukee Bucks'
        dk_team_abbr = 'Mil'
    elif team_id == 'MIN': 
        team_name = 'Minnesota Timberwolves'
        dk_team_abbr = 'Min'
    elif team_id == 'NOP': 
        team_name = 'New Orleans Hornets'
        dk_team_abbr = 'NO'
    elif team_id == 'NYK': 
        team_name = 'New York Knicks'
        dk_team_abbr = 'NY'
    elif team_id == 'OKC': 
        team_name = 'Oklahoma City Thunder'
        dk_team_abbr = ''
    elif team_id == 'ORL': 
        team_name = 'Orlando Magic'
        dk_team_abbr = 'Orl'
    elif team_id == 'PHI': 
        team_name = 'Philadelphia 76ers'
        dk_team_abbr = 'Phi'
    elif team_id == 'PHO': 
        team_name = 'Phoenix Suns'
        dk_team_abbr = 'Pho'
    elif team_id == 'POR': 
        team_name = 'Portland Trail Blazers'
        dk_team_abbr = 'Por'
    elif team_id == 'SAS': 
        team_name = 'San Antonio Spurs'
        dk_team_abbr = 'SA'
    elif team_id == 'SAC': 
        team_name = 'Sacramento Kings'
        dk_team_abbr = 'Sac'
    elif team_id == 'TOR': 
        team_name = 'Toronto Raptors'
        dk_team_abbr = 'Tor'
    elif team_id == 'UTA': 
        team_name = 'Utah Jazz'
        dk_team_abbr = 'Uta'
    elif team_id == 'WAS': 
        team_name = 'Washington Wizards'
        dk_team_abbr = 'Was'

    url = 'http://www.basketball-reference.com/teams/' + team_id + '/' + str(season) + '.html'
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")
    
    for tr in soup('table')[0].findAll('tr'):
        if tr.th.get('class',None)[0] == 'center':
            for td in tr.findAll('td'):
                if td.get('data-stat',None) == 'player':
                    player_id = td.get('data-append-csv',None)
                    player_name = td.text
                    player_name_strip = player_name.upper().replace('-','').replace('.','').replace("'","").replace(',','').replace('JR','').replace('SR','').strip()
                elif td.get('data-stat',None) == 'pos':
                    position = td.text
            player_insert = (player_id, player_name, player_name_strip, position, team_id, team_name, dk_team_abbr)
            cur.execute('INSERT INTO players VALUES(?' + ',?'*6 + ')',player_insert)
con.commit()
con.close()


# In[ ]:



