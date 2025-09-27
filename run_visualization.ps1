# PowerShell script to run the biomedical signal visualization

Write-Host "Biomedical Signal Visualization" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# Check if Python is available
$pythonCommands = @("python", "py", "python3")

foreach ($cmd in $pythonCommands) {
    try {
        $version = & $cmd --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Found Python: $cmd" -ForegroundColor Yellow
            Write-Host "Version: $version" -ForegroundColor Yellow
            
            # Install packages
            Write-Host "Installing required packages..." -ForegroundColor Yellow
            & $cmd -m pip install pandas plotly numpy
            
            # Run visualization
            Write-Host "Creating visualization..." -ForegroundColor Yellow
            & $cmd create_demo_html.py
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✓ Visualization created successfully!" -ForegroundColor Green
                Write-Host "✓ Opening biomedical_signals_demo.html..." -ForegroundColor Green
                Start-Process "biomedical_signals_demo.html"
                break
            }
        }
    }
    catch {
        # Continue to next command
    }
}

Write-Host "If the script didn't work, try running manually:" -ForegroundColor Cyan
Write-Host "1. Install Python from python.org" -ForegroundColor Cyan
Write-Host "2. Run: pip install pandas plotly numpy" -ForegroundColor Cyan
Write-Host "3. Run: python create_demo_html.py" -ForegroundColor Cyan

Read-Host "Press Enter to continue"
