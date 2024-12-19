@echo off
setlocal enabledelayedexpansion

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not running. Please start Docker and try again.
    pause
    exit /b 1
)

REM Remove existing auth service container if it exists
docker ps -a | findstr "aime-auth-service" >nul 2>&1
if %errorlevel% equ 0 (
    echo Removing existing auth service container...
    docker rm -f aime-auth-service
)

REM Build the auth service image
echo Building auth service image...
docker build -t aime-auth-service ../auth-service

REM Run the auth service container
echo Starting auth service container...
docker run -d ^
    --name aime-auth-service ^
    --network aime-network ^
    -p 8000:8000 ^
    aime-auth-service

if %errorlevel% equ 0 (
    echo Auth service started successfully!
) else (
    echo Failed to start auth service.
)

pause
