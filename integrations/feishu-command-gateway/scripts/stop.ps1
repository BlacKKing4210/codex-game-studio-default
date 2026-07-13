$ErrorActionPreference = "Stop"

$gatewayRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$pidFile = Join-Path $gatewayRoot "state\gateway.pid"
if (-not (Test-Path -LiteralPath $pidFile)) {
    Write-Output "Gateway is not running."
    exit 0
}

$gatewayPid = [int](Get-Content -Raw -LiteralPath $pidFile)
$process = Get-CimInstance Win32_Process -Filter "ProcessId=$gatewayPid" -ErrorAction SilentlyContinue
if (-not $process) {
    Remove-Item -LiteralPath $pidFile -Force
    Write-Output "Removed a stale gateway PID file."
    exit 0
}
if ($process.Name -ne "python.exe" -or $process.CommandLine -notmatch "feishu_gateway\.app") {
    throw "PID $gatewayPid does not belong to the Feishu gateway; refusing to stop it."
}

Stop-Process -Id $gatewayPid
Remove-Item -LiteralPath $pidFile -Force
Write-Output "Gateway stopped."
