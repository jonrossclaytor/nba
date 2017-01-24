SELECT model, params, mse
FROM model_results
WHERE model_date = '<model_date>'
AND player_id = '<player_id>'
AND stat = '<stat>'
AND mse = 
(
SELECT MIN(mse)
FROM model_results
WHERE model_date = '<model_date>'
AND player_id = '<player_id>'
AND stat = '<stat>'
)