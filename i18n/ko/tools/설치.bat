@echo off
setlocal
REM One-click launcher for install_orange_ko.ps1: installs Orange 3.40.0 (if
REM needed) and applies the Korean language pack, in one step. Double-click
REM this file; no need to fight PowerShell's execution policy or right-click
REM menus.
title Orange 한국어 설치

set SCRIPT_DIR=%~dp0
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%install_orange_ko.ps1" %*
echo.
pause
