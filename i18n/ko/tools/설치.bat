@echo off
setlocal
REM One-click launcher for install_orange_ko.ps1: installs Orange 3.40.0 (if
REM needed) and applies the Korean language pack in one step. Keep this file
REM pure ASCII - cmd.exe reads it with the system code page (cp949), so any
REM UTF-8 Korean text in here would be misparsed.
title Orange Korean Setup

set "SCRIPT_DIR=%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%install_orange_ko.ps1" %*
echo.
pause
