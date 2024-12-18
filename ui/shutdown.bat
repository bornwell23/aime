@echo off
setlocal enabledelayedexpansion

:: Check if .env file exists in project root
if not exist "..\\.env" (
    echo .env file not found in project root. Creating with default settings.
    echo UI_PORT=8008 > "..\\.env"
)

:: Read UI_PORT from .env file
for /f "tokens=2 delims==" %%a in ('findstr /i "UI_PORT" "..\\.env"') do set UI_PORT=%%a

:: Kill Node.js processes
echo Stopping Node.js processes...
taskkill /F /IM node.exe 2>nul
if %errorlevel% equ 0 (
    echo Successfully stopped Node.js processes.
) else (
    echo No Node.js processes were running.
)

:: Double check specified port
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":%UI_PORT%"') do (
    echo Found process on port %UI_PORT% with PID: %%a
    taskkill /F /PID %%a
    if %errorlevel% equ 0 (
        echo Successfully stopped process on port %UI_PORT%.
    )
)

echo.
echo Shutdown process complete.
pause
