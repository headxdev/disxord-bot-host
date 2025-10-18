@echo off
REM Discord Bot Manager Service Starter
REM Created by headx and the psychon
title Discord Bot Manager Service

REM Check if running with admin rights
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo This script needs to be run as Administrator.
    echo Please right-click and select "Run as administrator"
    pause
    exit /b 1
)

echo =====================================
echo Discord Bot Manager Service Starter
echo Created by headx and the psychon
echo =====================================
echo.

REM Create logs directory if it doesn't exist
if not exist logs mkdir logs

REM Start the PowerShell monitor script
echo Starting service monitor...
PowerShell.exe -ExecutionPolicy Bypass -NoProfile -File "%~dp0service_monitor.ps1"
