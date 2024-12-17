#!/usr/bin/env pwsh

# Function to stop Node.js processes
function Stop-NodeProcesses {
    param (
        [switch]$Force = $false
    )

    # Keywords to identify Aime-related Node processes
    $aimeKeywords = @('aime', 'ui', 'server', 'vue', 'node')

    # Get all Node.js processes
    $nodeProcesses = Get-Process -Name node -ErrorAction SilentlyContinue | Where-Object {
        $processName = $_.ProcessName
        $commandLine = (Get-WmiObject Win32_Process | Where-Object { $_.ProcessId -eq $_.ProcessId }).CommandLine

        # Check if any Aime keywords are in the command line
        $aimeKeywords | ForEach-Object {
            if ($commandLine -like "*$_*") {
                return $true
            }
        }
    }

    if ($nodeProcesses.Count -eq 0) {
        Write-Host "No Aime-related Node.js processes found." -ForegroundColor Green
        return
    }

    Write-Host "Found $($nodeProcesses.Count) Aime-related Node.js processes to stop." -ForegroundColor Yellow
    
    foreach ($process in $nodeProcesses) {
        try {
            if ($Force) {
                Write-Host "Forcefully terminating process: $($process.Id) - $($process.ProcessName)" -ForegroundColor Red
                Stop-Process -Id $process.Id -Force
            } else {
                Write-Host "Gracefully stopping process: $($process.Id) - $($process.ProcessName)" -ForegroundColor Yellow
                $process.CloseMainWindow() | Out-Null
            }
        }
        catch {
            Write-Host "Failed to stop process $($process.Id)" -ForegroundColor Red
        }
    }

    # Additional cleanup for any lingering processes
    Start-Sleep -Seconds 2
    Stop-NodeProcesses -Force
}

# Stop ui
Write-Host "Stopping ui..." -ForegroundColor Cyan
$uiDir = "d:/coding/Aime/ui"
if (Test-Path "$uiDir\shutdown.bat") {
    Start-Process "$uiDir\shutdown.bat" -Wait
} else {
    Write-Host "No ui shutdown script found." -ForegroundColor Yellow
}

# Stop Server
Write-Host "Stopping Server..." -ForegroundColor Cyan
$serverDir = "d:/coding/Aime/server"
if (Test-Path "$serverDir\restart.bat") {
    Start-Process "$serverDir\restart.bat" -Wait
} else {
    Write-Host "No server restart/stop script found." -ForegroundColor Yellow
}

# Stop all Node processes
Write-Host "Cleaning up Node processes..." -ForegroundColor Cyan
Stop-NodeProcesses -Force

Write-Host "Aime services stopped successfully." -ForegroundColor Green
