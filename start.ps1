# Launch FastAPI backend and Streamlit frontend

Write-Host "Starting Mealplanner application..." -ForegroundColor Green

# Store the original location
$originalLocation = Get-Location

try {
    # Start FastAPI backend in background
    Write-Host "Starting FastAPI backend..." -ForegroundColor Yellow
    Start-Job -Name "FastAPI" -ScriptBlock {
        Set-Location $using:originalLocation
        Set-Location "src/mealplanner/backend"
        uvicorn api:app --reload --host 127.0.0.1 --port 8000
    }
    
    # Give backend time to start
    Start-Sleep -Seconds 3
    
    # Check if FastAPI job is running
    $fastApiJob = Get-Job -Name "FastAPI"
    if ($fastApiJob.State -eq "Running") {
        Write-Host "FastAPI backend started successfully on http://127.0.0.1:8000" -ForegroundColor Green
        Write-Host "API docs available at http://127.0.0.1:8000/docs" -ForegroundColor Cyan
    } else {
        Write-Host "Failed to start FastAPI backend" -ForegroundColor Red
        Write-Host "Job output:" -ForegroundColor Red
        Receive-Job -Name "FastAPI"
        throw "Backend failed to start"
    }
    
    # Start Streamlit frontend
    Write-Host "Starting Streamlit dashboard..." -ForegroundColor Yellow
    streamlit run src/mealplanner/frontend/dashboard.py --server.port 8501
    
} catch {
    Write-Host "Error occurred: $_" -ForegroundColor Red
} finally {
    # Cleanup: Stop background jobs
    Write-Host "`nStopping background processes..." -ForegroundColor Yellow
    Get-Job -Name "FastAPI" -ErrorAction SilentlyContinue | Stop-Job
    Get-Job -Name "FastAPI" -ErrorAction SilentlyContinue | Remove-Job
    
    # Return to original location
    Set-Location $originalLocation
    Write-Host "Cleanup completed." -ForegroundColor Green
}