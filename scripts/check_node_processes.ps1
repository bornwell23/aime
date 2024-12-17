#!/usr/bin/env pwsh

# Function to get processes with detailed information
function Get-AimeNodeProcesses {
    param (
        [switch]$Verbose = $false
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
        Write-Host "No Aime-related Node.js processes found." -ForegroundColor Yellow
        return
    }

    Write-Host "Aime Node.js Processes:" -ForegroundColor Green
    $nodeProcesses | ForEach-Object {
        $process = $_
        $fullDetails = Get-WmiObject Win32_Process | Where-Object { $_.ProcessId -eq $process.Id }

        Write-Host "`nProcess ID: $($process.Id)" -ForegroundColor Cyan
        Write-Host "Name: $($process.ProcessName)" -ForegroundColor White
        Write-Host "Command Line: $($fullDetails.CommandLine)" -ForegroundColor White
        
        if ($Verbose) {
            Write-Host "CPU Usage: $($process.CPU) seconds" -ForegroundColor White
            Write-Host "Memory Usage: $([math]::Round($process.WorkingSet64 / 1MB, 2)) MB" -ForegroundColor White
        }
    }

    # Option to kill processes
    $confirmation = Read-Host "Do you want to terminate these processes? (y/n)"
    if ($confirmation -eq 'y') {
        $nodeProcesses | ForEach-Object {
            try {
                Stop-Process -Id $_.Id -Force
                Write-Host "Terminated process ID $($_.Id)" -ForegroundColor Red
            }
            catch {
                Write-Host "Could not terminate process ID $($_.Id)" -ForegroundColor Yellow
            }
        }
    }
}

# Run the function
Get-AimeNodeProcesses -Verbose
