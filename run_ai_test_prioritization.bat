@echo off
REM Run the AI Test Prioritization main script.

CALL c:/Users/saura/OneDrive/Desktop/open_source_venv/Scripts/activate.bat

echo([32;40m==== Running AI Test Prioritization Script ====

python -m src.main

if %ERRORLEVEL% EQU 0 (
    echo([32;40m==== AI Test Prioritization Completed Successfully ==== [0m
    exit /b 0
) else (
    echo([31;40m==== AI Test Prioritization Failed ==== [0m
    exit /b 1
)
