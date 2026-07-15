$ErrorActionPreference = "Stop"

$taskName = "Codex Feishu Gateway"
$task = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if (-not $task) {
    Write-Output "Autostart task is not installed."
} else {
    if (@("Running", "Queued") -contains [string]$task.State) {
        Stop-ScheduledTask -TaskName $taskName
        for ($attempt = 0; $attempt -lt 20; $attempt++) {
            Start-Sleep -Milliseconds 250
            $task = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
            if (-not $task -or $task.State -ne "Running") {
                break
            }
        }
    }
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Output "Removed '$taskName'."
}

$powershell = Join-Path $PSHOME "powershell.exe"
& $powershell `
    -NoLogo `
    -NoProfile `
    -NonInteractive `
    -ExecutionPolicy Bypass `
    -File (Join-Path $PSScriptRoot "stop.ps1") | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw "Autostart was removed, but stopping the current gateway failed with code $LASTEXITCODE."
}

Write-Output "The autostart supervisor and current gateway process were stopped."
