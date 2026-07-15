param(
    [ValidateRange(5, 300)]
    [int]$RestartDelaySeconds = 10,

    [ValidateRange(1, 60)]
    [int]$PollIntervalSeconds = 5
)

$ErrorActionPreference = "Stop"

$gatewayRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$python = Join-Path $gatewayRoot ".venv\Scripts\python.exe"
$pidFile = Join-Path $gatewayRoot "state\gateway.pid"
$supervisorPidFile = Join-Path $gatewayRoot "state\gateway-supervisor.pid"
$supervisorLog = Join-Path $gatewayRoot "logs\autostart.log"

if (-not (Test-Path -LiteralPath $python)) {
    throw "Gateway dependencies are not installed. Run scripts\install.ps1 first."
}

New-Item -ItemType Directory -Force -Path (Split-Path $supervisorLog), (Split-Path $pidFile) | Out-Null

$sha256 = [Security.Cryptography.SHA256]::Create()
try {
    $rootHash = [BitConverter]::ToString(
        $sha256.ComputeHash([Text.Encoding]::UTF8.GetBytes($gatewayRoot.ToLowerInvariant()))
    ).Replace("-", "").Substring(0, 16)
} finally {
    $sha256.Dispose()
}
$supervisorMutex = New-Object Threading.Mutex($false, "Local\CodexFeishuGatewaySupervisor-$rootHash")
$ownsSupervisorMutex = $false
try {
    $ownsSupervisorMutex = $supervisorMutex.WaitOne(0)
} catch [Threading.AbandonedMutexException] {
    $ownsSupervisorMutex = $true
}
if (-not $ownsSupervisorMutex) {
    $supervisorMutex.Dispose()
    Write-Output "Gateway supervisor is already running for this checkout."
    exit 0
}

function Write-SupervisorLog {
    param([string]$Message)

    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -LiteralPath $supervisorLog -Value "$timestamp $Message" -Encoding UTF8
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

if (Test-Path -LiteralPath $supervisorPidFile) {
    $existingSupervisorPid = 0
    $supervisorPidText = (Get-Content -Raw -LiteralPath $supervisorPidFile).Trim()
    if ([int]::TryParse($supervisorPidText, [ref]$existingSupervisorPid) -and $existingSupervisorPid -ne $PID) {
        $existingSupervisor = Get-CimInstance Win32_Process -Filter "ProcessId=$existingSupervisorPid" -ErrorAction SilentlyContinue
        if (
            $existingSupervisor -and
            $existingSupervisor.Name -ieq "powershell.exe" -and
            $existingSupervisor.CommandLine -match "(?i)run-supervised\.ps1"
        ) {
            Write-Output "Gateway supervisor is already running with PID $existingSupervisorPid."
            exit 0
        }
    }
    Remove-Item -LiteralPath $supervisorPidFile -Force -ErrorAction SilentlyContinue
}

$PID | Set-Content -LiteralPath $supervisorPidFile -Encoding ASCII
$env:PYTHONPATH = Join-Path $gatewayRoot "src"
Set-Location -LiteralPath $gatewayRoot
Write-SupervisorLog "Autostart supervisor started with PID $PID."

try {
    while ($true) {
        $gatewayProcess = Get-VerifiedGatewayProcess
        if ($gatewayProcess) {
            $observedPid = [int]$gatewayProcess.ProcessId
            Write-SupervisorLog "Adopting existing gateway PID $observedPid."
            do {
                Start-Sleep -Seconds $PollIntervalSeconds
                $gatewayProcess = Get-VerifiedGatewayProcess
            } while ($gatewayProcess -and [int]$gatewayProcess.ProcessId -eq $observedPid)
            Write-SupervisorLog "Gateway PID $observedPid stopped."
        } else {
            Remove-Item -LiteralPath $pidFile -Force -ErrorAction SilentlyContinue
            Write-SupervisorLog "Gateway is not running; starting it."
            try {
                # The Python entrypoint writes UTF-8 logs itself. Discard the
                # inherited native streams so Windows PowerShell 5 does not
                # wrap normal stderr logging as NativeCommandError records.
                $previousErrorActionPreference = $ErrorActionPreference
                $ErrorActionPreference = "Continue"
                try {
                    & $python -m feishu_gateway.app *> $null
                    $gatewayExitCode = $LASTEXITCODE
                } finally {
                    $ErrorActionPreference = $previousErrorActionPreference
                }
                Write-SupervisorLog "Gateway exited with code $gatewayExitCode."
            } catch {
                Write-SupervisorLog "Gateway launch failed: $($_.Exception.Message)"
            }
        }

        Start-Sleep -Seconds $RestartDelaySeconds
    }
} finally {
    try {
        if ((Get-Content -Raw -LiteralPath $supervisorPidFile).Trim() -eq [string]$PID) {
            Remove-Item -LiteralPath $supervisorPidFile -Force
        }
    } catch {
        # Shutdown cleanup is best effort.
    }
    if ($ownsSupervisorMutex) {
        try {
            $supervisorMutex.ReleaseMutex()
        } catch {
            # The operating system also releases the mutex on process exit.
        }
    }
    $supervisorMutex.Dispose()
}
