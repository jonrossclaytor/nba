# nba
An application that scrapes using machine learning to construct an optimal DraftKings lineup

Web scraping is first used to pull VBA box scores for the past 5 seasons.  Next an ETL process generates team level and player level stats going into each game.  Machine learning algorithms using the scikitlearn library are then used to build models on the data to predict key metrics including points, rebounds, and assists where the most accurate model for each player and statistic is selected to make a prediction for today's game.

Last, salaries from DraftKings are considered and an optimal lineup is built based on the predictions made for each player. 
