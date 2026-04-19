@echo off
echo Budget App Logs:
ssh rich@10.0.0.30 "tail -30 /home/rich/DATA/budget_app/app.log"
pause