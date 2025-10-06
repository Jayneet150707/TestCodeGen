# PowerShell script to install Fundamento API Service
# Run this script as Administrator

param(
    [Parameter(Mandatory=$false)]
    [string]$ServiceName = "FundamentoApiService",
    
    [Parameter(Mandatory=$false)]
    [string]$DisplayName = "Fundamento API Service",
    
    [Parameter(Mandatory=$false)]
    [string]$Description = "Windows Service that calls Fundamento APIs daily and saves responses",
    
    [Parameter(Mandatory=$false)]
    [string]$ExecutablePath = "$PSScriptRoot\bin\Release\net8.0\win-x64\publish\FundamentoApiService.exe"
)

# Check if running as Administrator
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
$isAdmin = $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Please right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Fundamento API Service Installer" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if executable exists
if (-not (Test-Path $ExecutablePath)) {
    Write-Host "ERROR: Executable not found at: $ExecutablePath" -ForegroundColor Red
    Write-Host "Please build the project first using:" -ForegroundColor Yellow
    Write-Host "  dotnet publish -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true" -ForegroundColor Yellow
    exit 1
}

Write-Host "Executable found: $ExecutablePath" -ForegroundColor Green

# Check if service already exists
$existingService = Get-Service -Name $ServiceName -ErrorAction SilentlyContinue

if ($existingService) {
    Write-Host ""
    Write-Host "Service '$ServiceName' already exists!" -ForegroundColor Yellow
    $response = Read-Host "Do you want to reinstall it? This will stop and delete the existing service. (Y/N)"
    
    if ($response -eq 'Y' -or $response -eq 'y') {
        Write-Host "Stopping existing service..." -ForegroundColor Yellow
        Stop-Service -Name $ServiceName -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 2
        
        Write-Host "Deleting existing service..." -ForegroundColor Yellow
        sc.exe delete $ServiceName
        Start-Sleep -Seconds 2
        Write-Host "Existing service removed." -ForegroundColor Green
    } else {
        Write-Host "Installation cancelled." -ForegroundColor Yellow
        exit 0
    }
}

# Create the service
Write-Host ""
Write-Host "Installing service..." -ForegroundColor Cyan
$createResult = sc.exe create $ServiceName binPath= $ExecutablePath start= auto DisplayName= $DisplayName

if ($LASTEXITCODE -eq 0) {
    Write-Host "Service created successfully!" -ForegroundColor Green
    
    # Set description
    sc.exe description $ServiceName $Description
    
    # Start the service
    Write-Host ""
    $startResponse = Read-Host "Do you want to start the service now? (Y/N)"
    
    if ($startResponse -eq 'Y' -or $startResponse -eq 'y') {
        Write-Host "Starting service..." -ForegroundColor Cyan
        Start-Service -Name $ServiceName
        Start-Sleep -Seconds 2
        
        $service = Get-Service -Name $ServiceName
        if ($service.Status -eq 'Running') {
            Write-Host "Service started successfully!" -ForegroundColor Green
        } else {
            Write-Host "Warning: Service status is $($service.Status)" -ForegroundColor Yellow
        }
    }
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Installation Complete!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Service Name: $ServiceName" -ForegroundColor White
    Write-Host "Display Name: $DisplayName" -ForegroundColor White
    Write-Host "Executable: $ExecutablePath" -ForegroundColor White
    Write-Host ""
    Write-Host "Useful commands:" -ForegroundColor Cyan
    Write-Host "  Start service:   net start $ServiceName" -ForegroundColor White
    Write-Host "  Stop service:    net stop $ServiceName" -ForegroundColor White
    Write-Host "  Check status:    Get-Service $ServiceName" -ForegroundColor White
    Write-Host "  View logs:       Check the logs/ directory" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "ERROR: Failed to create service!" -ForegroundColor Red
    Write-Host "Error code: $LASTEXITCODE" -ForegroundColor Red
    exit 1
}
