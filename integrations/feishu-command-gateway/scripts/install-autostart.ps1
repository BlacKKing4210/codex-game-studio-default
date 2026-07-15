param(
    [switch]$DoNotStart
)

$ErrorActionPreference = "Stop"

$taskName = "Codex Feishu Gateway"
$gatewayRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$supervisorScript = Join-Path $PSScriptRoot "run-supervised.ps1"
$pidFile = Join-Path $gatewayRoot "state\gateway.pid"
$stderrLog = Join-Path $gatewayRoot "logs\gateway.stderr.log"
$powershell = Join-Path $PSHOME "powershell.exe"
$currentUser = [Security.Principal.WindowsIdentity]::GetCurrent().Name

if (-not (Test-Path -LiteralPath $supervisorScript)) {
    throw "Autostart supervisor is missing: $supervisorScript"
}

& $powershell `
    -NoLogo `
    -NoProfile `
    -NonInteractive `
    -ExecutionPolicy Bypass `
    -File (Join-Path $PSScriptRoot "stop.ps1") *> $null
if ($LASTEXITCODE -ne 0) {
    throw "Could not stop the previous managed gateway before installing autostart."
}

$arguments = "-NoLogo -NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$supervisorScript`""
$action = New-ScheduledTaskAction `
    -Execute $powershell `
    -Argument $arguments `
    -WorkingDirectory $gatewayRoot
$trigger = New-ScheduledTaskTrigger -AtLogOn -User $currentUser
$principal = New-ScheduledTaskPrincipal `
    -UserId $currentUser `
    -LogonType Interactive `
    -RunLevel Limited
$settings = New-ScheduledTaskSettingsSet `
    -MultipleInstances IgnoreNew `
    -Priority 4 `
    -RestartCount 999 `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -StartWhenAvailable `
    -ExecutionTimeLimit ([TimeSpan]::Zero) `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries

Register-ScheduledTask `
    -TaskName $taskName `
    -Description "Starts and supervises the Codex Feishu gateway after user sign-in." `
    -Action $action `
    -Trigger $trigger `
    -Principal $principal `
    -Settings $settings `
    -Force | Out-Null

Write-Output "Registered '$taskName' for $currentUser."

if ($DoNotStart) {
    Write-Output "The gateway will start automatically at the next Windows sign-in."
    exit 0
}

Start-ScheduledTask -TaskName $taskName

$verifiedPid = $null
for ($attempt = 0; $attempt -lt 180; $attempt++) {
    Start-Sleep -Milliseconds 500
    if (-not (Test-Path -LiteralPath $pidFile)) {
        continue
    }
    $gatewayPid = 0
    $pidText = (Get-Content -Raw -LiteralPath $pidFile).Trim()
    if (-not [int]::TryParse($pidText, [ref]$gatewayPid)) {
        continue
    }
    $candidate = Get-CimInstance Win32_Process -Filter "ProcessId=$gatewayPid" -ErrorAction SilentlyContinue
    $logIsCurrent = $false
    if ($candidate -and (Test-Path -LiteralPath $stderrLog)) {
        $logIsCurrent = (Get-Item -LiteralPath $stderrLog).LastWriteTime -ge $candidate.CreationDate
    }
    $logText = Get-Content -Raw -LiteralPath $stderrLog -Encoding UTF8 -ErrorAction SilentlyContinue
    $readyPattern = "(?m)\s$gatewayPid\s+INFO\s+feishu_gateway:\s+Feishu long connection established"
    if (
        $candidate -and
        $candidate.Name -ieq "python.exe" -and
        $candidate.CommandLine -match "(?i)(?:^|\s)-m\s+feishu_gateway\.app(?:\s|$)" -and
        $logIsCurrent -and
        $logText -match $readyPattern
    ) {
        $verifiedPid = $gatewayPid
        break
    }
}

if (-not $verifiedPid) {
    $taskInfo = Get-ScheduledTaskInfo -TaskName $taskName -ErrorAction SilentlyContinue
    $lastResult = if ($taskInfo) { $taskInfo.LastTaskResult } else { "unknown" }
    throw "Autostart task was registered, but the gateway did not start within 90 seconds. LastTaskResult=$lastResult. Check $stderrLog."
}

Write-Output "Gateway is running with PID $verifiedPid."
Write-Output "It will reconnect automatically after future Windows sign-ins and restart after unexpected exits."
