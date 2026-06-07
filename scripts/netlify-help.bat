@echo off
REM Common Netlify CLI commands for Windows. Run from an app's apps\web directory.
REM Usage: netlify-help.bat [section]
REM   Sections: setup, update, env, domain, monitor, troubleshoot, all (default)

if "%1"=="" goto all
if /i "%1"=="all" goto all
if /i "%1"=="setup" goto setup
if /i "%1"=="update" goto update
if /i "%1"=="env" goto env
if /i "%1"=="domain" goto domain
if /i "%1"=="monitor" goto monitor
if /i "%1"=="troubleshoot" goto troubleshoot

:all
call :setup
call :update
call :env
call :domain
call :monitor
call :troubleshoot
goto :eof

:setup
echo.
echo ============================================================
echo   First-time setup (run from apps\web\)
echo ============================================================
echo.
echo   1. Log in to Netlify (opens browser)
echo      netlify login
echo.
echo   2. Create a new site (or link existing)
echo      netlify sites:create --name pharmaip-radar --ci
echo.
echo   3. Set environment variables
echo      netlify env:set NEXT_PUBLIC_API_URL https://pharmaip-radar.fly.dev
echo      netlify env:set NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY pk_live_xxxxx
echo.
echo   4. Deploy to production
echo      netlify deploy --prod
echo.
echo   5. Open the site in browser
echo      netlify open:site
goto :eof

:update
echo.
echo ============================================================
echo   Update an existing site
echo ============================================================
echo.
echo   git push origin main
echo   :: auto-deploys if connected to GitHub
echo.
echo   netlify deploy --prod
echo   netlify logs
echo   netlify deploy:list
goto :eof

:env
echo.
echo ============================================================
echo   Environment variables
echo ============================================================
echo.
echo   netlify env:list
echo   netlify env:set KEY value
echo   netlify env:import .env.production
echo   netlify env:get KEY
goto :eof

:domain
echo.
echo ============================================================
echo   Custom domains
echo ============================================================
echo.
echo   netlify domains:add yourdomain.com
echo   netlify domains:update yourdomain.com --primary
echo   netlify https:enable
goto :eof

:monitor
echo.
echo ============================================================
echo   Monitoring
echo ============================================================
echo.
echo   netlify logs --function=...
echo   netlify status
echo   netlify open
goto :eof

:troubleshoot
echo.
echo ============================================================
echo   Troubleshooting
echo ============================================================
echo.
echo   netlify build --clear-cache
echo   netlify dev
echo   netlify status
echo   netlify unlink
goto :eof
