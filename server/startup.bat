@echo off
echo Starting Aime Server Setup...

:: Check if Node.js is installed
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo Node.js is not installed. Please install Node.js first.
    exit /b 1
)

:: Navigate to the server directory
cd /d "%~dp0"

:: Install dependencies
echo Installing dependencies...
call npm install

:: Check if PM2 is installed globally
call pm2 -v >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing PM2 globally...
    call npm install -g pm2
)

:: Start the service using PM2
echo Starting Aime server...
call npm run prod

:: Save PM2 process list to ensure it starts on system reboot
call pm2 save

:: Setup PM2 to start on system startup
call pm2 startup

echo Setup complete! The service is now running.
echo To check status, use: pm2 status
pause
