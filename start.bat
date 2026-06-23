@echo off
REM Quick Start Script for Windows
REM Run this to install dependencies and start the application

echo ============================================================
echo DIABETES PREDICTION SYSTEM - WINDOWS QUICK START
echo ============================================================
echo.

echo [Step 1/3] Installing Python dependencies...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies!
    pause
    exit /b 1
)
echo.

echo [Step 2/3] Training ML model...
python train_model.py
if errorlevel 1 (
    echo Model training failed! You can run it later manually.
    echo.
)
echo.

echo [Step 3/3] Starting Flask server...
echo.
echo ============================================================
echo APPLICATION STARTED SUCCESSFULLY!
echo ============================================================
echo.
echo Access the application at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

cd backend
python app.py

pause
