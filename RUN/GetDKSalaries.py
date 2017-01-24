
# coding: utf-8

# In[2]:

import sqlite3
import fileinput, urllib
import time, datetime
from bs4 import BeautifulSoup

con = sqlite3.connect('C:\\NBA\\nba.db')
cur = con.cursor()

cur.execute('DROP TABLE IF EXISTS dk_salaries')
cur.execute('''CREATE TABLE dk_salaries
            (
             player_name TEXT
            ,player_name_strip TEXT
            ,position TEXT
            ,salary INTEGER
            ,dk_team_abbr TEXT
            ,projected_dk_score REAL
            ,adjusted_dk_score REAL
            ,multiplier REAL
            ,adjusted_multiplier REAL
            )''')

sals = 'C:\\NBA\\DKSalaries.csv'

projected_dk_score = -1
adjusted_dk_score = -1

multiplier = -1
adj_multiplier = -1

for line in fileinput.input(sals):
    if fileinput.lineno() > 1:
        line = line.replace('"','')
        line = line.split(',')
        pos = line[0].split('/')
        for p in pos:
            player_name = line[1]
            player_name_strip = player_name.upper().replace('-','').replace('.','').replace("'","").replace(',','').replace('JR','').replace('SR','').strip()
            position = p
            salary = line[2]
            dk_team_abbr = line[5].strip()
            dk_insert = (player_name, player_name_strip, position, salary, dk_team_abbr, projected_dk_score,adjusted_dk_score,multiplier,adj_multiplier)
            cur.execute('INSERT INTO dk_salaries VALUES(?' + ',?'*8 + ')',dk_insert)
        if 'PG' in pos:
            position = 'G'
            dk_insert = (player_name, player_name_strip, position, salary, dk_team_abbr, projected_dk_score,adjusted_dk_score,multiplier,adj_multiplier)
            cur.execute('INSERT INTO dk_salaries VALUES(?' + ',?'*8 + ')',dk_insert)
        elif 'SG' in pos:
            position = 'G'
            dk_insert = (player_name, player_name_strip, position, salary, dk_team_abbr, projected_dk_score,adjusted_dk_score,multiplier,adj_multiplier)
            cur.execute('INSERT INTO dk_salaries VALUES(?' + ',?'*8 + ')',dk_insert)
        if 'PF' in pos:
            position = 'F'
            dk_insert = (player_name, player_name_strip, position, salary, dk_team_abbr, projected_dk_score,adjusted_dk_score,multiplier,adj_multiplier)
            cur.execute('INSERT INTO dk_salaries VALUES(?' + ',?'*8 + ')',dk_insert)
        elif 'SF' in pos:
            position = 'F'
            dk_insert = (player_name, player_name_strip, position, salary, dk_team_abbr, projected_dk_score,adjusted_dk_score,multiplier,adj_multiplier)
            cur.execute('INSERT INTO dk_salaries VALUES(?' + ',?'*8 + ')',dk_insert)
fileinput.close()
con.commit()

# delete inactive players
url = 'http://www.rotowire.com/basketball/nba_lineups.htm'

html = urllib.urlopen(url).read()
soup = BeautifulSoup(html, "lxml")

inactive_players = []
for div in soup.findAll('div'):
    if div.text[:8].upper() == 'INJURIES':
        for d in div.findAll('div'):
            if d.get('class', None) != None:
                if d.get('class', None)[0] in ('dlineups-vplayer','dlineups-hplayer'):
                    url2 = 'http://www.rotowire.com' +  d.a.get('href', None)
                    html2 = urllib.urlopen(url2).read()
                    soup2 = BeautifulSoup(html2, "lxml")
                    name_split = soup2('head')[0].findAll('title')[0].text.split(' Fantasy Stats |')
                    pname = name_split[0]
                    inactive_players.append(pname.upper().replace('-','').replace('.','').replace("'","").replace(',','').replace('JR','').replace('SR','').strip())

for inactive_player in inactive_players:
    cur.execute("DELETE FROM dk_salaries WHERE player_name_strip = '" + inactive_player + "'")
    con.commit()
con.close()


# In[ ]:



