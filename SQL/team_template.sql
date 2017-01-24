
SELECT 
 season.missed_field_goal_pg_season AS missed_field_goal_pg_season
,season.missed_three_pointers_pg_season AS missed_three_pointers_pg_season
,season.missed_free_throws_pg_season AS missed_free_throws_pg_season
,season.missed_free_throws_pg_season AS offensive_rebounds_pg_season 
,season.defensive_rebounds_pg_season AS defensive_rebounds_pg_season
,season.assists_pg_season AS assists_pg_season
,season.steals_pg_season AS steals_pg_season
,season.blocks_pg_season AS blocks_pg_season
,season.turnovers_pg_season AS turnovers_pg_season
,season.personal_fouls_pg_season AS personal_fouls_pg_season
,five_games.missed_field_goal_pg_5games AS missed_field_goal_pg_5games
,five_games.missed_three_pointers_pg_5games AS missed_three_pointers_pg_5games
,five_games.missed_free_throws_pg_5games AS missed_free_throws_pg_5games
,five_games.offensive_rebounds_pg_5games AS offensive_rebounds_pg_5games
,five_games.defensive_rebounds_pg_5games AS defensive_rebounds_pg_5games
,five_games.assists_pg_5games AS assists_pg_5games
,five_games.steals_pg_5games AS steals_pg_5games
,five_games.blocks_pg_5games AS blocks_pg_5games
,five_games.turnovers_pg_5games AS turnovers_pg_5games
,five_games.personal_fouls_pg_5games AS personal_fouls_pg_5games
,twoweeks.missed_field_goal_pg_twoweeks AS missed_field_goal_pg_twoweeks
,twoweeks.missed_three_pointers_pg_twoweeks AS missed_three_pointers_pg_twoweeks
,twoweeks.missed_free_throws_pg_twoweeks AS missed_free_throws_pg_twoweeks
,twoweeks.offensive_rebounds_pg_twoweeks AS offensive_rebounds_pg_twoweeks
,twoweeks.defensive_rebounds_pg_twoweeks AS defensive_rebounds_pg_twoweeks
,twoweeks.assists_pg_twoweeks AS assists_pg_twoweeks
,twoweeks.steals_pg_twoweeks AS steals_pg_twoweeks
,twoweeks.blocks_pg_twoweeks AS blocks_pg_twoweeks
,twoweeks.turnovers_pg_twoweeks AS turnovers_pg_twoweeks
,twoweeks.personal_fouls_pg_twoweeks AS personal_fouls_pg_twoweeks

FROM
(
SELECT 
 g.team
,(SUM(g.field_goal_attempts) - SUM(g.field_goals))*1.0 / season_games.games*1.0 AS missed_field_goal_pg_season
,(SUM(g.three_point_attempts) - SUM(g.three_pointers))*1.0 / season_games.games*1.0 AS missed_three_pointers_pg_season
,(SUM(g.free_throw_attempts) - SUM(g.free_throws))*1.0 / season_games.games*1.0 AS missed_free_throws_pg_season
,SUM(g.offensive_rebounds)*1.0 / season_games.games*1.0 AS offensive_rebounds_pg_season 
,SUM(g.defensive_rebounds)*1.0 / season_games.games*1.0 AS defensive_rebounds_pg_season
,SUM(g.assists)*1.0 / season_games.games*1.0 AS assists_pg_season
,SUM(g.steals)*1.0 / season_games.games*1.0 AS steals_pg_season
,SUM(g.blocks)*1.0 / season_games.games*1.0 AS blocks_pg_season
,SUM(g.turnovers)*1.0 / season_games.games*1.0 AS turnovers_pg_season
,SUM(g.personal_fouls)*1.0 / season_games.games*1.0 AS personal_fouls_pg_season

FROM games g
JOIN 
(
SELECT g.team, COUNT(DISTINCT g.game_id) AS games 
FROM games g
WHERE g.team = '<team>' 
AND g.season = '<season>' 
AND g.game_date < '<game_date>'
) season_games ON season_games.team = g.team

WHERE g.team = '<team>' 
AND g.season = '<season>' 
AND g.game_date < '<game_date>'
GROUP BY g.team
) season

