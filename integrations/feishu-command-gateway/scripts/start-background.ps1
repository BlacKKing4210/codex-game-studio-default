$ErrorActionPreference = "Stop"

$gatewayRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$python = Join-Path $gatewayRoot ".venv\Scripts\python.exe"
$pidFile = Join-Path $gatewayRoot "state\gateway.pid"
$stdoutLog = Join-Path $gatewayRoot "logs\gateway.stdout.log"
$stderrLog = Join-Path $gatewayRoot "logs\gateway.stderr.log"
if (-not (Test-Path -LiteralPath $python)) {
    throw "Gateway dependencies are not installed. Run scripts\install.ps1 first."
}

if (Test-Path -LiteralPath $pidFile) {
    $existingPid = [int](Get-Content -Raw -LiteralPath $pidFile)
    if (Get-Process -Id $existingPid -ErrorAction SilentlyContinue) {
        Write-Output "Gateway is already running with PID $existingPid."
        exit 0
    }
    Remove-Item -LiteralPath $pidFile -Force
}

New-Item -ItemType Directory -Force -Path (Split-Path $pidFile), (Split-Path $stdoutLog) | Out-Null
$env:PYTHONPATH = Join-Path $gatewayRoot "src"
$process = Start-Process `
    -FilePath $python `
    -ArgumentList @("-m", "feishu_gateway.app") `
    -WorkingDirectory $gatewayRoot `
    -WindowStyle Hidden `
    -RedirectStandardOutput $stdoutLog `
    -RedirectStandardError $stderrLog `
    -PassThru
$process.Id | Set-Content -LiteralPath $pidFile -Encoding ASCII

$ready = $false
$startupError = ""
for ($attempt = 0; $attempt -lt 30; $attempt++) {
    Start-Sleep -Milliseconds 500
    $running = Get-Process -Id $process.Id -ErrorAction SilentlyContinue
    $errorText = Get-Content -Raw -LiteralPath $stderrLog -ErrorAction SilentlyContinue
    if ($errorText -match "Starting Feishu long connection") {
        $ready = $true
        break
    }
    if ($errorText -match "Configuration error:") {
        $startupError = $errorText
        break
    }
    if (-not $running) {
        $startupError = $errorText
        break
    }
}
if (-not $ready) {
    $running = Get-Process -Id $process.Id -ErrorAction SilentlyContinue
    if ($running) {
        Stop-Process -Id $process.Id -Force
    }
    Remove-Item -LiteralPath $pidFile -Force -ErrorAction SilentlyContinue
    if (-not $startupError) {
        $startupError = "No readiness signal was received within 15 seconds."
    }
    throw "Gateway failed to start. $startupError"
}

Write-Output "Gateway started in the background with PID $($process.Id)."
Write-Output "Logs: $stderrLog"
