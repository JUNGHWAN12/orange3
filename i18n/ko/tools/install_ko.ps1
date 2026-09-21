#Requires -Version 5.1
<#
.SYNOPSIS
  Installs the Korean language pack onto an existing Orange installation by
  overlaying translated .py files and i18n/*.json. Never touches compiled
  extensions (.pyd) or anything else.

.DESCRIPTION
  Run this script from inside the unzipped language pack folder (it expects
  Orange\, orangecanvas\, orangewidget\ and manifest.json next to it).
  It self-elevates (UAC prompt) if not already running as Administrator.

  Safety:
  - Backs up every file it is about to overwrite into Backup-<timestamp>.zip
    in this same folder before copying anything.
  - Refuses to run if the installed Orange3 version doesn't match the
    language pack's version.

.PARAMETER InstallPath
  Root of the Orange installation. Default: "C:\Program Files\Orange".

.PARAMETER SkipLanguageSwitch
  If set, does not change the current user's language setting or turn off
  update checks; only copies the translated files.
#>
param(
    [string]$InstallPath = "C:\Program Files\Orange",
    [switch]$SkipLanguageSwitch,
    [switch]$Elevated  # internal: set when this is the re-invoked elevated instance
)

$ErrorActionPreference = "Stop"

function Wait-BeforeExit {
    Write-Host ""
    Write-Host "(Window stays open - press Enter to close it.)"
    try { Read-Host | Out-Null } catch { Start-Sleep -Seconds 5 }
}

# ---- self-elevate --------------------------------------------------------
# Re-invoked (elevated) instances carry this flag so they don't try to
# elevate again and so they pause themselves before closing.
if (-not $Elevated) {
    $currentPrincipal = New-Object Security.Principal.WindowsPrincipal(
        [Security.Principal.WindowsIdentity]::GetCurrent())
    if (-not $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)) {
        Write-Host "Requesting administrator privileges (look for a UAC prompt)..."
        $argList = @("-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "`"$PSCommandPath`"",
                    "-InstallPath", "`"$InstallPath`"", "-Elevated")
        if ($SkipLanguageSwitch) { $argList += "-SkipLanguageSwitch" }
        try {
            $p = Start-Process powershell -Verb RunAs -ArgumentList $argList -Wait -PassThru
            if ($p.ExitCode -ne 0) {
                Write-Host "The elevated installer window reported an error (exit code $($p.ExitCode)). Scroll up in that window, or re-run this script from an already-open Administrator PowerShell window to see the full output."
            } else {
                Write-Host "Elevated installer finished. Check the other window for details."
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
$manifestPath = Join-Path $packDir "manifest.json"
if (-not (Test-Path $manifestPath)) {
    Write-Error "manifest.json not found next to this script ($packDir). Run this script from inside the unzipped language pack folder."
}
$manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json
$packVersion = $manifest.version

$orangePython = Join-Path $InstallPath "python.exe"
if (-not (Test-Path $orangePython)) {
    Write-Error "Orange python.exe not found at '$orangePython'. Pass -InstallPath if Orange is installed elsewhere."
}

Write-Host "Checking installed Orange version..."
$checkScript = @"
import importlib.metadata as m, json
print(json.dumps({p: m.version(p) for p in ('Orange3','orange-canvas-core','orange-widget-base')}))
"@
$versions = & $orangePython -c $checkScript | ConvertFrom-Json
if ($versions.Orange3 -ne $packVersion) {
    Write-Error "Installed Orange3 is $($versions.Orange3), but this language pack is for $packVersion. Do not proceed - install the matching Orange version first."
}
Write-Host "  Orange3 $($versions.Orange3), orange-canvas-core $($versions.'orange-canvas-core'), orange-widget-base $($versions.'orange-widget-base') - OK"

$sitePackages = Join-Path $InstallPath "Lib\site-packages"
$packageMap = @{
    "Orange"        = "Orange"
    "orangecanvas"  = "orangecanvas"
    "orangewidget"  = "orangewidget"
}

# ---- back up files that will be overwritten -----------------------------
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backupDir = Join-Path $packDir "Backup-$stamp"
New-Item -ItemType Directory -Path $backupDir | Out-Null
Write-Host "Backing up files that will be replaced into $backupDir ..."

foreach ($pkg in $packageMap.Keys) {
    $srcPkgDir = Join-Path $packDir $pkg
    $dstPkgDir = Join-Path $sitePackages $packageMap[$pkg]
    if (-not (Test-Path $srcPkgDir)) { continue }
    Get-ChildItem -Path $srcPkgDir -Recurse -File | ForEach-Object {
        $rel = $_.FullName.Substring($srcPkgDir.Length + 1)
        $dstFile = Join-Path $dstPkgDir $rel
        if (Test-Path $dstFile) {
            $backupFile = Join-Path $backupDir "$pkg\$rel"
            New-Item -ItemType Directory -Path (Split-Path $backupFile) -Force | Out-Null
            Copy-Item $dstFile $backupFile
        }
    }
}
Compress-Archive -Path (Join-Path $backupDir "*") -DestinationPath (Join-Path $packDir "Backup-$stamp.zip")
Remove-Item -Recurse -Force $backupDir
Write-Host "  Backup saved: Backup-$stamp.zip"

# ---- copy translated files ----------------------------------------------
Write-Host "Installing Korean translation..."
$totalCopied = 0
foreach ($pkg in $packageMap.Keys) {
    $srcPkgDir = Join-Path $packDir $pkg
    $dstPkgDir = Join-Path $sitePackages $packageMap[$pkg]
    if (-not (Test-Path $srcPkgDir)) { continue }
    Get-ChildItem -Path $srcPkgDir -Recurse -File | ForEach-Object {
        $rel = $_.FullName.Substring($srcPkgDir.Length + 1)
        $dstFile = Join-Path $dstPkgDir $rel
        New-Item -ItemType Directory -Path (Split-Path $dstFile) -Force | Out-Null
        Copy-Item $_.FullName $dstFile -Force
        $totalCopied++
    }
}
Write-Host "  $totalCopied files copied."

# ---- switch language for the current user -------------------------------
if (-not $SkipLanguageSwitch) {
    $iniDir = Join-Path $env:APPDATA "biolab.si"
    New-Item -ItemType Directory -Path $iniDir -Force | Out-Null
    $iniPath = Join-Path $iniDir "Orange.ini"
    $lines = @()
    if (Test-Path $iniPath) { $lines = Get-Content $iniPath }

    function Set-IniValue([string[]]$Lines, [string]$Section, [string]$Key, [string]$Value) {
        $out = New-Object System.Collections.Generic.List[string]
        $inSection = $false
        $sectionSeen = $false
        $keySet = $false
        foreach ($line in $Lines) {
            if ($line -match '^\[(.+)\]$') {
                if ($inSection -and -not $keySet) {
                    $out.Add("$Key=$Value")
                    $keySet = $true
                }
                $inSection = ($matches[1] -eq $Section)
                if ($inSection) { $sectionSeen = $true }
                $out.Add($line)
                continue
            }
            if ($inSection -and $line -match "^$([regex]::Escape($Key))=") {
                $out.Add("$Key=$Value")
                $keySet = $true
                continue
            }
            $out.Add($line)
        }
        if ($inSection -and -not $keySet) { $out.Add("$Key=$Value") }
        if (-not $sectionSeen) {
            $out.Add("[$Section]")
            $out.Add("$Key=$Value")
        }
        return $out
    }

    $lines = Set-IniValue -Lines $lines -Section "application" -Key "language" -Value "한국어"
    $lines = Set-IniValue -Lines $lines -Section "startup" -Key "check-updates" -Value "false"
    Set-Content -Path $iniPath -Value $lines -Encoding UTF8
    Write-Host "  Language set to Korean for user '$env:USERNAME' (and update checks disabled)."
    Write-Host "  Settings file: $iniPath"
} else {
    Write-Host "  Skipped language switch (-SkipLanguageSwitch). Pick 한국어 in Preferences > General > Language."
}

Write-Host ""
Write-Host "Done. Close Orange completely and reopen it to see the Korean UI."
Write-Host "To undo: run uninstall_ko.ps1 from this same folder (as Administrator)."

} catch {
    Write-Host ""
    Write-Host "ERROR: $($_.Exception.Message)"
    Write-Host $_.ScriptStackTrace
} finally {
    Wait-BeforeExit
}
