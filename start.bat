@echo off
echo Starting PerfumeShop AI...

start "Backend  - http://localhost:8000" cmd /k "cd /d "%~dp0" && uvicorn main:app --reload"
start "Frontend - http://localhost:5173" cmd /k "cd /d "%~dp0frontend" && pnpm dev"

echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
