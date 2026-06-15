param(
    [string]$OutputPath = ".\dist\innova-content-agent-deploy.zip"
)

$ErrorActionPreference = "Stop"
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$outputFullPath = [System.IO.Path]::GetFullPath((Join-Path $projectRoot $OutputPath))
$outputDirectory = Split-Path -Parent $outputFullPath

if (-not $outputFullPath.StartsWith($projectRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "O pacote deve ser criado dentro do workspace."
}

New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null
if (Test-Path -LiteralPath $outputFullPath) {
    Remove-Item -LiteralPath $outputFullPath -Force
}

Push-Location $projectRoot
try {
    & tar.exe -a -c -f $outputFullPath `
        --exclude=".git" `
        --exclude=".next" `
        --exclude=".venv" `
        --exclude="node_modules" `
        --exclude="dist" `
        --exclude="__pycache__" `
        --exclude=".pytest_cache" `
        --exclude=".ruff_cache" `
        --exclude="*.db" `
        .
    if ($LASTEXITCODE -ne 0) {
        throw "Falha ao criar o pacote de implantação."
    }
}
finally {
    Pop-Location
}

Write-Host "Pacote criado em: $outputFullPath"
Write-Warning "O pacote contém o arquivo .env e deve ser tratado como confidencial."
