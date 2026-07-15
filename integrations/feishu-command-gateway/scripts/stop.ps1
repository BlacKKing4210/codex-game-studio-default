$ErrorActionPreference = "Stop"

$gatewayRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$supervisorScript = (Resolve-Path (Join-Path $PSScriptRoot "run-supervised.ps1")).Path
$venvPython = Join-Path $gatewayRoot ".venv\Scripts\python.exe"
$pidFile = Join-Path $gatewayRoot "state\gateway.pid"
$supervisorPidFile = Join-Path $gatewayRoot "state\gateway-supervisor.pid"
$taskName = "Codex Feishu Gateway"

function Stop-OwnedProcessTree {
    param([int]$RootProcessId)

    $descendantIds = New-Object System.Collections.Generic.List[int]
    $pendingParentIds = New-Object System.Collections.Generic.Queue[int]
    $pendingParentIds.Enqueue($RootProcessId)
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
    Stop-Process -Id $RootProcessId -Force -ErrorAction SilentlyContinue
}

$autostartTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($autostartTask -and @("Running", "Queued") -contains [string]$autostartTask.State) {
    Stop-ScheduledTask -TaskName $taskName
    for ($attempt = 0; $attempt -lt 20; $attempt++) {
        Start-Sleep -Milliseconds 250
        $autostartTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
        if (-not $autostartTask -or $autostartTask.State -ne "Running") {
            break
        }
    }
}

$escapedSupervisorScript = [regex]::Escape($supervisorScript)
$supervisors = Get-CimInstance Win32_Process -Filter "Name='powershell.exe'" -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -match $escapedSupervisorScript }
foreach ($supervisor in $supervisors) {
    Stop-OwnedProcessTree -RootProcessId ([int]$supervisor.ProcessId)
}
Remove-Item -LiteralPath $supervisorPidFile -Force -ErrorAction SilentlyContinue

# Clean up any older launcher tree that predates the supervisor PID ledger.
$gatewayLaunchers = Get-CimInstance Win32_Process -Filter "Name='python.exe'" -ErrorAction SilentlyContinue |
    Where-Object {
        $_.ExecutablePath -eq $venvPython -and
        $_.CommandLine -match "(?i)(?:^|\s)-m\s+feishu_gateway\.app(?:\s|$)"
    }
foreach ($launcher in $gatewayLaunchers) {
    Stop-OwnedProcessTree -RootProcessId ([int]$launcher.ProcessId)
}

if (-not (Test-Path -LiteralPath $pidFile)) {
    Write-Output "Gateway is not running."
    exit 0
}

$gatewayPid = 0
$gatewayPidText = (Get-Content -Raw -LiteralPath $pidFile).Trim()
if (-not [int]::TryParse($gatewayPidText, [ref]$gatewayPid)) {
    Remove-Item -LiteralPath $pidFile -Force
    Write-Output "Removed an invalid gateway PID file."
    exit 0
}
$process = Get-CimInstance Win32_Process -Filter "ProcessId=$gatewayPid" -ErrorAction SilentlyContinue
if (-not $process) {
    Remove-Item -LiteralPath $pidFile -Force
    Write-Output "Removed a stale gateway PID file."
    exit 0
}
if ($process.Name -ne "python.exe" -or $process.CommandLine -notmatch "feishu_gateway\.app") {
    throw "PID $gatewayPid does not belong to the Feishu gateway; refusing to stop it."
}

# The gateway runtime and any active App Server turn form a verified
# descendant tree. Stop children first so no app-server is orphaned.
Stop-OwnedProcessTree -RootProcessId $gatewayPid
Remove-Item -LiteralPath $pidFile -Force
Write-Output "Gateway stopped."
