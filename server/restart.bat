@echo off
echo Restarting Aime Server...

:: Navigate to the server directory
cd /d "%~dp0"

:: Check if PM2 is running the service
call pm2 pid aime-server >nul 2>&1
if %errorlevel% equ 0 (
    :: Service is running, restart it
    echo Restarting existing service...
    call pm2 restart aime-server
) else (
    :: Service is not running, start it
    echo Service not running. Starting service...
    call npm run prod
)

echo.
echo Service status:
call pm2 status aime-server
pause
