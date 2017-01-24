
# coding: utf-8

# In[1]:

from sklearn.preprocessing import MinMaxScaler
import numpy as np
from sklearn import neighbors
import sqlite3
import sys

def predict_knn(player,stat,sample,k):
    
    sample = np.asarray(sample)

    knnclf = neighbors.KNeighborsClassifier(k, weights='distance')
    
    # normalize the train and test data based on the training data with min-max normalization
    player_records = []
    cur = con.cursor()
    cur.execute("SELECT * FROM records WHERE player_id = '" + player + "'")
    for record in cur:
        record = record[9:] # get rid of target attributes
        player_records.append(record)
    
    # convert to NumPy array to be passed into minmax scaler
    player_records = np.asarray(player_records)
    
    # scale the training data
    min_max_scaler = MinMaxScaler().fit(player_records)
    train_norm = min_max_scaler.transform(player_records)
    sample_norm = min_max_scaler.transform(sample)
    
    # get the target attribute
    target_list = []
    if stat == 'rebounds': stat = 'total_rebounds'
    if stat == 'made_threes': stat = 'made_three_pts'
    cur.execute("SELECT " + stat + " FROM records WHERE player_id = '" + player + "'")
    for record in cur:
        target_list.append(record)
        
    target_array = np.asarray(target_list)
    
    # convert targets to strings 
    targets_str = ["%.0f" % tar for tar in target_array]
    
    knnclf.fit(train_norm, targets_str)
    knnpreds_test = knnclf.predict(sample_norm)
    return knnpreds_test[0]


# In[1]:

from sklearn import tree
import sqlite3

def predict_decisiontree(player,stat,sample,m):
    sample = np.asarray(sample)
    
    player_records = []
    cur = con.cursor()
    cur.execute("SELECT * FROM records WHERE player_id = '" + player + "'")
    for record in cur:
        record = record[9:] # get rid of target attributes
        player_records.append(record)
        
    # convert to NumPy array
    player_records = np.asarray(player_records)
    
    # get the target attribute
    target_list = []
    if stat == 'rebounds': stat = 'total_rebounds'
    if stat == 'made_threes': stat = 'made_three_pts'
    cur.execute("SELECT " + stat + " FROM records WHERE player_id = '" + player + "'")
    for record in cur:
        target_list.append(record)
        
    target_array = np.asarray(target_list)
    
    # convert targets to strings 
    targets_str = ["%.0f" % tar for tar in target_array]
    
    
    treeclf = tree.DecisionTreeClassifier(criterion='entropy', min_samples_split=m)
    treeclf = treeclf.fit(player_records, targets_str)
    
    treepreds_test = treeclf.predict(sample)
    

    return treepreds_test[0]            


# In[ ]:

from sklearn import naive_bayes
import sqlite3

def predict_naivebayes(player,stat,sample):
    sample = np.asarray(sample)
    
    player_records = []
    cur = con.cursor()
    cur.execute("SELECT * FROM records WHERE player_id = '" + player + "'")
    for record in cur:
        record = record[9:] # get rid of target attributes
        player_records.append(record)
        
    # convert to NumPy array
    player_records = np.asarray(player_records)
    
    # get the target attribute
    target_list = []
    if stat == 'rebounds': stat = 'total_rebounds'
    if stat == 'made_threes': stat = 'made_three_pts'
    cur.execute("SELECT " + stat + " FROM records WHERE player_id = '" + player + "'")
    for record in cur:
        target_list.append(record)
        
    target_array = np.asarray(target_list)
    
    # convert targets to strings 
    targets_str = ["%.0f" % tar for tar in target_array]
    
    nbclf = naive_bayes.GaussianNB()
    nbclf = nbclf.fit(player_records, targets_str)
    
    nbpreds_test = nbclf.predict(sample)

    return nbpreds_test[0]    


# In[ ]:

from sklearn.ensemble import RandomForestClassifier
import sqlite3

