# PowerShell script to build and publish the Fundamento API Service

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Fundamento API Service - Build & Publish" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if .NET SDK is installed
$dotnetVersion = dotnet --version 2>$null

if (-not $dotnetVersion) {
    Write-Host "ERROR: .NET SDK is not installed!" -ForegroundColor Red
    Write-Host "Please install .NET 8.0 SDK or later from: https://dotnet.microsoft.com/download" -ForegroundColor Yellow
    exit 1
}

Write-Host "Detected .NET SDK version: $dotnetVersion" -ForegroundColor Green
Write-Host ""

# Navigate to project directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Clean previous builds
Write-Host "Cleaning previous builds..." -ForegroundColor Cyan
dotnet clean -c Release

if ($LASTEXITCODE -ne 0) {
    Write-Host "Warning: Clean command failed, continuing anyway..." -ForegroundColor Yellow
}

Write-Host ""

# Restore dependencies
Write-Host "Restoring dependencies..." -ForegroundColor Cyan
dotnet restore

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to restore dependencies!" -ForegroundColor Red
    exit 1
}

Write-Host "Dependencies restored successfully!" -ForegroundColor Green
Write-Host ""

# Build the project
Write-Host "Building project..." -ForegroundColor Cyan
dotnet build -c Release

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "Build successful!" -ForegroundColor Green
Write-Host ""

# Publish the project
Write-Host "Publishing single-file executable..." -ForegroundColor Cyan
dotnet publish -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true -p:PublishReadyToRun=true

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Publish failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Build & Publish Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$outputPath = Join-Path $scriptPath "bin\Release\net8.0\win-x64\publish\FundamentoApiService.exe"

if (Test-Path $outputPath) {
    Write-Host "Executable location:" -ForegroundColor Cyan
    Write-Host "  $outputPath" -ForegroundColor White
    
    $fileSize = (Get-Item $outputPath).Length / 1MB
    Write-Host ""
    Write-Host "File size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor White
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Run .\install-service.ps1 as Administrator to install the service" -ForegroundColor White
    Write-Host "  2. Or manually copy the executable to your desired location" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "Warning: Executable not found at expected location!" -ForegroundColor Yellow
}
