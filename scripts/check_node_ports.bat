@echo off
echo Checking for Node.js processes using netstat...
echo.

netstat -ano | findstr /C:"LISTENING" | findstr /C:"node.exe"

echo.
echo Done. The above lines show Node.js processes currently listening on ports.
