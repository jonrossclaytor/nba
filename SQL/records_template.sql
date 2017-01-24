SELECT DISTINCT
 games.player_id
,games.game_id
,MAX(games.assists,0.001) AS assists
,MAX(games.total_rebounds,0.001) AS total_rebounds
,MAX(games.points,0.001) AS points
,MAX(games.steals,0.001) AS steals
,MAX(games.blocks,0.001) AS blocks
,MAX(games.turnovers,0.001) AS turnovers
,MAX(games.three_pointers,0.001) AS three_pointers

,player_stats.field_goal_attempts_pg_season
,player_stats.field_goals_pg_season
,player_stats.three_point_attempts_pg_season
,player_stats.three_pointers_pg_season
,player_stats.free_throw_attempts_pg_season
,player_stats.free_throws_pg_season
,player_stats.offensive_rebounds_pg_season
,player_stats.defensive_rebounds_pg_season
,player_stats.assists_pg_season
,player_stats.steals_pg_season
,player_stats.blocks_pg_season
,player_stats.turnovers_pg_season
,player_stats.personal_fouls_pg_season
,player_stats.points_pg_season
,player_stats.minutes_pg_season              
,player_stats.field_goal_attempts_pg_5games
,player_stats.field_goals_pg_5games
,player_stats.three_point_attempts_pg_5games
,player_stats.three_pointers_pg_5games
,player_stats.free_throw_attempts_pg_5games
,player_stats.free_throws_pg_5games
,player_stats.offensive_rebounds_pg_5games
,player_stats.defensive_rebounds_pg_5games
,player_stats.assists_pg_5games
,player_stats.steals_pg_5games
,player_stats.blocks_pg_5games
,player_stats.turnovers_pg_5games
,player_stats.personal_fouls_pg_5games
,player_stats.points_pg_5games
,player_stats.minutes_pg_5games
,player_stats.field_goal_attempts_pg_twoweeks
,player_stats.field_goals_pg_twoweeks
,player_stats.three_point_attempts_pg_twoweeks
,player_stats.three_pointers_pg_twoweeks
,player_stats.free_throw_attempts_pg_twoweeks
,player_stats.free_throws_pg_twoweeks
,player_stats.offensive_rebounds_pg_twoweeks
,player_stats.defensive_rebounds_pg_twoweeks
,player_stats.assists_pg_twoweeks
,player_stats.steals_pg_twoweeks
,player_stats.blocks_pg_twoweeks
,player_stats.turnovers_pg_twoweeks
,player_stats.personal_fouls_pg_twoweeks
,player_stats.points_pg_twoweeks
,player_stats.minutes_pg_twoweeks


,team_stats.missed_field_goal_pg_season
,team_stats.missed_three_pointers_pg_season
,team_stats.missed_free_throws_pg_season
,team_stats.offensive_rebounds_pg_season
,team_stats.defensive_rebounds_pg_season
,team_stats.assists_pg_season
,team_stats.steals_pg_season
,team_stats.blocks_pg_season
,team_stats.turnovers_pg_season
,team_stats.personal_fouls_pg_season
,team_stats.missed_field_goal_pg_5games
,team_stats.missed_three_pointers_pg_5games
,team_stats.missed_free_throws_pg_5games
,team_stats.offensive_rebounds_pg_5games
,team_stats.defensive_rebounds_pg_5games
,team_stats.assists_pg_5games
,team_stats.steals_pg_5games
,team_stats.blocks_pg_5games
,team_stats.turnovers_pg_5games
,team_stats.personal_fouls_pg_5games
,team_stats.missed_field_goal_pg_twoweeks
,team_stats.missed_three_pointers_pg_twoweeks
,team_stats.missed_free_throws_pg_twoweeks
,team_stats.offensive_rebounds_pg_twoweeks
,team_stats.defensive_rebounds_pg_twoweeks
,team_stats.assists_pg_twoweeks
,team_stats.steals_pg_twoweeks
,team_stats.blocks_pg_twoweeks
,team_stats.turnovers_pg_twoweeks
,team_stats.personal_fouls_pg_twoweeks

FROM player_stats
JOIN team_stats ON player_stats.game_id = team_stats.game_id AND team_stats.team != (SELECT team FROM games WHERE game_id = '<game_id>' AND player_id = '<player_id>')
JOIN games on games.player_id = player_stats.player_id AND games.game_id = player_stats.game_id
WHERE player_stats.player_id = '<player_id>' 
AND player_stats.game_id = '<game_id>'