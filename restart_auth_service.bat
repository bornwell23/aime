@echo off
if "%1" == "--rebuild" (
    echo "Rebuilding auth-service..."
    docker-compose down auth-service
    sleep 1
    set BUILD_DATE=%date:~0,4%%date:~4,2%/%date:~7,2% %time:~0,2%:%time:~3,2%:%time:~6,2%
    call docker-compose up --build --no-deps auth-service -d
) else (
    call docker-compose restart auth-service
)