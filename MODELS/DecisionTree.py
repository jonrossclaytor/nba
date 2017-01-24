
# coding: utf-8

# In[47]:

def find_min_samples_split(data_test,data_train,target_test,target_train,min_range):
    minMSE = -1
    for m in min_range:
        if m <= data_test.shape[0]: # make sure there are enough test samples available
            treeclf = tree.DecisionTreeClassifier(criterion='entropy', min_samples_split=m)
            treeclf = treeclf.fit(data_train, target_train)

            treepreds_test = treeclf.predict(data_test)
            # convert the predictions and targets to integers so that MSE can be calculated
            target_test = np.asarray(target_test)
            target_test_float = target_test.astype(np.float)
            treepreds_test_float = treepreds_test.astype(np.float)

            MSE = math.sqrt(sum((treepreds_test_float - target_test_float)**2)) / treepreds_test_float.shape[0]

            if minMSE == -1:
                minMSE = MSE
                min_m = m
            elif MSE < minMSE:
                minMSE = MSE
                min_m = m
    
    return minMSE, min_m


# In[50]:

import sqlite3
import numpy as np
import time, datetime

from sklearn.preprocessing import MinMaxScaler
from sklearn import neighbors, tree, naive_bayes
from sklearn.cross_validation import train_test_split
import math



today = datetime.date.today() 
today = today.strftime("%Y-%m-%d")

con = sqlite3.connect('C:\\NBA\\nba.db')
cur = con.cursor()
cur2 = con.cursor()
cur3 = con.cursor()

player_list = []
cur.execute('''
            SELECT DISTINCT player_id
            FROM 
            (
            SELECT player_id, COUNT(*)
            FROM records
            GROUP BY player_id
            HAVING COUNT(*) > 4
            ) tab       
            ''')
for player in cur:
    player_list.append(player[0])

for p in player_list:
    cur2.execute("SELECT * FROM records WHERE player_id = '" + p + "'")

    player_records = [] # initiate empty list to eventually hold the palyer records as a numpy array

    for record in cur2:
        record = list(record)
        record = record[2:] # omit the player_id and game_id
        player_records.append(record)

    player_records = np.asarray(player_records)

    # define numerical tagets
    assists = player_records[:,0] # first column
    rebounds = player_records[:,1]
    points = player_records[:,2]
    steals = player_records[:,3]
    blocks = player_records[:,4]
    turnovers = player_records[:,5]
    made_threes = player_records[:,6]


    # define categorical targets
    assists_str = ["%.0f" % asst for asst in assists]
    rebounds_str = ["%.0f" % reb for reb in rebounds]
    points_str = ["%.0f" % point for point in points]
    steals_str = ["%.0f" % steal for steal in steals]
    blocks_str = ["%.0f" % block for block in blocks]
    turnovers_str = ["%.0f" % turnover for turnover in turnovers]
    made_threes_str = ["%.0f" % made_three for made_three in made_threes]

    # drop targets from array
    player_records = np.delete(player_records, 0, 1) # remove assists
    player_records = np.delete(player_records, 0, 1) # remove rebounds
    player_records = np.delete(player_records, 0, 1) # remove points
    player_records = np.delete(player_records, 0, 1) # remove steals
    player_records = np.delete(player_records, 0, 1) # remove blocks
    player_records = np.delete(player_records, 0, 1) # remove turnovers
    player_records = np.delete(player_records, 0, 1) # remove made_three

    for target in [assists_str,rebounds_str,points_str,steals_str,blocks_str,turnovers_str,made_threes_str]:
        if np.array_equal(target, assists_str):
            stat = 'assists'
        elif np.array_equal(target, rebounds_str):
            stat = 'rebounds'
        elif np.array_equal(target, points_str):
            stat = 'points'
        elif np.array_equal(target, steals_str):
            stat = 'steals'
        elif np.array_equal(target, blocks_str):
            stat = 'blocks'
        elif np.array_equal(target, turnovers_str):
            stat = 'turnovers'
        elif np.array_equal(target, made_threes_str):
            stat = 'made_threes'
            
        # split the data into randomized 80% 20% training and test split
        train, test, target_train, target_test = train_test_split(player_records, target, test_size=0.2, random_state=33)
        
        rng = np.linspace(1,train.shape[0],20)
        rng = list(rng.astype(int))
        MSE, m =  find_min_samples_split(test,train,target_test,target_train,rng) # 20 integers betweeen 1 and size of training data
        

        result = [p,today,'decisiontree',stat,MSE,m,'Minimum Samples for a Split']
        result = tuple(result)
        result = tuple(result)
        cur3.execute('INSERT INTO model_results VALUES(?' + ',?'*6 + ')',result)
    con.commit()
con.close()


# In[ ]:



