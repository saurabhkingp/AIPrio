@echo off
REM Run the AI Test Prioritization main script.

REM Print start message in green (using ANSI escape code directly)
echo([32m==== Running AI Test Prioritization ====

REM Run the Python script
python -m src.main

REM Print end message based on exit code
if %ERRORLEVEL% EQU 0 (
    echo([32m==== AI Test Prioritization Completed Successfully ==== [0m
    exit /b 0
) else (
    echo([31m==== AI Test Prioritization Failed ==== [0m
    exit /b 1
)
