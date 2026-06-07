# connect-frontend-to-backend.ps1 - Update Netlify env vars to point to live Fly.io backends (Windows)

param()

$ErrorActionPreference = "Stop"

$Apps = @(
  @{ Name = "pharmaip-radar";      Netlify = "pharmaip-radar";      ApiUrl = "https://pharmaip-radar-api.fly.dev" },
  @{ Name = "cloudfinops-copilot"; Netlify = "cloudfinops-copilot"; ApiUrl = "https://cloudfinops-copilot-api.fly.dev" },
  @{ Name = "autohedge-pro";       Netlify = "autohedge-pro";       ApiUrl = "https://autohedge-pro-api.fly.dev" },
  @{ Name = "quantalab";           Netlify = "quantalab";           ApiUrl = "https://quantalab-api.fly.dev" }
)

function Log($m) { Write-Host "`n$m" -ForegroundColor Cyan }
function Ok($m)  { Write-Host "✓ $m" -ForegroundColor Green }
function Err($m) { Write-Host "✗ $m" -ForegroundColor Red }

Log "🔗 Connect Frontends to Backends"
$confirm = Read-Host "Have you deployed backends to Fly.io? (y/n)"
if ($confirm -ne "y") { Err "Deploy first: .\scripts\deploy-fly.ps1"; exit 1 }

if (-not (Get-Command netlify -ErrorAction SilentlyContinue)) {
  Err "netlify CLI not installed"; exit 1
}

foreach ($app in $Apps) {
  Log "━━━ $($app.Name) ━━━"
  $webDir = "$($app.Name)\apps\web"
  if (-not (Test-Path $webDir)) { Err "Missing: $webDir"; continue }
  Push-Location $webDir

  if (-not (Test-Path ".netlify\state.json")) {
    Err "$webDir not linked. Run: cd $webDir && netlify link"
    Pop-Location; continue
  }

  netlify env:set NEXT_PUBLIC_API_URL $app.ApiUrl 2>&1 | Out-Null
  Ok "Set NEXT_PUBLIC_API_URL=$($app.ApiUrl)"

  Log "Redeploying..."
  netlify deploy --prod 2>&1 | Select-Object -Last 3
  Ok "Redeployed"

  Pop-Location
}

Log ""
Log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Ok "🎉 All 4 frontends connected to live backends"
Log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
