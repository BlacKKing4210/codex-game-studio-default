$ErrorActionPreference = "Stop"

$gatewayRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$envFile = Join-Path $gatewayRoot ".env"
if (-not (Test-Path -LiteralPath $envFile)) {
    throw "Run scripts\install.ps1 before configuring credentials."
}

$appId = (Read-Host "Feishu App ID").Trim()
if (-not $appId) {
    throw "App ID cannot be empty."
}

$secureSecret = Read-Host "Feishu App Secret (input is hidden)" -AsSecureString
$secretPointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureSecret)
try {
    $appSecret = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($secretPointer)
} finally {
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($secretPointer)
}
if (-not $appSecret) {
    throw "App Secret cannot be empty."
}
if ($appId -match "[\r\n]" -or $appSecret -match "[\r\n]") {
    throw "Credentials cannot contain line breaks."
}

$content = Get-Content -Raw -Encoding UTF8 -LiteralPath $envFile
$safeAppId = $appId.Replace('$', '$$')
$safeAppSecret = $appSecret.Replace('$', '$$')
$content = [regex]::Replace($content, '(?m)^FEISHU_APP_ID=.*$', "FEISHU_APP_ID=$safeAppId")
$content = [regex]::Replace($content, '(?m)^FEISHU_APP_SECRET=.*$', "FEISHU_APP_SECRET=$safeAppSecret")
[IO.File]::WriteAllText($envFile, $content, (New-Object Text.UTF8Encoding($false)))
$appSecret = $null

Write-Output "Credentials saved to the ignored local .env file."
Write-Output "Run scripts\start-background.ps1 after configuring the Feishu application."
