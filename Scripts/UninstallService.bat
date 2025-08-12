@echo off
echo Uninstalling Email Service...

REM Stop the service
sc stop "Email Sending Service"

REM Delete the service
sc delete "Email Sending Service"

echo Service uninstalled successfully!
pause

