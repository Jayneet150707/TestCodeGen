# Fundamento API Service

A Windows Service that calls Fundamento APIs daily and saves responses to files.

## Features

- **Automated Daily Execution**: Runs automatically at 2:00 AM every day
- **Multiple API Endpoints**: Calls Pre Due, Post Due, EMI, and Onboarding APIs
- **Response Logging**: Saves all API responses to dated files
- **Error Handling**: Comprehensive error logging and recovery
- **Windows Service**: Runs as a background Windows service

## API Endpoints

### Pre Due APIs
- `dayToDue=0`
- `dayToDue=1`
- `dayToDue=3`

### Post Due APIs
- `dayRange=2`
- `dayRange=3`
- `dayRange=4`
- `dayRange=5`

### EMI Collected API
- Previous day's data

### Onboarding APIs
- `type=ONBOARD`
- `type=REJECT`
- `type=SANCTION`

## File Naming Convention

Response files are saved with the following naming format:

```
Predue_response_0_dd-MMMM-yyyy.txt
Predue_response_1_dd-MMMM-yyyy.txt
Predue_response_3_dd-MMMM-yyyy.txt
Postdue_response_2_dd-MMMM-yyyy.txt
Postdue_response_3_dd-MMMM-yyyy.txt
Postdue_response_4_dd-MMMM-yyyy.txt
Postdue_response_5_dd-MMMM-yyyy.txt
EMI_response_dd-MMMM-yyyy.txt
Onboard_response_ONBOARD_dd-MMMM-yyyy.txt
Onboard_response_REJECT_dd-MMMM-yyyy.txt
Onboard_response_SANCTION_dd-MMMM-yyyy.txt
```

Example: `Predue_response_0_06-October-2025.txt`

## Building the Application

### Prerequisites
- .NET 8.0 SDK or later
- Windows OS

### Build Commands

```bash
# Navigate to project directory
cd FundamentoApiService

# Restore dependencies
dotnet restore

# Build the project
dotnet build

# Publish as single executable
dotnet publish -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true
```

The executable will be created in:
```
bin/Release/net8.0/win-x64/publish/FundamentoApiService.exe
```

## Installation as Windows Service

### Option 1: Using PowerShell Script (Recommended)

1. Build the project first using `build-and-publish.ps1`:
   ```powershell
   .\build-and-publish.ps1
   ```

2. Run PowerShell as Administrator and execute:
   ```powershell
   .\install-service.ps1
   ```

### Option 2: Manual Installation

Run PowerShell as Administrator:

```powershell
# Create the service
sc.exe create "FundamentoApiService" binPath="C:\Path\To\FundamentoApiService.exe" start=auto

# Start the service
sc.exe start "FundamentoApiService"

# Check service status
sc.exe query "FundamentoApiService"
```

## Managing the Service

### Start the Service
```powershell
sc.exe start "FundamentoApiService"
# or
net start "FundamentoApiService"
```

### Stop the Service
```powershell
sc.exe stop "FundamentoApiService"
# or
net stop "FundamentoApiService"
```

### Delete the Service
```powershell
# Use the uninstall script
.\uninstall-service.ps1

# Or manually
sc.exe delete "FundamentoApiService"
```

### View Service Status
```powershell
sc.exe query "FundamentoApiService"
# or
Get-Service "FundamentoApiService"
```

## Configuration

### Changing Execution Time

Edit `Worker.cs` to modify the daily execution time:

```csharp
private readonly TimeSpan _dailyExecutionTime = new TimeSpan(2, 0, 0); // 2:00 AM
```

Change the values to your desired time (Hours, Minutes, Seconds).

### Changing Response Directory

Edit `ApiService.cs`:

```csharp
private readonly string _responseDirectory = "ApiResponses";
```

## Logs

Logs are stored in:
- **Console**: When running in development
- **File**: `logs/fundamento-service-yyyy-MM-dd.txt`

Log files are automatically rotated daily.

## Directory Structure

```
FundamentoApiService/
├── ApiResponses/          # API response files (created automatically)
├── logs/                  # Service logs (created automatically)
├── ApiService.cs          # API calling logic
├── Worker.cs              # Background service worker
├── Program.cs             # Application entry point
├── appsettings.json       # Configuration file
└── FundamentoApiService.csproj
```

## Troubleshooting

### Service Won't Start
1. Check Event Viewer (Windows Logs > Application)
2. Verify the executable path is correct
3. Ensure .NET 8.0 Runtime is installed (if not self-contained)
4. Check file permissions for the service account

### API Calls Failing
1. Check logs in the `logs/` directory
2. Verify network connectivity to `sms.paisalo.in:979`
3. Check firewall settings
4. Verify SSL/TLS certificates

### Response Files Not Created
1. Check write permissions for the `ApiResponses/` directory
2. Review error logs in `logs/` directory
3. Ensure adequate disk space

## Development

### Running Locally (Not as Service)

```bash
dotnet run
```

This will execute the service once immediately for testing purposes.

### Testing Individual API Calls

You can modify `Worker.cs` to call `ExecuteDailyTasks` immediately on startup for testing:

```csharp
// Execute immediately on service start
await ExecuteDailyTasks(stoppingToken);
```

## Security Notes

- The service uses HTTPS for all API calls
- Ensure proper network security and firewall rules
- Response files may contain sensitive data - secure the directory appropriately
- Run the service with minimal required permissions

## Support

For issues or questions, please contact the development team or check the logs for detailed error information.
