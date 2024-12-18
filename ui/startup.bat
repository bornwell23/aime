@echo off
setlocal enabledelayedexpansion

:: Check if Node.js is installed
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo Node.js is not installed. Please install Node.js first.
    exit /b 1
)

:: Navigate to the ui directory
cd /d "%~dp0"

:: Install dependencies if node_modules doesn't exist
if not exist "node_modules\" (
    echo Installing dependencies...
    call npm install
    if %errorlevel% neq 0 (
        echo Failed to install dependencies.
        pause
        exit /b 1
    )
)

:: Check if .env file exists in project root
if not exist "..\\.env" (
    echo .env file not found in project root. Creating with default settings.
    echo UI_PORT=8008 > "..\\.env"
)

:: Read UI_PORT from .env file
for /f "tokens=2 delims==" %%a in ('findstr /i "UI_PORT" "..\\.env"') do set UI_PORT=%%a

:: Check if serve is running on the specified port
netstat -ano | findstr ":%UI_PORT%" >nul
if %errorlevel% equ 0 (
    echo Port %UI_PORT% is already in use. Please free up the port and try again.
    pause
    exit /b 1
)

:: Start the development server
echo Starting development server...
start "" http://localhost:%UI_PORT%
npm run serve

echo.
echo If the browser doesn't open automatically, visit: http://localhost:%UI_PORT%
pause
