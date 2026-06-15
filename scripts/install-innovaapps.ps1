param(
    [string]$ExpectedTailscaleIp = "100.108.2.19"
)

$ErrorActionPreference = "Stop"
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $projectRoot

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw "Docker não está disponível nesta máquina."
}

$tailscaleOutput = tailscale ip -4 2>$null
if ($LASTEXITCODE -ne 0 -or $tailscaleOutput -notcontains $ExpectedTailscaleIp) {
    throw "O IP Tailscale $ExpectedTailscaleIp não está ativo nesta máquina."
}

if (-not (Test-Path -LiteralPath ".env")) {
    throw "Arquivo .env não encontrado."
}

docker compose config --quiet
docker compose build api web
docker compose up -d

Start-Sleep -Seconds 8
$health = Invoke-RestMethod -Uri "http://$ExpectedTailscaleIp`:8000/api/health"
if ($health.status -ne "ok") {
    throw "A API não respondeu com status ok."
}

$webResponse = Invoke-WebRequest -Uri "http://$ExpectedTailscaleIp`:3002/login" -UseBasicParsing
if ($webResponse.StatusCode -ne 200) {
    throw "O frontend não respondeu com HTTP 200."
}

docker compose ps
Write-Host "Innova Content Agent disponível em http://$ExpectedTailscaleIp`:3002"
