#!/bin/bash
cd /home/rich/DATA/budget_app
pkill -f "python.*app.py" 2>/dev/null
sleep 2
nohup python3 app.py > app.log 2>&1 &
echo "App started (PID: $!)"
