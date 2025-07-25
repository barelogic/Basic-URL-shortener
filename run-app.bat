@echo off
set FLASK_APP=app.py
set FLASK_ENV=development
python app.py --host=0.0.0.0
pause