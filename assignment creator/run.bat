@echo off
title AI Assignment Creator
echo ================================================
echo  AI Assignment Creator — Starting...
echo ================================================
echo.
echo The app will open in your browser automatically.
echo If it doesn't, go to: http://localhost:8501
echo.
echo To stop the app, close this window.
echo.
streamlit run app.py --browser.gatherUsageStats false
pause
