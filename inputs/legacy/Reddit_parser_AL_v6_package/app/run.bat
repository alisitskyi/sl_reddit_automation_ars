@echo off
cd /d "%~dp0"

echo Перевіряю залежності...
py -m pip install -r requirements.txt --quiet --disable-pip-version-check

echo.
echo Запускаю сервер...
start "" http://localhost:5000
py app.py

pause
