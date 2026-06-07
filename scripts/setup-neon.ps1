# setup-neon.ps1 - Configure Neon Postgres for all 4 backends (Windows)

param()

$ErrorActionPreference = "Stop"

$Apps = @("pharmaip-radar", "cloudfinops-copilot", "autohedge-pro", "quantalab")

function Log($m)  { Write-Host "`n$m" -ForegroundColor Cyan }
function Ok($m)   { Write-Host "✓ $m" -ForegroundColor Green }
function Err($m)  { Write-Host "✗ $m" -ForegroundColor Red }

Log "🐘 Neon Setup for Maxie Made"
Log ""
Log "Get a free database from: https://neon.tech"
Log ""

$dbUrl = Read-Host "Database URL (postgresql+asyncpg://...)"

if (-not $dbUrl) { Err "DATABASE_URL required"; exit 1 }
if ($dbUrl -notmatch "^postgresql(\+asyncpg)?://") {
  Err "URL must start with postgresql:// or postgresql+asyncpg://"
  exit 1
}

foreach ($app in $Apps) {
  $envFile = "$app\apps\api\.env"
  if (-not (Test-Path $envFile)) {
    $example = "$app\apps\api\.env.example"
    if (Test-Path $example) { Copy-Item $example $envFile } else { New-Item -ItemType File -Path $envFile | Out-Null }
  }
  $content = Get-Content $envFile | Where-Object { $_ -notmatch "^DATABASE_URL=" }
  $content += "DATABASE_URL=$dbUrl"
  Set-Content -Path $envFile -Value $content
  Ok "Updated: $envFile"
}

Log ""
Log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Ok "🎉 Neon configured for all 4 apps"
Log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Log ""
Log "Next: restart your backend, tables will auto-create"
