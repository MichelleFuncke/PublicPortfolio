SELECT 
	@name [Name], 
	GameName, 
	bl.GameId, 
	SUM(bl.NumChips * bl.ChipSize * 1.0) [SumWager], 
	SUM(bl.Payout * 1.0) [SumPayouts], 
	(SELECT COUNT(*) 
		FROM tb_Bets
		WHERE GameId = @gameid
		AND Time BETWEEN @StartTime AND @EndTime
		AND UserId IN 	(SELECT ID FROM tb_Users nolock
							WHERE Name LIKE @name
							AND BetNumber = 0) [NumBets], 
	MAX(Payout) [MaxPayout], 
	((SUM(Payout * 1.0) / SUM(NumChips * ChipSize * 1.0)) * 100) [PayoutPercentage]
FROM tb_Bets bl 
JOIN tb_Games m 
ON bl.GameID = m.GameID
WHERE bl.GameID = @gameid
AND bl.UserID IN (SELECT ID FROM tb_Users
					WHERE Name LIKE @name)
AND Time BETWEEN @StartTime AND @EndTime
GROUP BY GameName, bl.GameID
ORDER BY GameName, bl.GameID