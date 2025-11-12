# Quick Setup and Run Script for Windows PowerShell
# Run this script to automatically set up and start the application

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Educational Institute Website Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✓ $pythonVersion found" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.7 or higher." -ForegroundColor Red
    exit 1
}

Write-Host ""

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Initialize database
Write-Host "Initializing database with sample data..." -ForegroundColor Yellow
python init_db.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Database initialized successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to initialize database" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete! Starting the server..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "The application will be available at: http://localhost:5000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the Flask application
python app.py
