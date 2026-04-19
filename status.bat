@echo off
echo Checking Budget App status...
ssh rich@10.0.0.30 "curl -s -o /dev/null -w 'HTTP Status: %%{http_code}\n' http://localhost:8080 || echo App not responding"
echo.
echo Running processes:
ssh rich@10.0.0.30 "ps aux | grep 'python3 app.py' | grep -v grep"
pause