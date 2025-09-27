@echo off
echo Biomedical Signal Visualization Demo
echo ====================================
echo.
echo Installing required packages...
py -m pip install pandas plotly numpy
echo.
echo Running demonstration...
py demo_features.py
echo.
echo Opening basic demo in browser...
start demo_basic.html
echo.
echo Demo complete! Check the generated HTML files.
pause
