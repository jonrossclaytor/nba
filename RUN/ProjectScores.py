
# coding: utf-8

# In[9]:

import time, datetime, sqlite3

con = sqlite3.connect('C:\\NBA\\nba.db')
cur = con.cursor()
cur2 = con.cursor()

today = datetime.date.today() 

player_list = []

cur.execute("SELECT DISTINCT player_id FROM predictions WHERE date = '" + today.strftime("%Y-%m-%d") + "'")

for player in cur:
    player_list.append(player[0])
    
dk_pts_dict = {}
dk_adj_pts_dict = {}
    
for p in player_list:
    dk_points = 0
    dk_adj_points = 0
    
    dubs = 0
    adj_dubs = 0
    cur.execute("SELECT * FROM predictions WHERE player_id = '" + p + "' AND date = '" + today.strftime("%Y-%m-%d") + "'")
    for row in cur:
        if row[1] == 'assists':
            dk_points = dk_points + (row[2] * 1.5)
            dk_adj_points = dk_adj_points + ((row[2] - row[5]) * 1.5)
            if row[2] > 9: dubs = dubs + 1
            if (row[2] - row[5]) > 9:  adj_dubs = adj_dubs + 1
        elif row[1] == 'rebounds':
            dk_points = dk_points + (row[2] * 1.25)
            dk_adj_points = dk_adj_points + ((row[2] - row[5]) * 1.25)
            if row[2] > 9: dubs = dubs + 1
            if (row[2] - row[5]) > 9:  adj_dubs = adj_dubs + 1
        elif row[1] == 'points':
            dk_points = dk_points + row[2]
            dk_adj_points = dk_adj_points + (row[2] - row[5])
            if row[2] > 9: dubs = dubs + 1
            if (row[2] - row[5]) > 9:  adj_dubs = adj_dubs + 1
        elif row[1] == 'steals':
            dk_points = dk_points + (row[2] * 2)
            dk_adj_points = dk_adj_points + ((row[2] - row[5]) * 2)
            if row[2] > 9: dubs = dubs + 1
            if (row[2] - row[5]) > 9:  adj_dubs = adj_dubs + 1
        elif row[1] == 'blocks':
            dk_points = dk_points + (row[2] * 2)
            dk_adj_points = dk_adj_points + ((row[2] - row[5]) * 2)
            if row[2] > 9: dubs = dubs + 1
            if (row[2] - row[5]) > 9:  adj_dubs = adj_dubs + 1
        elif row[1] == 'turnovers':
            dk_points = dk_points + (row[2] * -.5)
            dk_adj_points = dk_adj_points + ((row[2] + row[5]) * -.5)
        elif row[1] == 'made_threes':
            dk_points = dk_points + (row[2] * .5)
            dk_adj_points = dk_adj_points + ((row[2] - row[5]) * .5)
    if dubs > 2:
        dk_points = dk_points + 3 # triple-double
    elif dubs > 1:
        dk_points = dk_points + 1.5 # double-double
    if adj_dubs > 2:
        dk_adj_points = dk_adj_points + 3 # triple-double
    elif adj_dubs > 1:
        dk_adj_points = dk_adj_points + 1.5 # double-double
    
    dk_pts_dict[p] = dk_points
    dk_adj_pts_dict[p] = dk_adj_points
    
for p in dk_pts_dict:
    cur.execute("SELECT player_name, dk_team_abbr FROM players WHERE player_id = '" + p + "'")
    for rec in cur:
        cur2.execute('''UPDATE dk_salaries
                        SET projected_dk_score = ''' + str(dk_pts_dict[p]) + '''
                        WHERE player_name_strip = (SELECT player_name_strip FROM players WHERE player_id = "''' + p + '''") 
                        AND  dk_team_abbr = (SELECT dk_team_abbr FROM players where player_id = "''' + p + '''") 
                     ''')
        cur2.execute('''UPDATE dk_salaries
                        SET adjusted_dk_score = ''' + str(dk_adj_pts_dict[p]) + '''
                        WHERE player_name_strip = (SELECT player_name_strip FROM players WHERE player_id = "''' + p + '''") 
                        AND  dk_team_abbr = (SELECT dk_team_abbr FROM players where player_id = "''' + p + '''") 
                     ''')

cur2.execute('''UPDATE dk_salaries
                SET multiplier = (projected_dk_score / salary) * 1000
             ''')

cur2.execute('''UPDATE dk_salaries
                SET adjusted_multiplier = (adjusted_dk_score / salary) * 1000
             ''')

con.commit()
con.close()


# In[ ]:



