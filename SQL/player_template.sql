
SELECT 
 season.field_goal_attempts_pg_season AS field_goal_attempts_pg_season
,season.field_goals_pg_season AS field_goals_pg_season
,season.three_point_attempts_pg_season AS three_point_attempts_pg_season
,season.three_pointers_pg_season AS three_pointers_pg_season
,season.free_throw_attempts_pg_season AS free_throw_attempts_pg_season
,season.free_throws_pg_season AS free_throws_pg_season
,season.offensive_rebounds_pg_season AS offensive_rebounds_pg_season 
,season.defensive_rebounds_pg_season AS defensive_rebounds_pg_season
,season.assists_pg_season AS assists_pg_season
,season.steals_pg_season AS steals_pg_season
,season.blocks_pg_season AS blocks_pg_season
,season.turnovers_pg_season AS turnovers_pg_season
,season.personal_fouls_pg_season AS personal_fouls_pg_season
,season.points_pg_season AS points_pg_season
,season.minutes_pg_season AS minutes_pg_season
,five_games.field_goal_attempts_pg_5games AS field_goal_attempts_pg_5games
,five_games.field_goals_pg_5games AS field_goals_pg_5games
,five_games.three_point_attempts_pg_5games AS three_point_attempts_pg_5games
,five_games.three_pointers_pg_5games AS three_pointers_pg_5games
,five_games.free_throw_attempts_pg_5games AS free_throw_attempts_pg_5games
,five_games.free_throws_pg_5games AS free_throws_pg_5games
,five_games.offensive_rebounds_pg_5games AS offensive_rebounds_pg_5games
,five_games.defensive_rebounds_pg_5games AS defensive_rebounds_pg_5games
,five_games.assists_pg_5games AS assists_pg_5games
,five_games.steals_pg_5games AS steals_pg_5games
,five_games.blocks_pg_5games AS blocks_pg_5games
,five_games.turnovers_pg_5games AS turnovers_pg_5games
,five_games.personal_fouls_pg_5games AS personal_fouls_pg_5games
,five_games.points_pg_5games AS points_pg_5games
,five_games.minutes_pg_5games AS minutes_pg_5games
,twoweeks.field_goal_attempts_pg_twoweeks AS field_goal_attempts_pg_twoweeks
,twoweeks.field_goals_pg_twoweeks AS field_goals_pg_twoweeks
,twoweeks.three_point_attempts_pg_twoweeks AS three_point_attempts_pg_twoweeks
,twoweeks.three_pointers_pg_twoweeks AS three_pointers_pg_twoweeks
,twoweeks.free_throw_attempts_pg_twoweeks AS free_throw_attempts_pg_twoweeks
,twoweeks.free_throws_pg_twoweeks AS free_throws_pg_twoweeks
,twoweeks.offensive_rebounds_pg_twoweeks AS offensive_rebounds_pg_twoweeks
,twoweeks.defensive_rebounds_pg_twoweeks AS defensive_rebounds_pg_twoweeks
,twoweeks.assists_pg_twoweeks AS assists_pg_twoweeks
,twoweeks.steals_pg_twoweeks AS steals_pg_twoweeks
,twoweeks.blocks_pg_twoweeks AS blocks_pg_twoweeks
,twoweeks.turnovers_pg_twoweeks AS turnovers_pg_twoweeks
,twoweeks.personal_fouls_pg_twoweeks AS personal_fouls_pg_twoweeks
,twoweeks.points_pg_twoweeks AS points_pg_twoweeks
,twoweeks.minutes_pg_twoweeks AS minutes_pg_twoweeks

FROM
(
SELECT 
 g.player_id
,SUM(g.field_goal_attempts)*1.0 / season_games.games*1.0 AS field_goal_attempts_pg_season
,SUM(g.field_goals)*1.0 / season_games.games*1.0 AS field_goals_pg_season
,SUM(g.three_point_attempts)*1.0 / season_games.games*1.0 AS three_point_attempts_pg_season
,SUM(g.three_pointers)*1.0 / season_games.games*1.0 AS three_pointers_pg_season
,SUM(g.free_throw_attempts)*1.0 / season_games.games*1.0 AS free_throw_attempts_pg_season
,SUM(g.free_throws)*1.0 / season_games.games*1.0 AS free_throws_pg_season
,SUM(g.offensive_rebounds)*1.0 / season_games.games*1.0 AS offensive_rebounds_pg_season 
,SUM(g.defensive_rebounds)*1.0 / season_games.games*1.0 AS defensive_rebounds_pg_season
,SUM(g.assists)*1.0 / season_games.games*1.0 AS assists_pg_season
,SUM(g.steals)*1.0 / season_games.games*1.0 AS steals_pg_season
,SUM(g.blocks)*1.0 / season_games.games*1.0 AS blocks_pg_season
,SUM(g.turnovers)*1.0 / season_games.games*1.0 AS turnovers_pg_season
,SUM(g.personal_fouls)*1.0 / season_games.games*1.0 AS personal_fouls_pg_season
,SUM(g.points)*1.0 / season_games.games*1.0 AS points_pg_season
,SUM(g.minutes_played)*1.0 / season_games.games*1.0 AS minutes_pg_season
FROM games g
JOIN 
(
SELECT g.player_id, COUNT(DISTINCT g.game_id) AS games 
FROM games g
WHERE g.player_id = '<player>' 
AND g.season = '<season>' 
AND g.game_date < '<game_date>'
) season_games ON season_games.player_id = g.player_id

WHERE g.player_id = '<player>' 
AND g.season = '<season>' 
AND g.game_date < '<game_date>'
GROUP BY g.player_id
) season

