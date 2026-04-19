@echo off
set SERVER=10.0.0.30

echo ========================================
echo    BUDGET APP CONTROL
echo ========================================
echo.
echo 1 - Restart App
echo 2 - View Status
echo 3 - View Logs
echo 4 - Open in Browser
echo.
set /p CHOICE=Select (1-4): 

if "%CHOICE%"=="1" goto RESTART
if "%CHOICE%"=="2" goto STATUS
if "%CHOICE%"=="3" goto LOGS
if "%CHOICE%"=="4" goto BROWSER
goto END

:RESTART
echo.
echo Restarting app...
ssh -o StrictHostKeyChecking=no rich@%SERVER% "fuser -k 8080/tcp 2>/dev/null; sleep 1; cd /home/rich/DATA/budget_app && source venv/bin/activate && nohup python3 app.py > app.log 2>&1 &"
echo Done! App restarted.
pause
goto END

:STATUS
echo.
echo Checking status...
ssh -o StrictHostKeyChecking=no rich@%SERVER% "curl -s -o /dev/null -w 'HTTP: %%{http_code}' http://localhost:8080"
echo.
ssh -o StrictHostKeyChecking=no rich@%SERVER% "ps aux | grep 'python3 app.py' | grep -v grep"
pause
goto END

:LOGS
echo.
ssh -o StrictHostKeyChecking=no rich@%SERVER% "tail -25 /home/rich/DATA/budget_app/app.log"
pause
goto END

:BROWSER
start http://%SERVER%:8080
goto END

:END