# Discord Bot Manager Service Monitor
# Created by headx and the psychon

$ErrorActionPreference = "Stop"
$VerbosePreference = "Continue"

# Script configuration
$CONFIG = @{
    WorkingDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
    DataFile = "data\bots.json"
    LogFile = "logs\service-$(Get-Date -Format 'yyyy-MM-dd').log"
    CheckInterval = 30  # seconds
}

# Ensure log directory exists
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
}

function Write-Log {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Message,
        
        [Parameter(Mandatory=$false)]
        [ValidateSet("INFO", "WARN", "ERROR")]
        [string]$Level = "INFO"
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    
    Write-Verbose $logMessage
    Add-Content -Path $CONFIG.LogFile -Value $logMessage
}

function Start-DiscordBot {
    param(
        [Parameter(Mandatory=$true)]
        [PSCustomObject]$Bot
    )
    
    try {
        Write-Log "Starting bot $($Bot.name) (ID: $($Bot.id))"
        
        $pythonPath = (Get-Command python).Source
        $startInfo = New-Object System.Diagnostics.ProcessStartInfo
        $startInfo.FileName = $pythonPath
        $startInfo.Arguments = "bots\runner.py $($Bot.id)"
        $startInfo.WorkingDirectory = $CONFIG.WorkingDirectory
        $startInfo.UseShellExecute = $false
        $startInfo.RedirectStandardOutput = $true
        $startInfo.RedirectStandardError = $true
        $startInfo.WindowStyle = [System.Diagnostics.ProcessWindowStyle]::Hidden
        
        $process = [System.Diagnostics.Process]::Start($startInfo)
        
        Write-Log "Bot process started with PID $($process.Id)"
        return $process
    }
    catch {
        Write-Log "Failed to start bot $($Bot.name): $_" -Level "ERROR"
        return $null
    }
}

function Stop-DiscordBot {
    param(
        [Parameter(Mandatory=$true)]
        [PSCustomObject]$Bot
    )
    
    try {
        if ($Bot.processId) {
            $process = Get-Process -Id $Bot.processId -ErrorAction SilentlyContinue
            if ($process) {
                Write-Log "Stopping bot $($Bot.name) (PID: $($Bot.processId))"
                $process | Stop-Process -Force
                Write-Log "Bot stopped successfully"
            }
        }
    }
    catch {
        Write-Log "Error stopping bot $($Bot.name): $_" -Level "ERROR"
    }
}

function Get-BotsConfig {
    try {
        $json = Get-Content -Path $CONFIG.DataFile -Raw | ConvertFrom-Json
        return $json.bots
    }
    catch {
        Write-Log "Error reading bot configuration: $_" -Level "ERROR"
        return @()
    }
}

function Update-BotStatus {
    param(
        [Parameter(Mandatory=$true)]
        [string]$BotId,
        
        [Parameter(Mandatory=$true)]
        [string]$Status,
        
        [Parameter(Mandatory=$false)]
        [int]$ProcessId = $null
    )
    
    try {
        $json = Get-Content -Path $CONFIG.DataFile -Raw | ConvertFrom-Json
        $bot = $json.bots | Where-Object { $_.id -eq $BotId }
        
        if ($bot) {
            $bot.status = $Status
            $bot.processId = $ProcessId
            $bot.lastUpdated = (Get-Date).ToString("o")
            
            $json | ConvertTo-Json -Depth 10 | Set-Content -Path $CONFIG.DataFile
        }
    }
    catch {
        Write-Log "Error updating bot status: $_" -Level "ERROR"
    }
}

function Start-BotMonitor {
    Write-Log "Starting Discord Bot Manager Service Monitor"
    Write-Log "Working Directory: $($CONFIG.WorkingDirectory)"
    
    # Track running bots
    $runningBots = @{}
    
    while ($true) {
        try {
            $bots = Get-BotsConfig
            
            foreach ($bot in $bots) {
                # Skip bots that should be offline
                if ($bot.status -eq "offline") {
                    continue
                }
                
                # Check if bot process is still running
                if ($runningBots[$bot.id]) {
                    $process = $runningBots[$bot.id]
                    
                    if ($process.HasExited) {
                        Write-Log "Bot $($bot.name) (ID: $($bot.id)) has crashed, restarting..." -Level "WARN"
                        $runningBots.Remove($bot.id)
                        Update-BotStatus -BotId $bot.id -Status "restarting"
                        
                        # Restart the bot
                        $newProcess = Start-DiscordBot -Bot $bot
                        if ($newProcess) {
                            $runningBots[$bot.id] = $newProcess
                            Update-BotStatus -BotId $bot.id -Status "online" -ProcessId $newProcess.Id
                        }
                        else {
                            Update-BotStatus -BotId $bot.id -Status "error"
                        }
                    }
                }
                # Start bot if it should be running but isn't
                elseif ($bot.status -in @("online", "starting")) {
                    Write-Log "Starting bot $($bot.name) (ID: $($bot.id))"
                    $process = Start-DiscordBot -Bot $bot
                    
                    if ($process) {
                        $runningBots[$bot.id] = $process
                        Update-BotStatus -BotId $bot.id -Status "online" -ProcessId $process.Id
                    }
                    else {
                        Update-BotStatus -BotId $bot.id -Status "error"
                    }
                }
            }
            
            # Remove any bots that are no longer in the config
            $botIds = $bots | Select-Object -ExpandProperty id
            $removedBots = $runningBots.Keys | Where-Object { $_ -notin $botIds }
            
            foreach ($botId in $removedBots) {
                Write-Log "Removing bot $botId from monitor"
                $process = $runningBots[$botId]
                
                if (-not $process.HasExited) {
                    Stop-DiscordBot -Bot @{ processId = $process.Id }
                }
                
                $runningBots.Remove($botId)
            }
            
            Start-Sleep -Seconds $CONFIG.CheckInterval
        }
        catch {
            Write-Log "Error in monitor loop: $_" -Level "ERROR"
            Start-Sleep -Seconds 5  # Short sleep on error before retrying
        }
    }
}

# Start the monitor
Start-BotMonitor
