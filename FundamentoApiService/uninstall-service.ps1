# PowerShell script to uninstall Fundamento API Service
# Run this script as Administrator

param(
    [Parameter(Mandatory=$false)]
    [string]$ServiceName = "FundamentoApiService"
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
Write-Host "Fundamento API Service Uninstaller" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if service exists
$service = Get-Service -Name $ServiceName -ErrorAction SilentlyContinue

if (-not $service) {
    Write-Host "Service '$ServiceName' is not installed." -ForegroundColor Yellow
    exit 0
}

Write-Host "Service found: $ServiceName" -ForegroundColor White
Write-Host "Status: $($service.Status)" -ForegroundColor White
Write-Host ""

$response = Read-Host "Are you sure you want to uninstall this service? (Y/N)"

if ($response -ne 'Y' -and $response -ne 'y') {
    Write-Host "Uninstallation cancelled." -ForegroundColor Yellow
    exit 0
}

# Stop the service if running
if ($service.Status -eq 'Running') {
    Write-Host "Stopping service..." -ForegroundColor Yellow
    Stop-Service -Name $ServiceName -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
    Write-Host "Service stopped." -ForegroundColor Green
}

# Delete the service
Write-Host "Removing service..." -ForegroundColor Yellow
$deleteResult = sc.exe delete $ServiceName

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Service uninstalled successfully!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Note: Response files and logs have been preserved." -ForegroundColor Cyan
    Write-Host "If you want to remove them, manually delete:" -ForegroundColor Cyan
    Write-Host "  - ApiResponses/ directory" -ForegroundColor White
    Write-Host "  - logs/ directory" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "ERROR: Failed to delete service!" -ForegroundColor Red
    Write-Host "Error code: $LASTEXITCODE" -ForegroundColor Red
    exit 1
}
