SELECT u.ID [ID], 
cast(u.Percentage AS NUMERIC(36,11)) [Payout Percentage], 
cast(u.VI AS NUMERIC(36,11)) [Volatility Index], 
cast(u.SD AS NUMERIC(36,11)) [Standard Deviation],
b.Name,  
b.FileName [File Name], 
CEILING(0.5 *(POWER(CEILING(u.VI)/0.004,2) + @MinSpins + ABS(POWER(CEILING(u.VI)/0.004,2) - @MinSpins))) [Required Spins], 
(CEILING(0.5 *(POWER(CEILING(u.VI)/0.004,2) + @MinSpins + ABS(POWER(CEILING(u.VI)/0.004,2) - @MinSpins)))/@MinSpins)*@Hours [Hours]
FROM dbo.tb_PayoutPercentage u JOIN dbo.tb_Strategy b ON u.StrategyId = b.StrategyID WHERE u.ID = @ID