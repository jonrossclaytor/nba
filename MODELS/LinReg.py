
# coding: utf-8

# In[ ]:

from sklearn import cross_validation
import math
from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet, SGDRegressor
from sklearn import feature_selection

def ftr_sel(x,y,model):
    
    model.fit(x,y)
    percentiles = range(5, 100, 5)
    results = []
    for i in range(1, 100, 5):
        fs = feature_selection.SelectPercentile(feature_selection.f_regression, percentile=i)
        X_train_fs = fs.fit_transform(x, y)
        if X_train_fs != []:
            scores = cross_validation.cross_val_score(model, X_train_fs, y, cv=5, scoring='mean_absolute_error')
            results = np.append(results, scores.mean())
        
    optimal_percentil = max(np.where(results == results.max())[0])
    op_perc = percentiles[optimal_percentil]

    #optimal_num_features = int(math.floor(percentiles[optimal_percentil]*len(x.columns)/100))
    
    return op_perc


# In[11]:

import sqlite3
import numpy as np
import sys

from sklearn.preprocessing import MinMaxScaler
from sklearn import neighbors
from sklearn.cross_validation import train_test_split

from sklearn import cross_validation
from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet, SGDRegressor
from sklearn import feature_selection

import time, datetime

import math
import warnings
warnings.filterwarnings('ignore')

today = datetime.date.today() 
today = today.strftime("%Y-%m-%d")

con = sqlite3.connect('C:\\NBA\\nba.db')
cur = con.cursor()
cur2 = con.cursor()
cur3 = con.cursor()

player_list = []
#cur.execute("""select DISTINCT player_id from records where player_id = 'ayongu01'""")

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

    '''
    # define categorical targets
    assists_str = ["%.0f" % asst for asst in assists]
    rebounds_str = ["%.0f" % reb for reb in rebounds]
    points_str = ["%.0f" % point for point in points]
    steals_str = ["%.0f" % steal for steal in steals]
    blocks_str = ["%.0f" % block for block in blocks]
    turnovers_str = ["%.0f" % turnover for turnover in turnovers]
    made_threes_str = ["%.0f" % made_three for made_three in made_threes]
    '''
    
    # drop targets from array
    player_records = np.delete(player_records, 0, 1) # remove assists
    player_records = np.delete(player_records, 0, 1) # remove rebounds
    player_records = np.delete(player_records, 0, 1) # remove points
    player_records = np.delete(player_records, 0, 1) # remove steals
    player_records = np.delete(player_records, 0, 1) # remove blocks
    player_records = np.delete(player_records, 0, 1) # remove turnovers
    player_records = np.delete(player_records, 0, 1) # remove made_three

    for target in [assists,rebounds,points,steals,blocks,turnovers,made_threes]:
        if np.array_equal(target, assists):
            stat = 'assists'
        elif np.array_equal(target, rebounds):
            stat = 'rebounds'
        elif np.array_equal(target, points):
            stat = 'points'
        elif np.array_equal(target, steals):
            stat = 'steals'
        elif np.array_equal(target, blocks):
            stat = 'blocks'
        elif np.array_equal(target, turnovers):
            stat = 'turnovers'
        elif np.array_equal(target, made_threes):
            stat = 'made_threes'

        # normalize the train and test data based on the training data with min-max normalization
        '''
        min_max_scaler = MinMaxScaler().fit(train)
        train_norm = min_max_scaler.transform(train)
        test_norm = min_max_scaler.transform(test)
        '''

        linreg = LinearRegression()
        op_perc = ftr_sel(player_records,target,linreg) 
            
        fs = feature_selection.SelectPercentile(feature_selection.f_regression, percentile=op_perc)
        x_train_fs = fs.fit_transform(player_records, target)
        if x_train_fs != []:
            linreg.fit(x_train_fs,target)

            errors = cross_validation.cross_val_score(linreg, x_train_fs, target, cv=5, scoring='mean_absolute_error')
            MSE = errors.mean()*-1

            result = [p,today,'linreg',stat,MSE,op_perc,'Optimal Features']
            result = tuple(result)
            cur3.execute('INSERT INTO model_results VALUES(?' + ',?'*6 + ')',result)
    con.commit()
        
con.close()

