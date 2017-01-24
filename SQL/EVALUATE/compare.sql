SELECT DISTINCT
  g.player_id
, g.game_date
, g.total_rebounds AS rebounds
, p_rebounds.prediction AS p_rebounds
, g.assists
, p_assists.prediction AS p_assists
, g.steals
, p_steals.prediction AS p_steals
, g.blocks
, p_blocks.prediction AS p_blocks
, g.turnovers
, p_turnovers.prediction AS p_turnovers
, g.three_pointers AS made_threes
, p_made_threes.prediction AS p_made_threes
, g.points
, p_points.prediction AS p_points 
, (g.assists * 1.5) + (g.total_rebounds * 1.25) + g.points + (g.steals * 2) + (g.blocks * 2) + (g.turnovers * -.5) + (g.three_pointers * .5) AS dk_score

FROM games g
JOIN  predictions p_rebounds ON p_rebounds.player_id = g.player_id AND p_rebounds.date = g.game_date AND p_rebounds.stat = 'rebounds'
JOIN  predictions p_assists ON p_assists.player_id = g.player_id AND p_assists.date = g.game_date AND p_assists.stat = 'assists'
JOIN  predictions p_steals ON p_steals.player_id = g.player_id AND p_steals.date = g.game_date AND p_steals.stat = 'steals'
JOIN  predictions p_blocks ON p_blocks.player_id = g.player_id AND p_blocks.date = g.game_date AND p_blocks.stat = 'blocks'
JOIN  predictions p_turnovers ON p_turnovers.player_id = g.player_id AND p_turnovers.date = g.game_date AND p_turnovers.stat = 'turnovers'
JOIN  predictions p_points ON p_points.player_id = g.player_id AND p_points.date = g.game_date AND p_points.stat = 'points'
JOIN  predictions p_made_threes ON p_made_threes.player_id = g.player_id AND p_made_threes.date = g.game_date AND p_made_threes.stat = 'made_threes'
WHERE 1=1
AND g.game_date= '2016-12-12'
--and g.player_id = 'irvinky01'
/*
and g.player_id in
(
select player_id from players where player_name_strip in
(
'ALFAROUQ AMINU',
'CJ MCCOLLUM',
'DARREN COLLISON',
'DEMARCUS COUSINS',
'ED DAVIS',
'GARRETT TEMPLE',
'MASON PLUMLEE',
'RUDY GAY'
)
)
*/
ORDER BY points DESC
