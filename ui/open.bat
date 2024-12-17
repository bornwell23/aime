@echo off
setlocal enabledelayedexpansion

:: Check if .env file exists in project root
if not exist "..\\.env" (
    echo .env file not found in project root. Creating with default settings.
    echo FRONT_PORT=8008 > "..\\.env"
)

:: Read FRONT_PORT from .env file
for /f "tokens=2 delims==" %%a in ('findstr /i "FRONT_PORT" "..\\.env"') do set FRONT_PORT=%%a

:: Set default URL
set "URL=http://localhost:%FRONT_PORT%"

:: Default browser is Chrome
set "BROWSER=chrome"

:: Check for command line argument for browser choice
if not "%~1"=="" (
    if /i "%~1"=="edge" (
        set "BROWSER=edge"
    ) else if /i "%~1"=="chrome" (
        set "BROWSER=chrome"
    ) else (
        echo Invalid browser specified. Using default (Chrome^).
        echo Usage: open.bat [chrome^|edge]
        timeout /t 2 >nul
    )
)

:: Check if the server is running
netstat -ano | findstr ":%FRONT_PORT%" >nul
if %errorlevel% neq 0 (
    echo ui server is not running on port %FRONT_PORT%.
    echo Please start the server first using startup.bat
    pause
    exit /b 1
)

:: Try to open in the specified browser
if "%BROWSER%"=="chrome" (
    echo Opening in Chrome...
    
    :: Try Chrome's default installation paths
    set "CHROME_PATHS=C:\Program Files\Google\Chrome\Application\chrome.exe;C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    
    for %%p in (!CHROME_PATHS:;=!) do (
        if exist "%%p" (
            start "" "%%p" %URL%
            echo Opened successfully in Chrome.
            exit /b 0
        )
    )
    
    :: If Chrome paths not found, try the generic command
    start chrome %URL%
    if !errorlevel! equ 0 (
        echo Opened successfully in Chrome.
    ) else (
        echo Failed to open in Chrome. Is it installed?
        echo Attempting to open in default browser...
        start %URL%
    )
) else if "%BROWSER%"=="edge" (
    echo Opening in Edge...
    start msedge %URL%
    if !errorlevel! equ 0 (
        echo Opened successfully in Edge.
    ) else (
        echo Failed to open in Edge. Is it installed?
        echo Attempting to open in default browser...
        start %URL%
    )
)

echo.
echo If the browser didn't open automatically, please visit: %URL%
timeout /t 3 >nul
