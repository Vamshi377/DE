@echo off
setlocal EnableExtensions

set "KEY=%~1"

if "%KEY%"=="" (
    echo Usage: exam-answer key
    exit /b 1
)

set "RELATIVE_PATH=%KEY:/=\%.txt"
set "ANSWER_FILE=%~dp0answers\%RELATIVE_PATH%"

if not exist "%ANSWER_FILE%" (
    echo No answer saved for %KEY%
    exit /b 1
)

type "%ANSWER_FILE%"
exit /b 0
