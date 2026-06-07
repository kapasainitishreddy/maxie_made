# setup-clerk.ps1 - Configure Clerk auth for all 4 apps (Windows)

param()

$ErrorActionPreference = "Stop"

$Apps = @("pharmaip-radar", "cloudfinops-copilot", "autohedge-pro", "quantalab")

function Log($m)  { Write-Host "`n$m" -ForegroundColor Cyan }
function Ok($m)   { Write-Host "✓ $m" -ForegroundColor Green }
function Warn($m) { Write-Host "⚠ $m" -ForegroundColor Yellow }
function Err($m)  { Write-Host "✗ $m" -ForegroundColor Red }

Log "🔐 Clerk Setup for Maxie Made"
Log ""
Log "Get your keys from: https://dashboard.clerk.com/apps → API Keys"
Log "  - Publishable key: pk_test_... or pk_live_..."
Log "  - Secret key: sk_test_... or sk_live_..."
Log "  - JWKS URL: https://<app>.clerk.accounts.dev/.well-known/jwks.json"
Log ""

$pubKey = Read-Host "Publishable key (pk_test_...)"
$secKey = Read-Host "Secret key (sk_test_...)"
$jwksUrl = Read-Host "JWKS URL"

if (-not $pubKey -or -not $secKey -or -not $jwksUrl) {
  Err "All three keys are required"
  exit 1
}

foreach ($app in $Apps) {
  $envFile = "$app\apps\web\.env"
  if (-not (Test-Path $envFile)) {
    $example = "$app\apps\web\.env.example"
    if (Test-Path $example) { Copy-Item $example $envFile } else { New-Item -ItemType File -Path $envFile | Out-Null }
  }
  $content = Get-Content $envFile | Where-Object { $_ -notmatch "^NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=" }
  $content += "NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=$pubKey"
  Set-Content -Path $envFile -Value $content
  Ok "Updated: $envFile"
}

foreach ($app in $Apps) {
  $envFile = "$app\apps\api\.env"
  if (-not (Test-Path $envFile)) {
    $example = "$app\apps\api\.env.example"
    if (Test-Path $example) { Copy-Item $example $envFile } else { New-Item -ItemType File -Path $envFile | Out-Null }
  }
  $content = Get-Content $envFile | Where-Object { $_ -notmatch "^(CLERK_SECRET_KEY|CLERK_JWKS_URL)=" }
  $content += "CLERK_SECRET_KEY=$secKey"
  $content += "CLERK_JWKS_URL=$jwksUrl"
  Set-Content -Path $envFile -Value $content
  Ok "Updated: $envFile"
}

Log ""
Log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Ok "🎉 Clerk configured for all 4 apps"
Log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Log ""
Log "Next: restart your dev servers, then visit http://localhost:3000"
