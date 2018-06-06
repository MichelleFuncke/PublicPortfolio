USE ApplicationDB
DECLARE @AppNum INT
SET @AppNum = (SELECT ApplicationNumber FROM dbo.ApplicationIDs WHERE ApplicationName LIKE @AppName)

INSERT INTO dbo.ApplicationLogs
        ( Time, Username, Application, Notes, Event,TimeTaken )
VALUES  ( @time,@User,@AppNum,@Notes,@Event,@TimeTaken)