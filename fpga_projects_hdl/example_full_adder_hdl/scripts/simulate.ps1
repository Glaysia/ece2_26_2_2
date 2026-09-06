param([string]$VivadoBin = $env:VIVADO_BIN)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'tools.ps1')
$projectRoot = Split-Path -Parent $PSScriptRoot
$buildRoot = Join-Path $projectRoot 'build'
$waveOutput = Join-Path $buildRoot 'full_adder.vcd'
New-Item -ItemType Directory -Path $buildRoot -Force | Out-Null
# Do not leave an old waveform looking like a successful new result.
if (Test-Path -LiteralPath $waveOutput) { Remove-Item -LiteralPath $waveOutput }
$compiler = Find-VivadoTool -Name 'xvlog' -VivadoBin $VivadoBin
$elaborator = Find-VivadoTool -Name 'xelab' -VivadoBin $VivadoBin
$simulator = Find-VivadoTool -Name 'xsim' -VivadoBin $VivadoBin
$runRoot = Join-Path $buildRoot ('run-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $runRoot | Out-Null
$sources = @('src/half_adder.v', 'src/full_adder.v', 'sim/tb_full_adder.sv') | ForEach-Object { Join-Path $projectRoot $_ }
Push-Location -LiteralPath $runRoot
try {
    & $compiler --sv @sources *> compile.txt
    if ($LASTEXITCODE -ne 0) { Get-Content compile.txt; throw 'Compile failed.' }
    & $elaborator tb_full_adder --debug typical --snapshot full_adder_sim *> elaborate.txt
    if ($LASTEXITCODE -ne 0) { Get-Content elaborate.txt; throw 'Elaboration failed.' }
    & $simulator full_adder_sim --runall *> simulation.txt
    $simExit = $LASTEXITCODE
    Get-Content simulation.txt
    if ($simExit -ne 0) { throw 'Simulation failed.' }
    if (-not (Select-String -LiteralPath simulation.txt -SimpleMatch 'PASS: all 8 full-adder input combinations' -Quiet)) {
        throw 'Testbench did not report all eight cases passing.'
    }
    if (-not (Test-Path -LiteralPath full_adder.vcd)) { throw 'No VCD was generated.' }
    Copy-Item -LiteralPath full_adder.vcd -Destination $waveOutput
    Write-Host "Waveform: $waveOutput"
    Write-Host "Logs: $runRoot"
} finally { Pop-Location }
