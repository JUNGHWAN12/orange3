@echo off
chcp 65001 >nul
REM Runs after Orange's packages are installed and linked (constructor
REM guarantees this ordering for post_install, unlike extra_files/pre_install).
REM Overlays the Korean translation staged by extra_files under
REM %PREFIX%\_korean_langpack, then removes the staging copy.

set STAGE=%PREFIX%\_korean_langpack
set DEST=%PREFIX%\Lib\site-packages

if not exist "%STAGE%" (
    echo Korean language pack staging folder not found, skipping.
    goto :eof
)

echo Applying Korean translation...
xcopy "%STAGE%\Orange" "%DEST%\Orange" /E /H /Y /I >nul
xcopy "%STAGE%\orangecanvas" "%DEST%\orangecanvas" /E /H /Y /I >nul
xcopy "%STAGE%\orangewidget" "%DEST%\orangewidget" /E /H /Y /I >nul

rmdir /S /Q "%STAGE%"

REM Set the current user's language to Korean and turn off update checks,
REM the same as install_ko.ps1 does for the two-file deployment. Only
REM writes a fresh Orange.ini - never overwrites an existing one.
set INI_DIR=%APPDATA%\biolab.si
set INI=%INI_DIR%\Orange.ini
if not exist "%INI%" (
    if not exist "%INI_DIR%" mkdir "%INI_DIR%"
    (
        echo [application]
        echo language=한국어
        echo [startup]
        echo check-updates=false
    ) > "%INI%"
)

echo Korean translation applied.
