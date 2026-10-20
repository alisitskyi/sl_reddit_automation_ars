param()
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$manifestPath = Join-Path $projectRoot 'archive-manifest.json'
$manifest = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
$failures = @()
foreach ($entry in $manifest.files) {
  $targetPath = Join-Path $projectRoot $entry.path
  if (-not (Test-Path -LiteralPath $targetPath -PathType Leaf)) {
    $failures += "Missing: $($entry.path)"
    continue
  }
  $actualHash = (Get-FileHash -LiteralPath $targetPath -Algorithm SHA256).Hash
  if ($actualHash -ne $entry.sha256) { $failures += "Changed: $($entry.path)" }
}
if ($failures.Count -gt 0) {
  $failures | ForEach-Object { Write-Output $_ }
  exit 1
}
Write-Output "OK: $($manifest.files.Count) archived files match SHA256 manifest."