-- SUB QUERY FOR THE PAST 5 GAMES
JOIN 
(
SELECT  
 g.player_id
,SUM(g.field_goal_attempts)*1.0 / fivegames.games*1.0 AS field_goal_attempts_pg_5games
,SUM(g.field_goals)*1.0 / fivegames.games*1.0 AS field_goals_pg_5games
,SUM(g.three_point_attempts)*1.0 / fivegames.games*1.0 AS three_point_attempts_pg_5games
,SUM(g.three_pointers)*1.0 / fivegames.games*1.0 AS three_pointers_pg_5games
,SUM(g.free_throw_attempts)*1.0 / fivegames.games*1.0 AS free_throw_attempts_pg_5games
,SUM(g.free_throws)*1.0 / fivegames.games*1.0 AS free_throws_pg_5games
,SUM(g.offensive_rebounds)*1.0 / fivegames.games*1.0 AS offensive_rebounds_pg_5games
,SUM(g.defensive_rebounds)*1.0 / fivegames.games*1.0 AS defensive_rebounds_pg_5games
,SUM(g.assists)*1.0 / fivegames.games*1.0 AS assists_pg_5games
,SUM(g.steals)*1.0 / fivegames.games*1.0 AS steals_pg_5games
,SUM(g.blocks)*1.0 / fivegames.games*1.0 AS blocks_pg_5games
,SUM(g.turnovers)*1.0 / fivegames.games*1.0 AS turnovers_pg_5games
,SUM(g.personal_fouls)*1.0 / fivegames.games*1.0 AS personal_fouls_pg_5games
,SUM(g.points)*1.0 / fivegames.games*1.0 AS points_pg_5games
,SUM(g.minutes_played)*1.0 / fivegames.games*1.0 AS minutes_pg_5games
FROM games g
JOIN
(
SELECT player_id, MIN(COUNT(DISTINCT game_id),5) AS games
FROM games
WHERE player_id = '<player>' 
AND season = '<season>'
AND game_date < '<game_date>'
) fivegames ON fivegames.player_id = g.player_id

JOIN
(
SELECT DISTINCT game_id
FROM games
WHERE player_id = '<player>' 
AND season = '<season>' 
AND game_date < '<game_date>'
ORDER BY game_id DESC
LIMIT 5
) top5 ON g.game_id = top5.game_id

WHERE g.player_id = '<player>' 
AND g.season = '<season>' 
AND g.game_date < '<game_date>'
) five_games ON five_games.player_id = season.player_id


-- SUB QUERY FOR GAMES IN THE PAST TWO WEEKS
JOIN
(
SELECT 
 g.player_id
,SUM(g.field_goal_attempts)*1.0 / twoweeks.games*1.0 AS field_goal_attempts_pg_twoweeks
,SUM(g.field_goals)*1.0 / twoweeks.games*1.0 AS field_goals_pg_twoweeks
,SUM(g.three_point_attempts)*1.0 / twoweeks.games*1.0 AS three_point_attempts_pg_twoweeks
,SUM(g.three_pointers)*1.0 / twoweeks.games*1.0 AS three_pointers_pg_twoweeks
,SUM(g.free_throw_attempts)*1.0 / twoweeks.games*1.0 AS free_throw_attempts_pg_twoweeks
,SUM(g.free_throws)*1.0 / twoweeks.games*1.0 AS free_throws_pg_twoweeks
,SUM(g.offensive_rebounds)*1.0 / twoweeks.games*1.0 AS offensive_rebounds_pg_twoweeks
,SUM(g.defensive_rebounds)*1.0 / twoweeks.games*1.0 AS defensive_rebounds_pg_twoweeks
,SUM(g.assists)*1.0 / twoweeks.games*1.0 AS assists_pg_twoweeks
,SUM(g.steals)*1.0 / twoweeks.games*1.0 AS steals_pg_twoweeks
,SUM(g.blocks)*1.0 / twoweeks.games*1.0 AS blocks_pg_twoweeks
,SUM(g.turnovers)*1.0 / twoweeks.games*1.0 AS turnovers_pg_twoweeks
,SUM(g.personal_fouls)*1.0 / twoweeks.games*1.0 AS personal_fouls_pg_twoweeks
,SUM(g.points)*1.0 / twoweeks.games*1.0 AS points_pg_twoweeks
,SUM(g.minutes_played)*1.0 / twoweeks.games*1.0 AS minutes_pg_twoweeks
FROM games g
JOIN
(
SELECT player_id, COUNT(DISTINCT game_id) games
FROM games
WHERE player_id = '<player>'
AND game_date BETWEEN DATE('<game_date>','-14 day') AND '<game_date>'
) twoweeks ON twoweeks.player_id = g.player_id
WHERE g.player_id = '<player>' 
AND g.season = '<season>' 
AND g.game_id IN
(
SELECT DISTINCT game_id
FROM games
WHERE player_id = '<player>' 
AND game_date BETWEEN DATE('<game_date>','-14 day') AND '<game_date>'
)
) twoweeks ON twoweeks.player_id = season.player_id