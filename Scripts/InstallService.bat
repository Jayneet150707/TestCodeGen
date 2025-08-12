@echo off
echo Installing Email Service...

REM Stop the service if it's running
sc stop "Email Sending Service" 2>nul

REM Delete the service if it exists
sc delete "Email Sending Service" 2>nul

REM Create the service
sc create "Email Sending Service" binPath= "%~dp0EmailService.exe" start= auto DisplayName= "Email Sending Service"

REM Set service description
sc description "Email Sending Service" "Windows service for sending emails with attachments"

REM Start the service
sc start "Email Sending Service"

echo Service installed and started successfully!
pause

