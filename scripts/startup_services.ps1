#!/usr/bin/env pwsh

# Improved logging function
function Write-DetailedLog {
    param (
        [string]$Message,
        [string]$LogLevel = 'INFO',
        [switch]$Err
    )

    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $fullMessage = "[$timestamp] [$LogLevel] $Message"

    if ($Err) {
        Write-Host $fullMessage -ForegroundColor Red
    } else {
        Write-Host $fullMessage -ForegroundColor Green
    }

    # Ensure log directory exists
    $logDir = "d:/coding/Aime/logs"
    if (-not (Test-Path $logDir)) {
        New-Item -ItemType Directory -Path $logDir -Force | Out-Null
    }

    # Write to log file
    Add-Content -Path "$logDir/startup_debug.log" -Value $fullMessage
}

# Enhanced error logging function
function Write-ErrorLog {
    param (
        [string]$ServiceName,
        [System.Management.Automation.ErrorRecord]$ErrorRecord
    )

    $errorMessage = $ErrorRecord.Exception.Message
    $fullErrorDetails = $ErrorRecord | Format-List * -Force | Out-String

    Write-DetailedLog -Message "Error in $ServiceName/: $errorMessage" -LogLevel 'ERROR'
    Write-DetailedLog -Message "Full Error Details: $fullErrorDetails" -LogLevel 'ERROR'
}

# Enhanced command existence check
function Test-CommandExists {
    param ($Command)
    try {
        $fullPath = (Get-Command $Command -ErrorAction Stop).Source
        Write-DetailedLog "Command found: $Command at $fullPath"
        return $true
    }
    catch {
        Write-DetailedLog "Command not found: $Command" -LogLevel 'ERROR'
        return $false
    }
}

# Enhanced service start function
function Start-AimeService {
    param (
        [string]$ServiceName,
        [string]$WorkingDirectory,
        [string]$StartCommand,
        [string]$LogFile,
        [string[]]$StartArgs = @()
    )

    Write-DetailedLog "Attempting to start $ServiceName in $WorkingDirectory"

    # Ensure working directory exists
    if (-not (Test-Path $WorkingDirectory)) {
        Write-DetailedLog "Error: Directory $WorkingDirectory does not exist!" -LogLevel 'ERROR'
        return $false
    }

    # Create log directory if it doesn't exist
    $logDir = Split-Path $LogFile -Parent
    if (-not (Test-Path $logDir)) {
        New-Item -ItemType Directory -Path $logDir | Out-Null
    }

    # Prepare full command logging
    $fullCommand = "$StartCommand $($StartArgs -join ' ')"
    Write-DetailedLog "Full command: $fullCommand"

    # Start the service with enhanced error handling
    try {
        $processInfo = New-Object System.Diagnostics.ProcessStartInfo
        $processInfo.FileName = $StartCommand
        $processInfo.RedirectStandardOutput = $true
        $processInfo.RedirectStandardError = $true
        $processInfo.UseShellExecute = $false
        $processInfo.WorkingDirectory = $WorkingDirectory
        $processInfo.Arguments = $StartArgs

        $process = New-Object System.Diagnostics.Process
        $process.StartInfo = $processInfo
        
        # Event handlers for output and error
        $outputEvent = Register-ObjectEvent -InputObject $process -EventName OutputDataReceived -Action {
            param($sender, $eventArgs)
            if ($eventArgs.Data) {
                Add-Content -Path $using:LogFile -Value $eventArgs.Data
            }
        }
        
        $errorEvent = Register-ObjectEvent -InputObject $process -EventName ErrorDataReceived -Action {
            param($sender, $eventArgs)
            if ($eventArgs.Data) {
                Add-Content -Path ($using:LogFile -replace "\.log$", ".err.log") -Value $eventArgs.Data
            }
        }

        $process.Start() | Out-Null
        $process.BeginOutputReadLine()
        $process.BeginErrorReadLine()

        Write-DetailedLog "$ServiceName started successfully (PID: $($process.Id))"
        return $true
    }
    catch {
        Write-ErrorLog -ServiceName $ServiceName -ErrorRecord $_
        return $false
    }
    finally {
        if ($outputEvent) { Unregister-Event -SourceIdentifier $outputEvent.Name }
        if ($errorEvent) { Unregister-Event -SourceIdentifier $errorEvent.Name }
    }
}