-- SUB QUERY FOR THE PAST 5 GAMES
JOIN 
(
SELECT  
 g.team
,(SUM(g.field_goal_attempts) - SUM(g.field_goals))*1.0 / fivegames.games*1.0 AS missed_field_goal_pg_5games
,(SUM(g.three_point_attempts) - SUM(g.three_pointers))*1.0 / fivegames.games*1.0 AS missed_three_pointers_pg_5games
,(SUM(g.free_throw_attempts) - SUM(g.free_throws))*1.0 / fivegames.games*1.0 AS missed_free_throws_pg_5games
,SUM(g.offensive_rebounds)*1.0 / fivegames.games*1.0 AS offensive_rebounds_pg_5games
,SUM(g.defensive_rebounds)*1.0 / fivegames.games*1.0 AS defensive_rebounds_pg_5games
,SUM(g.assists)*1.0 / fivegames.games*1.0 AS assists_pg_5games
,SUM(g.steals)*1.0 / fivegames.games*1.0 AS steals_pg_5games
,SUM(g.blocks)*1.0 / fivegames.games*1.0 AS blocks_pg_5games
,SUM(g.turnovers)*1.0 / fivegames.games*1.0 AS turnovers_pg_5games
,SUM(g.personal_fouls)*1.0 / fivegames.games*1.0 AS personal_fouls_pg_5games

FROM games g
JOIN
(
SELECT team, MIN(COUNT(DISTINCT game_id),5) AS games
FROM games
WHERE team = '<team>'
AND season = '<season>'
AND game_date < '<game_date>'
) fivegames ON fivegames.team = g.team

JOIN
(
SELECT DISTINCT game_id
FROM games
WHERE team = '<team>'
AND season = '<season>' 
AND game_date < '<game_date>'
ORDER BY game_id DESC
LIMIT 5
) top5 ON g.game_id = top5.game_id

WHERE g.team = '<team>' 
AND g.season = '<season>' 
AND g.game_date < '<game_date>'
) five_games ON five_games.team = season.team


-- SUB QUERY FOR GAMES IN THE PAST TWO WEEKS
JOIN
(
SELECT 
 g.team
,(SUM(g.field_goal_attempts) - SUM(g.field_goals))*1.0 / twoweeks.games*1.0 AS missed_field_goal_pg_twoweeks
,(SUM(g.three_point_attempts) - SUM(g.three_pointers))*1.0 / twoweeks.games*1.0 AS missed_three_pointers_pg_twoweeks
,(SUM(g.free_throw_attempts) - SUM(g.free_throws))*1.0 / twoweeks.games*1.0 AS missed_free_throws_pg_twoweeks
,SUM(g.offensive_rebounds)*1.0 / twoweeks.games*1.0 AS offensive_rebounds_pg_twoweeks
,SUM(g.defensive_rebounds)*1.0 / twoweeks.games*1.0 AS defensive_rebounds_pg_twoweeks
,SUM(g.assists)*1.0 / twoweeks.games*1.0 AS assists_pg_twoweeks
,SUM(g.steals)*1.0 / twoweeks.games*1.0 AS steals_pg_twoweeks
,SUM(g.blocks)*1.0 / twoweeks.games*1.0 AS blocks_pg_twoweeks
,SUM(g.turnovers)*1.0 / twoweeks.games*1.0 AS turnovers_pg_twoweeks
,SUM(g.personal_fouls)*1.0 / twoweeks.games*1.0 AS personal_fouls_pg_twoweeks
FROM games g
JOIN
(
SELECT team, COUNT(DISTINCT game_id) games
FROM games
WHERE team = '<team>' 
AND game_date BETWEEN DATE('<game_date>','-14 day') AND '<game_date>'
) twoweeks ON twoweeks.team = g.team
WHERE g.team = '<team>' 
AND g.season = '<season>' 
AND g.game_id IN
(
SELECT DISTINCT game_id
FROM games
WHERE team = '<team>' 
AND game_date BETWEEN DATE('<game_date>','-14 day') AND '<game_date>'
)
) twoweeks ON twoweeks.team = season.team