def predict_randomforest(player,stat,sample):
    sample = np.asarray(sample)
    
    player_records = []
    cur = con.cursor()
    cur.execute("SELECT * FROM records WHERE player_id = '" + player + "'")
    for record in cur:
        record = record[9:] # get rid of target attributes
        player_records.append(record)
        
    # convert to NumPy array
    player_records = np.asarray(player_records)
    
    # get the target attribute
    target_list = []
    if stat == 'rebounds': stat = 'total_rebounds'
    if stat == 'made_threes': stat = 'made_three_pts'
    cur.execute("SELECT " + stat + " FROM records WHERE player_id = '" + player + "'")
    for record in cur:
        target_list.append(record)
        
    target_array = np.asarray(target_list)
    
    # convert targets to strings 
    targets_str = ["%.0f" % tar for tar in target_array]
    
    rf = RandomForestClassifier()
    rf = rf.fit(player_records, targets_str)
    rf_test = rf.predict(sample)
    

    return rf_test[0]    


# In[ ]:

from sklearn.ensemble import RandomForestClassifier
import sqlite3

def predict_adaboost(player,stat,sample):
    sample = np.asarray(sample)
    
    player_records = []
    cur = con.cursor()
    cur.execute("SELECT * FROM records WHERE player_id = '" + player + "'")
    for record in cur:
        record = record[9:] # get rid of target attributes
        player_records.append(record)
        
    # convert to NumPy array
    player_records = np.asarray(player_records)
    
    # get the target attribute
    target_list = []
    if stat == 'rebounds': stat = 'total_rebounds'
    if stat == 'made_threes': stat = 'made_three_pts'
    cur.execute("SELECT " + stat + " FROM records WHERE player_id = '" + player + "'")
    for record in cur:
        target_list.append(record)
        
    target_array = np.asarray(target_list)
    
    # convert targets to strings 
    targets_str = ["%.0f" % tar for tar in target_array]
    
    ab = AdaBoostClassifier()
    ab = ab.fit(player_records, targets_str)
    ab_test = ab.predict(sample)
    

    return ab_test[0]    


# In[ ]:

from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet, SGDRegressor
from sklearn import feature_selection


def predict_linreg(player,stat,sample,op_perc):
    
    sample = np.asarray(sample)
    
    linreg = LinearRegression()
    
    # normalize the train and test data based on the training data with min-max normalization
    player_records = []
    cur = con.cursor()
    cur.execute("SELECT * FROM records WHERE player_id = '" + player + "'")
    for record in cur:
        record = record[9:] # get rid of target attributes
        player_records.append(record)
    
    # convert to NumPy array to be passed into minmax scaler
    player_records = np.asarray(player_records)
    
    # scale the training data
    min_max_scaler = MinMaxScaler().fit(player_records)
    train_norm = min_max_scaler.transform(player_records)
    sample_norm = min_max_scaler.transform(sample)
    
    # get the target attribute
    target_list = []
    if stat == 'rebounds': stat = 'total_rebounds'
    if stat == 'made_threes': stat = 'made_three_pts'
    cur.execute("SELECT " + stat + " FROM records WHERE player_id = '" + player + "'")
    for record in cur:
        target_list.append(record)
        
    target_array = np.asarray(target_list)
    
    fs = feature_selection.SelectPercentile(feature_selection.f_regression, percentile=op_perc)
    x_train_fs = fs.fit_transform(train_norm, target_array)

    x_train_fs = fs.fit_transform(train_norm, target_array)
    sample_fs = sample_norm[fs.get_support()]
    linreg.fit(x_train_fs,target_array)

    return round(linreg.predict(sample_fs)[0])


# In[12]:

import urllib, sqlite3
import time, datetime
from bs4 import BeautifulSoup
import numpy as np
import sys

import warnings
warnings.filterwarnings('ignore') # will need to look into this later -- getting a warning on my knn predictions


# connect to the database
con = sqlite3.connect('C:\\NBA\\nba.db') # create database in the directory where the .py file is saved
cur = con.cursor()
cur2 = con.cursor()
cur3 = con.cursor()
cur4 = con.cursor()


today = datetime.date.today() 
#today = datetime.datetime.strptime('2016-11-16', '%Y-%m-%d')

if today.month > 9:
    season = today.year + 1
else:
    season = today.year

todays_samples_list = [] # combined player and team

