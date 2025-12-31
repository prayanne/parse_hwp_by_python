@echo off
REM Convenience script for parsing HWP files on Windows

if "%~1"=="" (
    echo Usage: %~nx0 ^<hwp-file^> [mode] [output]
    echo.
    echo Examples:
    echo   %~nx0 data\sample.hwp                    # Extract text to stdout
    echo   %~nx0 data\sample.hwp text               # Extract text to stdout
    echo   %~nx0 data\sample.hwp json result.json   # Export to JSON
    echo   %~nx0 data\sample.hwp tables tables.json # Extract tables
    echo.
    echo Modes: text ^(default^), json, tables
    exit /b 1
)

set HWP_FILE=%~1
set MODE=%~2
if "%MODE%"=="" set MODE=text
set OUTPUT=%~3

REM Get filename from path
for %%F in ("%HWP_FILE%") do set FILENAME=%%~nxF
set CONTAINER_INPUT=/app/data/%FILENAME%

REM Ensure directories exist
if not exist data mkdir data
if not exist output mkdir output

REM Check if file exists
if not exist "%HWP_FILE%" (
    echo Error: File not found: %HWP_FILE%
    exit /b 1
)

REM Copy file to data directory if not already there
echo %HWP_FILE% | findstr /i "^data\\" >nul
if errorlevel 1 (
    copy "%HWP_FILE%" "data\%FILENAME%" >nul
)

REM Build command
set CMD=docker run --rm -v "%cd%/data:/app/data" -v "%cd%/output:/app/output" hwp-parser --input %CONTAINER_INPUT% --mode %MODE%

REM Add output if specified
if not "%OUTPUT%"=="" (
    set CMD=%CMD% --output /app/output/%OUTPUT%
)

echo Running: %CMD%
%CMD%
