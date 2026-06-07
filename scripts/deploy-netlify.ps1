# deploy-netlify.ps1 - Deploy all 4 SaaS apps to Netlify from this monorepo
# Usage: .\scripts\deploy-netlify.ps1 [-DryRun]
#
# Prerequisites:
#   - netlify CLI installed: npm install -g netlify-cli
#   - netlify logged in: netlify login

param([switch]$DryRun)

$ErrorActionPreference = "Stop"

# --- Config ---
$Apps = @(
  @{ Name = "pharmaip-radar";     Subdomain = "pharmaip-radar.netlify.app";     ApiUrl = "https://pharmaip-radar.fly.dev" },
  @{ Name = "cloudfinops-copilot"; Subdomain = "cloudfinops-copilot.netlify.app"; ApiUrl = "https://cloudfinops-copilot.fly.dev" },
  @{ Name = "autohedge-pro";      Subdomain = "autohedge-pro.netlify.app";      ApiUrl = "https://autohedge-pro.fly.dev" },
  @{ Name = "quantalab";          Subdomain = "quantalab.netlify.app";          ApiUrl = "https://quantalab.fly.dev" }
)

# --- Helpers ---
function Log($msg)  { Write-Host "`n$msg" -ForegroundColor Cyan }
function Ok($msg)   { Write-Host "✓ $msg" -ForegroundColor Green }
function Warn($msg) { Write-Host "⚠ $msg" -ForegroundColor Yellow }
function Err($msg)  { Write-Host "✗ $msg" -ForegroundColor Red }

# --- Preflight ---
Log "🔍 Preflight checks..."

if (-not (Get-Command netlify -ErrorAction SilentlyContinue)) {
  Err "netlify CLI not installed. Run: npm install -g netlify-cli"
  exit 1
}
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
  Err "node not installed"
  exit 1
}

$netlifyStatus = netlify status 2>&1 | Out-String
if ($netlifyStatus -match "Not logged in") {
  Err "Not logged in to Netlify. Run: netlify login"
  exit 1
}
Ok "netlify CLI ready"

# --- Optional env vars (have dev-bypass fallbacks) ---
$ClerkKey = $env:NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY
$PlausibleDomain = $env:NEXT_PUBLIC_PLAUSIBLE_DOMAIN
$SentryDsn = $env:SENTRY_DSN

if (-not $ClerkKey) { Warn "No NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY — using dev bypass" }
if (-not $PlausibleDomain) { Warn "No NEXT_PUBLIC_PLAUSIBLE_DOMAIN — analytics disabled" }

# --- Deploy each app ---
Log "🚀 Deploying 4 apps to Netlify..."

foreach ($app in $Apps) {
  $appName = $app.Name
  $subdomain = $app.Subdomain
  $apiUrl = $app.ApiUrl
  $webDir = "$appName\apps\web"

  Log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  Log "📦 Deploying: $appName"
  Log "   Subdomain: $subdomain"
  Log "   API URL:   $apiUrl"
  Log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  if (-not (Test-Path $webDir)) {
    Err "Directory not found: $webDir"
    continue
  }

  Push-Location $webDir

  # Create or link site
  if (Test-Path ".netlify\state.json") {
    Ok "Site already linked"
  } else {
    if ($DryRun) {
      Write-Host "[dry-run] netlify sites:create --name $subdomain" -ForegroundColor DarkGray
    } else {
      Log "Creating site: $subdomain"
      try {
        netlify sites:create --name $subdomain --ci 2>&1 | Out-Null
      } catch {
        Warn "Site may exist, attempting to link..."
        netlify link --name $subdomain 2>&1 | Out-Null
      }
    }
  }

  # Set env vars
  Log "Setting environment variables..."
  $envVars = @{
    "NEXT_PUBLIC_API_URL" = $apiUrl
    "NEXT_PUBLIC_APP_NAME" = $appName
  }
  if ($ClerkKey) { $envVars["NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY"] = $ClerkKey }
  if ($PlausibleDomain) { $envVars["NEXT_PUBLIC_PLAUSIBLE_DOMAIN"] = $PlausibleDomain }
  if ($SentryDsn) { $envVars["SENTRY_DSN"] = $SentryDsn }

  foreach ($key in $envVars.Keys) {
    $value = $envVars[$key]
    if ($DryRun) {
      Write-Host "[dry-run] netlify env:set $key $value" -ForegroundColor DarkGray
    } else {
      netlify env:set $key $value 2>&1 | Out-Null
    }
  }

  # Deploy
  if ($DryRun) {
    Write-Host "[dry-run] netlify deploy --prod" -ForegroundColor DarkGray
  } else {
    Log "Deploying to production..."
    netlify deploy --prod --dir=.next 2>&1 | Select-Object -Last 10
    Ok "Deployed: https://$subdomain"
  }

  Pop-Location
}

Log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Ok "🎉 All 4 apps deployed"
Log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Log ""
Log "📋 Summary:"
foreach ($app in $Apps) {
  Log "   • $($app.Name) → https://$($app.Subdomain)"
}
Log ""
Log "Next: open Netlify dashboard to configure custom domains & deploy hooks"
