@echo off
@echo off
if "%1" == "--rebuild" (
    @echo "Rebuilding Aime Application..."
    docker-compose down
    sleep 1
    set BUILD_DATE=%date:~0,4%%date:~4,2%/%date:~7,2% %time:~0,2%:%time:~3,2%:%time:~6,2%
    docker-compose build --no-cache
) else (
    @echo Containerizing Aime Application...
    docker-compose build
)

@echo Starting Aime Application...
docker-compose up