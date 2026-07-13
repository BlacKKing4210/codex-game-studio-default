$ErrorActionPreference = "Stop"

$gatewayRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$venvPython = Join-Path $gatewayRoot ".venv\Scripts\python.exe"

$pythonCommand = Get-Command python.exe -ErrorAction SilentlyContinue
if ($pythonCommand -and $pythonCommand.Source -notmatch "\\WindowsApps\\") {
    $pythonExe = $pythonCommand.Source
} else {
    $bundled = Join-Path $env:USERPROFILE ".cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
    if (Test-Path -LiteralPath $bundled) {
        $pythonExe = $bundled
    } else {
        throw "Python 3.11+ was not found."
    }
}

if (-not (Test-Path -LiteralPath $venvPython)) {
    $venvRoot = Join-Path $gatewayRoot ".venv"
    if (Test-Path -LiteralPath $venvRoot) {
        Remove-Item -LiteralPath $venvRoot -Recurse -Force
    }
    & $pythonExe -m venv $venvRoot
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $venvPython)) {
        throw "Failed to create the Python virtual environment."
    }
}
& $venvPython -m pip install --disable-pip-version-check -r (Join-Path $gatewayRoot "requirements.txt")
if ($LASTEXITCODE -ne 0) {
    throw "Failed to install Python dependencies."
}

$desktopBin = Join-Path $env:LOCALAPPDATA "OpenAI\Codex\bin"
$codexExe = Get-ChildItem -LiteralPath $desktopBin -Recurse -Filter codex.exe -ErrorAction SilentlyContinue |
    Where-Object { $_.Length -gt 0 } |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $codexExe) {
    $npmCommand = Get-Command npm.cmd -ErrorAction SilentlyContinue
    if ($npmCommand) {
        $npmExe = $npmCommand.Source
    } else {
        $bundledNode = Join-Path $env:USERPROFILE ".cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin"
        $env:PATH = "$bundledNode;$env:PATH"
        $npmExe = (Get-Command npm.cmd -ErrorAction Stop).Source
    }
    $runtime = Join-Path $gatewayRoot ".runtime\codex"
    & $npmExe install --prefix $runtime --no-audit --no-fund "@openai/codex@0.144.3"
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to install the Codex CLI runtime."
    }
    $codexExe = Get-ChildItem -LiteralPath $runtime -Recurse -Filter codex.exe |
        Where-Object { $_.Length -gt 0 -and $_.FullName -match "@openai" } |
        Select-Object -First 1
}
if (-not $codexExe) {
    throw "Native Codex executable was not installed."
}

$envFile = Join-Path $gatewayRoot ".env"
if (-not (Test-Path -LiteralPath $envFile)) {
    $bytes = New-Object byte[] 24
    $rng = [Security.Cryptography.RandomNumberGenerator]::Create()
    try { $rng.GetBytes($bytes) } finally { $rng.Dispose() }
    $token = -join ($bytes | ForEach-Object { $_.ToString("x2") })
    $content = Get-Content -Raw -LiteralPath (Join-Path $gatewayRoot ".env.example")
    $content = $content.Replace("FEISHU_BOOTSTRAP_TOKEN=change-me", "FEISHU_BOOTSTRAP_TOKEN=$token")
    $content = $content.Replace("CODEX_EXECUTABLE=", "CODEX_EXECUTABLE=$($codexExe.FullName)")
    [IO.File]::WriteAllText($envFile, $content, (New-Object Text.UTF8Encoding($false)))
}

$projects = Join-Path $gatewayRoot "config\projects.json"
if (-not (Test-Path -LiteralPath $projects)) {
    Copy-Item -LiteralPath (Join-Path $gatewayRoot "config\projects.example.json") -Destination $projects
}

Write-Output "Installation complete."
Write-Output "1. Edit $envFile and set FEISHU_APP_ID / FEISHU_APP_SECRET."
Write-Output "2. Review $projects and keep only allowed repositories."
Write-Output "3. Run scripts\start.ps1."
