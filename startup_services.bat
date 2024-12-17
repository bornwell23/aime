@echo off
@REM Check if Docker Desktop is running
sc query "com.docker.service" > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Docker Desktop is not running. Please start Docker Desktop and try again.
    pause
    exit /b 1
)

echo Containerizing Aime Application...
docker-compose build
echo Starting Aime Application...
docker-compose up