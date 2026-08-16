@echo off
title Web Browser Setup

echo ==============================
echo       WEB BROWSER SETUP
echo ==============================
echo.

echo Creating virtual environment...
python -m venv env

if errorlevel 1 (
    echo Failed to create virtual environment.
    pause
    exit /b 1
)

echo.
echo Activating virtual environment...
call env\Scripts\activate.bat

echo.
echo Installing requirements...
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Failed to install requirements.
    pause
    exit /b 1
)

echo.
echo ==============================
echo       SETUP COMPLETE!
echo ==============================
echo.
echo Run the browser with:
echo     python main.py
echo.

pause