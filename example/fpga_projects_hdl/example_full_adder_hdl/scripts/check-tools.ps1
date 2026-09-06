param([string]$VivadoBin = $env:VIVADO_BIN)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'tools.ps1')
foreach ($name in @('xvlog', 'xelab', 'xsim')) {
    $tool = Find-VivadoTool -Name $name -VivadoBin $VivadoBin
    Write-Host "$name : $tool"
    & $tool -version
    if ($LASTEXITCODE -ne 0) { throw "$name version check failed." }
}
Write-Host 'PASS: Vivado simulation tools are available.'
