@echo off
REM Build the HWP Parser Docker image

echo Building HWP Parser Docker image...
docker build -t hwp-parser .

if %ERRORLEVEL% EQU 0 (
    echo Build successful!
    echo You can now run the parser with:
    echo   parse.bat your-file.hwp
) else (
    echo Build failed!
    exit /b 1
)
