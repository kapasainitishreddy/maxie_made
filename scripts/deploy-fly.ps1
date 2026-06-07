# deploy-fly.ps1 - Deploy all 4 SaaS backend APIs to Fly.io from this monorepo
# Usage: .\scripts\deploy-fly.ps1 [-DryRun]

param([switch]$DryRun)

$ErrorActionPreference = "Stop"

$Apps = @(
  @{ Name = "pharmaip-radar";      FlyName = "pharmaip-radar-api" },
  @{ Name = "cloudfinops-copilot"; FlyName = "cloudfinops-copilot-api" },
  @{ Name = "autohedge-pro";       FlyName = "autohedge-pro-api" },
  @{ Name = "quantalab";           FlyName = "quantalab-api" }
)

function Log($m)  { Write-Host "`n$m" -ForegroundColor Cyan }
function Ok($m)   { Write-Host "✓ $m" -ForegroundColor Green }
function Warn($m) { Write-Host "⚠ $m" -ForegroundColor Yellow }
function Err($m)  { Write-Host "✗ $m" -ForegroundColor Red }

Log "🔍 Preflight checks..."
if (-not (Get-Command fly -ErrorAction SilentlyContinue)) {
  Err "fly CLI not installed. Get it: https://fly.io/docs/hands-on/install-flyctl/"
  exit 1
}

$flyUser = fly auth whoami 2>&1 | Out-String
if ($flyUser -match "not logged in") {
  Err "Not logged in to Fly.io. Run: fly auth signup"
  exit 1
}
Ok "Logged in to Fly.io"

Log "🔑 Database + auth secrets (press Enter to skip)..."

$DatabaseUrl = $env:DATABASE_URL
$ClerkJwksUrl = $env:CLERK_JWKS_URL
$SentryDsn = $env:SENTRY_DSN
$PlausibleDomain = $env:NEXT_PUBLIC_PLAUSIBLE_DOMAIN

if (-not $DatabaseUrl) { Warn "No DATABASE_URL. App will use SQLite (dev only)." }
if (-not $ClerkJwksUrl) { Warn "No CLERK_JWKS_URL. Dev bypass mode (no auth)." }

Log "🚀 Deploying 4 backends to Fly.io..."

foreach ($app in $Apps) {
  $appName = $app.Name
  $flyName = $app.FlyName
  $apiDir = "$appName\apps\api"

  Log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  Log "📦 Deploying: $appName → $flyName"
  Log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  if (-not (Test-Path $apiDir)) { Err "Missing: $apiDir"; continue }
  Push-Location $apiDir

  # Create app if needed
  $appExists = fly apps list 2>&1 | Select-String $flyName
  if ($appExists) {
    Ok "App exists: $flyName"
  } else {
    if ($DryRun) {
      Write-Host "[dry-run] fly apps create $flyName" -ForegroundColor DarkGray
    } else {
      Log "Creating app: $flyName"
      fly apps create $flyName --org personal 2>&1 | Out-Null
    }
  }

  # Secrets
  Log "Setting secrets..."
  $secrets = @{ "APP_ENV" = "production" }
  if ($DatabaseUrl) { $secrets["DATABASE_URL"] = $DatabaseUrl }
  if ($ClerkJwksUrl) { $secrets["CLERK_JWKS_URL"] = $ClerkJwksUrl }
  if ($SentryDsn) { $secrets["SENTRY_DSN"] = $SentryDsn }
  if ($PlausibleDomain) { $secrets["PLAUSIBLE_DOMAIN"] = $PlausibleDomain }

  if ($DryRun) {
    foreach ($k in $secrets.Keys) { Write-Host "[dry-run] fly secrets set $k=***" -ForegroundColor DarkGray }
  } else {
    $secretArgs = ($secrets.GetEnumerator() | ForEach-Object { "$($_.Key)=$($_.Value)" }) -join " "
    fly secrets set $secretArgs 2>&1 | Out-Null
  }

  # Deploy
  if ($DryRun) {
    Write-Host "[dry-run] fly deploy" -ForegroundColor DarkGray
  } else {
    Log "Deploying..."
    fly deploy --remote-only 2>&1 | Select-Object -Last 10
    Ok "Deployed: https://$flyName.fly.dev"
  }

  Pop-Location
}

Log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Ok "🎉 All 4 backends deployed"
Log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Log ""
Log "📋 Summary:"
foreach ($app in $Apps) {
  Log "   • $($app.Name) → https://$($app.FlyName).fly.dev"
}
Log ""
Log "Next: update frontend NEXT_PUBLIC_API_URL env vars to point to these URLs"
