$ErrorActionPreference = "Stop"

$gatewayRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$python = Join-Path $gatewayRoot ".venv\Scripts\python.exe"
$supervisorScript = Join-Path $PSScriptRoot "run-supervised.ps1"
$pidFile = Join-Path $gatewayRoot "state\gateway.pid"
$supervisorPidFile = Join-Path $gatewayRoot "state\gateway-supervisor.pid"
$stderrLog = Join-Path $gatewayRoot "logs\gateway.stderr.log"
$powershell = Join-Path $PSHOME "powershell.exe"

if (-not (Test-Path -LiteralPath $python)) {
    throw "Gateway dependencies are not installed. Run scripts\install.ps1 first."
}

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

function Get-VerifiedGatewayProcess {
    if (-not (Test-Path -LiteralPath $pidFile)) {
        return $null
    }
    $gatewayPid = 0
    $pidText = (Get-Content -Raw -LiteralPath $pidFile).Trim()
    if (-not [int]::TryParse($pidText, [ref]$gatewayPid)) {
        return $null
    }
    $candidate = Get-CimInstance Win32_Process -Filter "ProcessId=$gatewayPid" -ErrorAction SilentlyContinue
    if (
        $candidate -and
        $candidate.Name -ieq "python.exe" -and
        $candidate.CommandLine -match "(?i)(?:^|\s)-m\s+feishu_gateway\.app(?:\s|$)"
    ) {
        return $candidate
    }
    return $null
}

$existingGateway = Get-VerifiedGatewayProcess
if (-not $existingGateway) {
    Remove-Item -LiteralPath $pidFile -Force -ErrorAction SilentlyContinue
}

$existingSupervisor = $null
$escapedSupervisorScript = [regex]::Escape($supervisorScript)
if (Test-Path -LiteralPath $supervisorPidFile) {
    $existingSupervisorPid = 0
    $supervisorPidText = (Get-Content -Raw -LiteralPath $supervisorPidFile).Trim()
    if ([int]::TryParse($supervisorPidText, [ref]$existingSupervisorPid)) {
        $candidate = Get-CimInstance Win32_Process -Filter "ProcessId=$existingSupervisorPid" -ErrorAction SilentlyContinue
        if (
            $candidate -and
            $candidate.Name -ieq "powershell.exe" -and
            $candidate.CommandLine -match $escapedSupervisorScript
        ) {
            $existingSupervisor = $candidate
        }
    }
}

$startedSupervisor = $false
if (-not $existingSupervisor) {
    Remove-Item -LiteralPath $supervisorPidFile -Force -ErrorAction SilentlyContinue
    New-Item -ItemType Directory -Force -Path (Split-Path $pidFile), (Split-Path $stderrLog) | Out-Null
    $arguments = "-NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass -File `"$supervisorScript`""
    $existingSupervisor = Start-Process `
        -FilePath $powershell `
        -ArgumentList $arguments `
        -WorkingDirectory $gatewayRoot `
        -WindowStyle Hidden `
        -PassThru
    $startedSupervisor = $true
}

if ($existingGateway) {
    Write-Output "Gateway is already running with PID $($existingGateway.ProcessId); supervisor is active."
    exit 0
}

$readyProcess = $null
$startupError = ""
for ($attempt = 0; $attempt -lt 180; $attempt++) {
    Start-Sleep -Milliseconds 500
    $readyProcess = Get-VerifiedGatewayProcess
    $errorText = Get-Content -Raw -LiteralPath $stderrLog -Encoding UTF8 -ErrorAction SilentlyContinue
    if ($readyProcess) {
        $readyPid = [int]$readyProcess.ProcessId
        $readyPattern = "(?m)\s$readyPid\s+INFO\s+feishu_gateway:\s+Feishu long connection established"
        $logIsCurrent = (Test-Path -LiteralPath $stderrLog) -and ((Get-Item -LiteralPath $stderrLog).LastWriteTime -ge $readyProcess.CreationDate)
        if ($logIsCurrent -and $errorText -match $readyPattern) {
            break
        }
    }
    $supervisorStillRunning = Get-Process -Id ([int]$existingSupervisor.ProcessId) -ErrorAction SilentlyContinue
    if (-not $supervisorStillRunning) {
        $startupError = $errorText
        $readyProcess = $null
        break
    }
    $readyProcess = $null
}

if (-not $readyProcess) {
    if ($startedSupervisor) {
        Stop-OwnedProcessTree -RootProcessId ([int]$existingSupervisor.ProcessId)
        Remove-Item -LiteralPath $pidFile -Force -ErrorAction SilentlyContinue
        Remove-Item -LiteralPath $supervisorPidFile -Force -ErrorAction SilentlyContinue
    }
    if (-not $startupError) {
        $startupError = "No readiness signal was received within 90 seconds."
    }
    throw "Gateway failed to start. $startupError"
}

Write-Output "Gateway started in the background with PID $($readyProcess.ProcessId)."
Write-Output "Logs: $stderrLog"
