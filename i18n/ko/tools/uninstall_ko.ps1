#Requires -Version 5.1
<#
.SYNOPSIS
  Reverts install_ko.ps1: restores the original files from the newest
  Backup-*.zip in this folder, and switches the current user back to
  English.

.PARAMETER InstallPath
  Root of the Orange installation. Default: "C:\Program Files\Orange".
#>
param(
    [string]$InstallPath = "C:\Program Files\Orange",
    [switch]$Elevated  # internal: set when this is the re-invoked elevated instance
)

$ErrorActionPreference = "Stop"

function Wait-BeforeExit {
    Write-Host ""
    Write-Host "(Window stays open - press Enter to close it.)"
    try { Read-Host | Out-Null } catch { Start-Sleep -Seconds 5 }
}

if (-not $Elevated) {
    $currentPrincipal = New-Object Security.Principal.WindowsPrincipal(
        [Security.Principal.WindowsIdentity]::GetCurrent())
    if (-not $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)) {
        Write-Host "Requesting administrator privileges (look for a UAC prompt)..."
        try {
            $p = Start-Process powershell -Verb RunAs -ArgumentList @(
                "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "`"$PSCommandPath`"",
                "-InstallPath", "`"$InstallPath`"", "-Elevated") -Wait -PassThru
            if ($p.ExitCode -ne 0) {
                Write-Host "The elevated window reported an error (exit code $($p.ExitCode)). Check that window, or re-run from an already-open Administrator PowerShell."
            } else {
                Write-Host "Elevated window finished. Check the other window for details."
            }
        } catch {
            Write-Host "Could not start the elevated window: $($_.Exception.Message)"
            Write-Host "UAC prompt may have been cancelled. Try again, or open PowerShell as Administrator yourself and run: & `"$PSCommandPath`" -InstallPath `"$InstallPath`""
        }
        Wait-BeforeExit
        exit
    }
}

try {

$packDir = $PSScriptRoot
$backup = Get-ChildItem -Path $packDir -Filter "Backup-*.zip" |
    Sort-Object Name -Descending | Select-Object -First 1
if (-not $backup) {
    Write-Error "No Backup-*.zip found in $packDir. Nothing to restore."
}
Write-Host "Restoring from $($backup.Name) ..."

$tmp = Join-Path $env:TEMP "orange-ko-restore-$(Get-Date -Format yyyyMMddHHmmss)"
Expand-Archive -Path $backup.FullName -DestinationPath $tmp
$sitePackages = Join-Path $InstallPath "Lib\site-packages"

$n = 0
Get-ChildItem -Path $tmp -Recurse -File | ForEach-Object {
    $rel = $_.FullName.Substring($tmp.Length + 1)
    $dst = Join-Path $sitePackages $rel
    New-Item -ItemType Directory -Path (Split-Path $dst) -Force | Out-Null
    Copy-Item $_.FullName $dst -Force
    $n++
}
Remove-Item -Recurse -Force $tmp
Write-Host "  $n files restored."

$iniPath = Join-Path $env:APPDATA "biolab.si\Orange.ini"
if (Test-Path $iniPath) {
    (Get-Content $iniPath) -replace '^language=.*$', 'language=English' |
        Set-Content $iniPath -Encoding UTF8
    Write-Host "  Language reset to English for user '$env:USERNAME'."
}

Write-Host ""
Write-Host "Done. Close Orange completely and reopen it."

} catch {
    Write-Host ""
    Write-Host "ERROR: $($_.Exception.Message)"
    Write-Host $_.ScriptStackTrace
} finally {
    Wait-BeforeExit
}
