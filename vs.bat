@echo off
set CONDAPATH=E:\miniconda3
set ENVNAME=replay_tool

if "%ENVNAME%"=="base" (
    set ENVPATH=%CONDAPATH%
) else (
    set ENVPATH=%CONDAPATH%\envs\%ENVNAME%
)

call %CONDAPATH%\Scripts\activate.bat %ENVPATH%

cd /d "%~dp0"
code .
