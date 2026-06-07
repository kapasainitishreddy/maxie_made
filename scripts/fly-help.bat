@echo off
REM Common Fly.io CLI commands for Windows. Run from an app's apps\api directory.
REM Usage: fly-help.bat [section]
REM   Sections: setup, update, secrets, domain, monitor, troubleshoot, all (default)

if "%1"=="" goto all
if /i "%1"=="all" goto all
if /i "%1"=="setup" goto setup
if /i "%1"=="update" goto update
if /i "%1"=="secrets" goto secrets
if /i "%1"=="domain" goto domain
if /i "%1"=="monitor" goto monitor
if /i "%1"=="troubleshoot" goto troubleshoot

:all
call :setup
call :update
call :secrets
call :domain
call :monitor
call :troubleshoot
goto :eof

:setup
echo.
echo ============================================================
echo   First-time setup
echo ============================================================
echo.
echo   1. Install fly CLI: https://fly.io/docs/hands-on/install-flyctl/
echo   2. fly auth signup   (uses GitHub)
echo   3. Per app:
echo      cd pharmaip-radar\apps\api
echo      fly launch --name pharmaip-radar-api
echo      fly secrets set DATABASE_URL=postgresql+asyncpg://...
echo      fly secrets set CLERK_JWKS_URL=https://...
echo      fly deploy
goto :eof

:update
echo.
echo ============================================================
echo   Deploy updates
echo ============================================================
echo.
echo   fly deploy
echo   fly logs
echo   fly ssh console
echo   fly status
echo   fly apps list
goto :eof

:secrets
echo.
echo ============================================================
echo   Secrets management
echo ============================================================
echo.
echo   fly secrets list
echo   fly secrets set KEY=value
echo   fly secrets set KEY1=val1 KEY2=val2
echo   fly secrets unset KEY
goto :eof

:domain
echo.
echo ============================================================
echo   Custom domains
echo ============================================================
echo.
echo   fly certs create yourdomain.com
echo   fly certs list
echo   fly certs show yourdomain.com
goto :eof

:monitor
echo.
echo ============================================================
echo   Monitoring + scaling
echo ============================================================
echo.
echo   fly dashboard
echo   fly scale vm shared-cpu-1x --memory 256
echo   fly machines stop
echo   fly machines list
goto :eof

:troubleshoot
echo.
echo ============================================================
echo   Troubleshooting
echo ============================================================
echo.
echo   fly logs --build-only
echo   fly machines restart
echo   fly releases list
echo   fly releases rollback ^<version^>
echo   fly doctor
goto :eof
