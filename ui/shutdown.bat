@echo off
setlocal enabledelayedexpansion

:: Check if .env file exists in project root
if not exist "..\\.env" (
    echo .env file not found in project root. Creating with default settings.
    echo FRONT_PORT=8008 > "..\\.env"
)

:: Read FRONT_PORT from .env file
for /f "tokens=2 delims==" %%a in ('findstr /i "FRONT_PORT" "..\\.env"') do set FRONT_PORT=%%a

:: Kill Node.js processes
echo Stopping Node.js processes...
taskkill /F /IM node.exe 2>nul
if %errorlevel% equ 0 (
    echo Successfully stopped Node.js processes.
) else (
    echo No Node.js processes were running.
)

:: Double check specified port
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":%FRONT_PORT%"') do (
    echo Found process on port %FRONT_PORT% with PID: %%a
    taskkill /F /PID %%a
    if %errorlevel% equ 0 (
        echo Successfully stopped process on port %FRONT_PORT%.
    )
)

echo.
echo Shutdown process complete.
pause
