
# coding: utf-8

# In[ ]:

def find_k(data_test,data_train,target_test,target_train,k_range):
    minMSE = -1
    for k in k_range:
        if k <= data_test.shape[0]: # make sure there are enough test samples available
            knnclf = neighbors.KNeighborsClassifier(k, weights='distance')
            knnclf.fit(data_train, target_train)

            knnpreds_test = knnclf.predict(data_test)
            # convert the predictions and targets to integers so that MSE can be calculated
            target_test = np.asarray(target_test)
            target_test_float = target_test.astype(np.float)
            knnpreds_test_float = knnpreds_test.astype(np.float)

            MSE = math.sqrt(sum((knnpreds_test_float - target_test_float)**2)) / knnpreds_test_float.shape[0]
            if minMSE == -1:
                minMSE = MSE
                return_k = k
            elif MSE < minMSE:
                minMSE = MSE
                return_k = k
    
    return minMSE, return_k


# In[5]:

import sqlite3
import numpy as np
import time, datetime

from sklearn.preprocessing import MinMaxScaler
from sklearn import neighbors
from sklearn.cross_validation import train_test_split
import math

today = datetime.date.today() 
today = today.strftime("%Y-%m-%d")

con = sqlite3.connect('C:\\NBA\\nba.db')
cur = con.cursor()
cur2 = con.cursor()
cur3 = con.cursor()

"""
cur.execute('DROP TABLE IF EXISTS model_results')
cur.execute('''CREATE TABLE model_results
             (
                 player_id TEXT
                ,model_date TEXT
                ,model TEXT
                ,stat TEXT
                ,mse REAL
                ,params TEXT
                ,params_desc TEXT
             )''')
"""

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

        # normalize the train and test data based on the training data with min-max normalization
        min_max_scaler = MinMaxScaler().fit(train)
        train_norm = min_max_scaler.transform(train)
        test_norm = min_max_scaler.transform(test)

        MSE, k =  find_k(test_norm,train_norm,target_test,target_train,list(range(6))[1:]) # 1 through 5

        result = [p,today,'knn',stat,MSE,k,'K Neareast Neighbors']
        result = tuple(result)
        cur3.execute('INSERT INTO model_results VALUES(?' + ',?'*6 + ')',result)
    con.commit()
con.close()

