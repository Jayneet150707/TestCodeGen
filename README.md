# Email Sending Windows Service

A robust Windows service built with C# .NET 8 for sending emails with attachments. The service processes emails from a queue system and supports various email features including HTML content, multiple recipients, and file attachments.

## Features

- ✅ **Windows Service**: Runs as a background Windows service
- ✅ **Email Queue System**: File-based queue for reliable email processing
- ✅ **Attachment Support**: Send emails with multiple file attachments
- ✅ **HTML & Text Emails**: Support for both HTML and plain text content
- ✅ **Priority Processing**: High, normal, and low priority email handling
- ✅ **Multiple Recipients**: Support for To, CC, and BCC recipients
- ✅ **Error Handling**: Robust error handling with retry mechanisms
- ✅ **Logging**: Comprehensive logging to Windows Event Log and console
- ✅ **Configuration**: JSON-based configuration management

## Project Structure

```
EmailService/
├── Models/
│   ├── EmailConfiguration.cs    # Configuration model
│   └── EmailRequest.cs          # Email request model
├── Services/
│   ├── IEmailSender.cs          # Email sender interface
│   ├── EmailSender.cs           # Email sending implementation
│   └── EmailWorkerService.cs    # Background service worker
├── Utils/
│   └── EmailQueueHelper.cs      # Helper for queuing emails
├── Examples/
│   └── TestEmailSender.cs       # Example usage
├── Scripts/
│   ├── InstallService.bat       # Service installation script
│   └── UninstallService.bat     # Service uninstallation script
├── Program.cs                   # Application entry point
├── appsettings.json            # Configuration file
└── EmailService.csproj         # Project file
```

## Configuration

Update the `appsettings.json` file with your email settings:

```json
{
  "EmailConfiguration": {
    "SmtpServer": "smtp.gmail.com",
    "SmtpPort": 587,
    "SmtpUsername": "your-email@gmail.com",
    "SmtpPassword": "your-app-password",
    "EnableSsl": true,
    "FromEmail": "your-email@gmail.com",
    "FromName": "Email Service",
    "ProcessIntervalMinutes": 5,
    "AttachmentFolder": "C:\\EmailAttachments",
    "ProcessedFolder": "C:\\EmailAttachments\\Processed",
    "ErrorFolder": "C:\\EmailAttachments\\Error"
  }
}
```

### Gmail Configuration

For Gmail, you'll need to:
1. Enable 2-factor authentication
2. Generate an App Password
3. Use the App Password in the `SmtpPassword` field

## Installation

### Prerequisites

- .NET 8.0 Runtime
- Windows OS
- Administrator privileges for service installation

### Build the Project

```bash
dotnet build --configuration Release
```

### Install as Windows Service

1. Run the build command to create the executable
2. Copy the output files to your desired installation directory
3. Run `Scripts/InstallService.bat` as Administrator
4. The service will be installed and started automatically

### Manual Installation

```cmd
sc create "Email Sending Service" binPath= "C:\Path\To\EmailService.exe" start= auto
sc start "Email Sending Service"
```

## Usage

### Queuing Emails Programmatically

```csharp
using EmailService.Models;
using EmailService.Utils;

// Create an email request
var emailRequest = new EmailRequest
{
    To = "recipient@example.com",
    Cc = "cc@example.com",
    Subject = "Test Email",
    Body = "<h1>Hello World!</h1><p>This is a test email.</p>",
    IsHtml = true,
    Priority = 1, // High priority
    Attachments = new List<string> { @"C:\path\to\file.pdf" }
};

// Queue the email
var queueFolder = @"C:\EmailAttachments\Queue";
await EmailQueueHelper.QueueEmailAsync(queueFolder, emailRequest);
```

### Email Priority Levels

- **1**: High Priority (processed first)
- **2**: Normal Priority (default)
- **3**: Low Priority (processed last)

### Folder Structure

The service creates and monitors these folders:

- **Queue**: Contains pending emails to be sent
- **Processed**: Successfully sent emails are moved here
- **Error**: Failed emails are moved here for investigation

## Monitoring

### Windows Event Log

The service logs to the Windows Event Log under "Application" with source "EmailService".

### Log Levels

- **Information**: Normal operations, successful email sends
- **Warning**: Non-critical issues, missing attachments
- **Error**: Failed email sends, configuration issues

## Troubleshooting

### Common Issues

1. **Service won't start**
   - Check if .NET 8 runtime is installed
   - Verify configuration file exists and is valid
   - Check Windows Event Log for error details

2. **Emails not sending**
   - Verify SMTP settings in appsettings.json
   - Check firewall settings for SMTP port
   - Ensure email credentials are correct

3. **Attachments not found**
   - Verify file paths in EmailRequest.Attachments
   - Check file permissions
   - Ensure files exist before queuing

### Testing

Run the example test application:

```bash
dotnet run --project Examples/TestEmailSender.cs
```

## Uninstallation

Run `Scripts/UninstallService.bat` as Administrator, or manually:

```cmd
sc stop "Email Sending Service"
sc delete "Email Sending Service"
```

## Development

### Adding New Features

1. Implement new functionality in the Services folder
2. Update the EmailConfiguration model if needed
3. Add appropriate logging
4. Update this README

### Testing

Create test email requests using the EmailQueueHelper utility class and monitor the service logs for processing results.

## License

This project is provided as-is for educational and commercial use.

