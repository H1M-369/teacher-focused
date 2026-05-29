@echo off
title AI Assignment Creator — Setup
echo ================================================
echo  AI Assignment Creator — First-Time Setup
echo ================================================
echo.
echo Installing required Python packages...
echo.
pip install -r requirements.txt
echo.
echo ================================================
if %errorlevel% == 0 (
    echo  Setup complete! Run "run.bat" to start the app.
) else (
    echo  Something went wrong. Check that Python is
    echo  installed and added to your PATH.
)
echo ================================================
echo.
pause
