@echo off
echo Restarting Budget App...

:: Kill existing process on server
ssh rich@10.0.0.30 "fuser -k 8080/tcp 2>/dev/null"

:: Wait a moment
timeout /t 2 >nul

:: Start app in background via SSH
ssh rich@10.0.0.30 "cd /home/rich/DATA/budget_app && source venv/bin/activate && nohup python3 app.py > app.log 2>&1 &"

echo.
echo Budget App should be running at: http://10.0.0.30:8080
echo.
echo To check if it's running:
echo   ssh rich@10.0.0.30 "curl -s http://localhost:8080"
echo.
echo To view logs:
echo   ssh rich@10.0.0.30 "tail -20 /home/rich/DATA/budget_app/app.log"
pause