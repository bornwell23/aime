@echo off
setlocal enabledelayedexpansion

echo Stopping Aime Services...

:: Stop ui
echo Stopping ui...
call stop_ui.bat

:: Stop Server
echo Stopping Server...
call stop_server.bat

@REM :: Kill any remaining Node processes
@REM echo Killing remaining Node processes...
@REM for /f "tokens=5" %%a in ('netstat -ano ^| findstr /C:"LISTENING" ^| findstr /C:"node.exe"') do (
@REM     taskkill /PID %%a /F 2>nul
@REM )

echo Aime services stopped.
pause
