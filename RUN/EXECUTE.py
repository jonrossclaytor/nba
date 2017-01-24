import datetime

print 'started'
print datetime.datetime.now()
print

print 'getting players'
print datetime.datetime.now()
execfile("GetPlayers.py")
print

print 'getting yesterdays games'
print datetime.datetime.now()
execfile("GetGames.py")
print

print 'getting player stats'
print datetime.datetime.now()
execfile("GetPlayerStats.py")
print

print 'getting team stats'
print datetime.datetime.now()
execfile("GetTeamStats.py")
print

print 'getting individual records'
print datetime.datetime.now()
execfile("GetRecords.py")
print

print 'getting AdaBoost results'
print datetime.datetime.now()
execfile("C:\\NBA\\MODELS\\AdaBoost.py")
print

print 'getting Random Forest results'
print datetime.datetime.now()
execfile("C:\\NBA\\MODELS\\RandomForest.py")
print

print 'getting Naive Bayes results'
print datetime.datetime.now()
execfile("C:\\NBA\\MODELS\\NaiveBayes.py")
print

print 'getting Decision Tree results'
print datetime.datetime.now()
execfile("C:\\NBA\\MODELS\\DecisionTree.py")
print

print 'getting KNN results'
print datetime.datetime.now()
execfile("C:\\NBA\\MODELS\\KNN.py")
print

'''
print 'getting linear regression resuls'
print datetime.datetime.now()
execfile("C:\\NBA\\MODELS\\LinReg.py")
print
'''

print 'finding the best models and making predictions'
print datetime.datetime.now()
execfile("GetTodaysSamples.py")
print

print 'finished'
print datetime.datetime.now()