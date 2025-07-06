@echo off
REM Run the AI Test Prioritization main script.

CALL c:/Users/saura/OneDrive/Desktop/open_source_venv/Scripts/activate.bat

echo([32m==== Running AI Test Prioritization ====

python -m src.main

if %ERRORLEVEL% EQU 0 (
    echo([32m==== AI Test Prioritization Completed Successfully ==== [0m
    exit /b 0
) else (
    echo([31m==== AI Test Prioritization Failed ==== [0m
    exit /b 1
)
