#Requires -Version 5.1
<#
.SYNOPSIS
  One-click setup: silently installs Orange 3.40.0 (if not already installed)
  and then applies the Korean language pack. For colleague teachers who don't
  have Orange yet, or want everything done in a single step.

.DESCRIPTION
  Run this script from inside the unzipped language pack folder, with the
  official installer "Orange3-3.40.0-x86_64.exe" copied into the SAME folder
  (or pass -InstallerPath). It self-elevates (UAC prompt) once for the whole
  process.

  IMPORTANT: Orange's installer (built with conda's "constructor") fails
  silently when the install path contains non-ASCII characters (Korean
  letters included) or is missing - this includes the default "install for
  me only" location under C:\Users\<name>\... when the Windows user name has
  Korean characters, which is common on Korean school PCs. To sidestep this,
  this script always installs to a plain ASCII path with no spaces
  (default: C:\Orange). Do not change -InstallPath to a path with spaces or
  non-ASCII characters.

.PARAMETER InstallerPath
  Path to "Orange3-3.40.0-x86_64.exe". Default: look for it next to this
  script.

.PARAMETER InstallPath
  Where to install Orange. Default: "C:\Orange". Must be ASCII-only, no
  spaces (see IMPORTANT above).

.PARAMETER SkipLanguageSwitch
  If set, does not change the current user's language setting or turn off
  update checks; only installs Orange and copies the translated files.
#>
param(
    [string]$InstallerPath,
    [string]$InstallPath = "C:\Orange",
    [switch]$SkipLanguageSwitch,
    [switch]$Elevated  # internal: set when this is the re-invoked elevated instance
)

$ErrorActionPreference = "Stop"
$RequiredVersion = "3.40.0"

function Wait-BeforeExit {
    Write-Host ""
    Write-Host "(Window stays open - press Enter to close it.)"
    try { Read-Host | Out-Null } catch { Start-Sleep -Seconds 5 }
}

if ($InstallPath -match '[^\x00-\x7F]') {
    Write-Host "ERROR: -InstallPath must be ASCII-only (no Korean or other non-English characters). Got: $InstallPath"
    Wait-BeforeExit
    exit 1
}
if ($InstallPath -match ' ') {
    Write-Host "ERROR: -InstallPath must not contain spaces (NSIS silent-install limitation). Got: $InstallPath"
    Wait-BeforeExit
    exit 1
}

if (-not $Elevated) {
    $currentPrincipal = New-Object Security.Principal.WindowsPrincipal(
        [Security.Principal.WindowsIdentity]::GetCurrent())
    if (-not $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)) {
        Write-Host "Requesting administrator privileges (look for a UAC prompt)..."
        $argList = @("-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "`"$PSCommandPath`"",
                    "-InstallPath", "`"$InstallPath`"", "-Elevated")
        if ($InstallerPath) { $argList += @("-InstallerPath", "`"$InstallerPath`"") }
        if ($SkipLanguageSwitch) { $argList += "-SkipLanguageSwitch" }
        try {
            $p = Start-Process powershell -Verb RunAs -ArgumentList $argList -Wait -PassThru
            if ($p.ExitCode -ne 0) {
                Write-Host "The elevated installer window reported an error (exit code $($p.ExitCode)). Check that window, or re-run from an already-open Administrator PowerShell."
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

function Get-InstalledVersions([string]$Root) {
    $py = Join-Path $Root "python.exe"
    if (-not (Test-Path $py)) { return $null }
    $checkScript = @"
import importlib.metadata as m, json
try:
    print(json.dumps({p: m.version(p) for p in ('Orange3','orange-canvas-core','orange-widget-base')}))
except Exception as e:
    print(json.dumps({"error": str(e)}))
"@
    try { return (& $py -c $checkScript | ConvertFrom-Json) } catch { return $null }
}

# ---- install Orange if needed --------------------------------------------
$versions = Get-InstalledVersions $InstallPath
if ($versions -and $versions.Orange3 -eq $RequiredVersion) {
    Write-Host "Orange $RequiredVersion is already installed at $InstallPath - skipping installer."
} else {
    if (Test-Path $InstallPath) {
        Write-Error "$InstallPath exists but does not contain a matching Orange $RequiredVersion install. Remove or rename that folder first, or choose a different -InstallPath."
    }
    if (-not $InstallerPath) {
        $InstallerPath = Join-Path $packDir "Orange3-$RequiredVersion-x86_64.exe"
    }
    if (-not (Test-Path $InstallerPath)) {
        Write-Error "Installer not found at '$InstallerPath'. Copy Orange3-$RequiredVersion-x86_64.exe next to this script, or pass -InstallerPath."
    }
    Write-Host "Installing Orange $RequiredVersion silently to $InstallPath ..."
    Write-Host "  (normally 3-10 minutes and about 90,000 files / 2.5 GB - this window will print progress every 10 seconds)"
    $proc = Start-Process -FilePath $InstallerPath -ArgumentList "/S", "/D=$InstallPath" -PassThru
    $lastCount = -1
    $stillCount = 0
    while (-not $proc.HasExited) {
        Start-Sleep -Seconds 10
        $fileCount = 0
        if (Test-Path $InstallPath) {
            $fileCount = (Get-ChildItem -LiteralPath $InstallPath -Recurse -File -ErrorAction SilentlyContinue | Measure-Object).Count
        }
        if ($fileCount -ne $lastCount) {
            Write-Host "  ... $fileCount files copied so far"
            $lastCount = $fileCount
            $stillCount = 0
        } else {
            $stillCount++
            Write-Host "  ... still at $fileCount files ($($stillCount * 10)s with no change)"
        }
    }
    $proc.WaitForExit()
    if ($proc.ExitCode -ne 0) {
        Write-Error "Installer exited with code $($proc.ExitCode). See $env:TEMP\$(Split-Path $InstallerPath -Leaf)-install-log.txt for details."
    }
    $versions = Get-InstalledVersions $InstallPath
    if (-not $versions -or $versions.Orange3 -ne $RequiredVersion) {
        Write-Error "Installer finished but Orange $RequiredVersion was not found at $InstallPath afterwards. See $env:TEMP\$(Split-Path $InstallerPath -Leaf)-install-log.txt for details."
    }
    Write-Host "  Orange $($versions.Orange3) installed."
}
Write-Host "  orange-canvas-core $($versions.'orange-canvas-core'), orange-widget-base $($versions.'orange-widget-base')"

} catch {
    Write-Host ""
    Write-Host "ERROR: $($_.Exception.Message)"
    Write-Host $_.ScriptStackTrace
    Wait-BeforeExit
    exit 1
}

# ---- apply the Korean language pack (reuses install_ko.ps1) --------------
try {
    $installKo = Join-Path $packDir "install_ko.ps1"
    if (-not (Test-Path $installKo)) {
        throw "install_ko.ps1 not found next to this script in $packDir."
    }
    $langArgs = @{ InstallPath = $InstallPath; Elevated = $true }
    if ($SkipLanguageSwitch) { $langArgs["SkipLanguageSwitch"] = $true }
    & $installKo @langArgs
    if ($LASTEXITCODE -and $LASTEXITCODE -ne 0) {
        throw "install_ko.ps1 exited with code $LASTEXITCODE."
    }
} catch {
    # install_ko.ps1 already pauses on its own (success or failure) via its
    # own finally block; only pause here for errors it never got to raise,
    # e.g. the file being missing.
    Write-Host ""
    Write-Host "ERROR applying the language pack: $($_.Exception.Message)"
    Write-Host $_.ScriptStackTrace
    Wait-BeforeExit
    exit 1
}
