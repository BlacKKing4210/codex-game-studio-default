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

# The venv launcher, Python runtime, and any active App Server turn form a
# verified descendant tree. Stop children first so no app-server is orphaned.
$descendantIds = New-Object System.Collections.Generic.List[int]
$pendingParentIds = New-Object System.Collections.Generic.Queue[int]
$pendingParentIds.Enqueue($gatewayPid)
while ($pendingParentIds.Count -gt 0) {
    $parentId = $pendingParentIds.Dequeue()
    $children = Get-CimInstance Win32_Process -Filter "ParentProcessId=$parentId" -ErrorAction SilentlyContinue
    foreach ($child in $children) {
        $childId = [int]$child.ProcessId
        $descendantIds.Add($childId)
        $pendingParentIds.Enqueue($childId)
    }
}
for ($index = $descendantIds.Count - 1; $index -ge 0; $index--) {
    Stop-Process -Id $descendantIds[$index] -Force -ErrorAction SilentlyContinue
}
Stop-Process -Id $gatewayPid
Remove-Item -LiteralPath $pidFile -Force
Write-Output "Gateway stopped."
