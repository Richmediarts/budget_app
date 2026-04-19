@echo off
echo Starting Budget App...
ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 rich@10.0.0.30 "cd /home/rich/DATA/budget_app && source venv/bin/activate && nohup python3 app.py > app.log 2>&1 &"
echo Done! Visit http://10.0.0.30:8080
pause