# Function to check service health
function Test-ServiceHealth {
    param (
        [string]$ServiceName,
        [int]$Port,
        [int]$MaxRetries = 10
    )

    for ($i = 1; $i -le $MaxRetries; $i++) {
        try {
            $tcpClient = New-Object System.Net.Sockets.TcpClient
            $tcpClient.Connect("localhost", $Port)
            
            if ($tcpClient.Connected) {
                Write-DetailedLog "$ServiceName is running on port $Port"
                $tcpClient.Close()
                return $true
            }
        }
        catch {
            Write-DetailedLog "Waiting for $ServiceName to start... (Attempt $i/$MaxRetries)" -LogLevel 'ERROR'
            Start-Sleep -Seconds 2
        }
    }

    Write-DetailedLog "Failed to start $ServiceName after $MaxRetries attempts" -LogLevel 'ERROR'
    return $false
}

# Function to stop Aime-related Node.js processes
function Stop-AimeProcesses {
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
        Write-DetailedLog "No Aime-related Node.js processes found." -LogLevel 'INFO'
        return $true
    }

    Write-DetailedLog "Found $($nodeProcesses.Count) Aime-related Node.js processes." -LogLevel 'WARNING'
    
    foreach ($process in $nodeProcesses) {
        try {
            if ($Force) {
                Write-DetailedLog "Forcefully terminating process: $($process.Id) - $($process.ProcessName)" -LogLevel 'WARNING'
                Stop-Process -Id $process.Id -Force
            } else {
                Write-DetailedLog "Gracefully stopping process: $($process.Id) - $($process.ProcessName)" -LogLevel 'WARNING'
                $process.CloseMainWindow() | Out-Null
            }
        }
        catch {
            Write-DetailedLog "Failed to stop process $($process.Id)" -LogLevel 'ERROR'
            return $false
        }
    }

    # Wait a moment to ensure processes are stopped
    Start-Sleep -Seconds 2
    return $true
}

# Main startup function
function Start-AimeApplication {

    # Check and stop existing processes
    $processesCleared = Stop-AimeProcesses

    if (-not $processesCleared) {
        Write-DetailedLog "Could not clear existing processes. Attempting force stop." -LogLevel 'ERROR'
        $processesCleared = Stop-AimeProcesses -Force
        
        if (-not $processesCleared) {
            Write-DetailedLog "Failed to stop existing processes. Aborting startup." -LogLevel 'ERROR'
            return $false
        }
    }

    $serverDir = "d:/coding/Aime/server"
    $uiDir = "d:/coding/Aime/ui"

    # Verify directories exist
    if (-not (Test-Path $serverDir) -or -not (Test-Path $uiDir)) {
        Write-DetailedLog "Server or ui directory does not exist!" -LogLevel 'ERROR'
        return $false
    }

    # Start server using its startup script
    Write-DetailedLog "Starting Aime Server..."
    $serverStartProcess = Start-Process -FilePath "$serverDir\startup.bat" -WorkingDirectory $serverDir -PassThru

    # Wait for server to start
    if (-not (Test-ServiceHealth -ServiceName "Aime Server" -Port 3000)) {
        Write-DetailedLog "Server service failed to start. Aborting." -LogLevel 'ERROR'
        return $false
    }

    $rootEnvPath = Join-Path -Path $PSScriptRoot "\..\\.env"

    # Read UI_PORT from .env file if it exists
    $rootEnv = Get-Content $rootEnvPath | ConvertFrom-StringData

    if (-not $rootEnv) {
        $uiPort = 8008
    }

    # Use the port from .env, default to 8008 if not set
    $uiPort = $rootEnv.UI_PORT
    if (-not $uiPort) {
        $uiPort = 8008
    }

    if (Test-ServiceHealth -ServiceName "Aime ui" -Port $uiPort -MaxRetries 1) {
        Write-DetailedLog "ui service already running. Opening browser..."
        Start-Process -FilePath "http://localhost:$uiPort" -PassThru
    }

    # Start ui using its startup script
    Write-DetailedLog "Starting Aime ui..."
    $uiStartProcess = Start-Process -FilePath "startup.bat" -WorkingDirectory $PSScriptRoot"\..\ui" -PassThru

    # Wait for ui to start
    if (-not (Test-ServiceHealth -ServiceName "Aime ui" -Port $uiPort -MaxRetries 5)) {
        Write-DetailedLog "ui service failed to start. Aborting." -LogLevel 'ERROR'
        return $false
    }

    Write-DetailedLog "Aime Application started successfully!" -LogLevel 'INFO'
    return $true
}

# Run the startup
$result = Start-AimeApplication

# Pause to keep window open if not successful
if (-not $result) {
    Write-Host "`nPress any key to exit..." -ForegroundColor Yellow
    $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") | Out-Null
}
