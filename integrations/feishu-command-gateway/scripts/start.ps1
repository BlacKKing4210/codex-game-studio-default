$ErrorActionPreference = "Stop"

$gatewayRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$python = Join-Path $gatewayRoot ".venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $python)) {
    throw "Gateway dependencies are not installed. Run scripts\install.ps1 first."
}

$env:PYTHONPATH = Join-Path $gatewayRoot "src"
Set-Location -LiteralPath $gatewayRoot
& $python -m feishu_gateway.app
