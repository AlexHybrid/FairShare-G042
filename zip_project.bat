@echo off
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File .\zip_project.ps1