cur.execute("SELECT DISTINCT team, opponent FROM schedules WHERE game_date = '" + today.strftime("%Y-%m-%d") + "'")
for team in cur:
     # get the team records
    query = open('C:\\NBA\\SQL\\team_template.sql','r')
    query = query.read()

    query_new = query.replace('<team>',team[1]) # insert the opponent
    query_new = query_new.replace('<season>',str(season))
    query_new = query_new.replace('<game_date>',today.strftime("%Y-%m-%d"))
    cur3.execute(query_new)
    for t in cur3:
        t = list(t)
        opp_team_arr = t
    
    # get the player records
    cur2.execute("SELECT DISTINCT player_id FROM games WHERE team = '" + team[0] + "' AND season = " + str(season))
    for p in cur2: # get the player stats going into the game
        query = open('C:\\NBA\\SQL\\player_template.sql','r')
        query = query.read()

        query_new = query.replace('<player>',p[0])
        query_new = query_new.replace('<season>',str(season))
        query_new = query_new.replace('<game_date>',today.strftime("%Y-%m-%d"))
        cur3.execute(query_new)
        for row in cur3:
            row = list(row)
            player_arr = row
            combine_arr = player_arr + opp_team_arr
            combine_arr = [p[0]] + combine_arr
            combine_arr.append(season)
            todays_samples_list.append(combine_arr)
            

prediction_list = []
for sample in todays_samples_list:
    for stat in ['assists','rebounds','points','steals','blocks','turnovers','made_threes']:
        query = open('C:\\NBA\\SQL\\find_model.sql','r')
        query = query.read()
        
        query_new = query.replace('<player_id>',sample[0])
        query_new = query_new.replace('<stat>',stat)
        query_new = query_new.replace('<model_date>',today.strftime("%Y-%m-%d"))
        cur4.execute(query_new)
        
        for c in cur4:
            if c[0] == 'knn':
                pred_knn = predict_knn(sample[0],stat,sample[1:],int(c[1]))
                p = (sample[0],stat,pred_knn)
                p = list(p)
                p.append(today.strftime("%Y-%m-%d"))
                p.append('knn')
                p.append(c[2]) # mse
                p = tuple(p)
            elif c[0] == 'linreg':
                pred_linreg = predict_linreg(sample[0],stat,sample[1:],int(c[1]))
                p = (sample[0],stat,pred_linreg)
                p = list(p)
                p.append(today.strftime("%Y-%m-%d"))
                p.append('linreg')
                p.append(c[2]) # mse
                p = tuple(p)
            elif c[0] == 'decisiontree':
                pred_decisiontree = predict_decisiontree(sample[0],stat,sample[1:],int(c[1]))
                p = (sample[0],stat,pred_decisiontree)
                p = list(p)
                p.append(today.strftime("%Y-%m-%d"))
                p.append('decisiontree')
                p.append(c[2]) # mse
                p = tuple(p)
            elif c[0] == 'naivebayes':
                pred_naivebayes = predict_naivebayes(sample[0],stat,sample[1:])
                p = (sample[0],stat,pred_naivebayes)
                p = list(p)
                p.append(today.strftime("%Y-%m-%d"))
                p.append('naivebayes')
                p.append(c[2]) # mse
                p = tuple(p)
            elif c[0] == 'randomforest':
                pred_randomforest = predict_randomforest(sample[0],stat,sample[1:])
                p = (sample[0],stat,pred_randomforest)
                p = list(p)
                p.append(today.strftime("%Y-%m-%d"))
                p.append('randomforest')
                p.append(c[2]) # mse
                p = tuple(p)
            elif c[0] == 'adaboost':
                pred_adaboost = predict_adaboost(sample[0],stat,sample[1:])
                p = (sample[0],stat,pred_adaboost)
                p = list(p)
                p.append(today.strftime("%Y-%m-%d"))
                p.append('adaboost')
                p.append(c[2]) # mse
                p = tuple(p)
                
            prediction_list.append(p)

for pred in prediction_list:
    cur.execute('INSERT INTO predictions VALUES(?' + ',?'*5 + ')',pred)
con.commit()


