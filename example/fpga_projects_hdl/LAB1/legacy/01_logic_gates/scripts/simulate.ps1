param([string]$VivadoBin = $env:VIVADO_BIN)
$ErrorActionPreference = 'Stop'
function Find-Tool([string]$Name) {
    if ($VivadoBin) {
        $candidate = Join-Path $VivadoBin ($Name + '.bat')
        if (Test-Path -LiteralPath $candidate -PathType Leaf) { return $candidate }
        throw "Missing $Name in VIVADO_BIN: $VivadoBin"
    }
    $found = Get-Command ($Name + '.bat') -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($found) { return $found.Source }
    throw "Cannot find $Name. Set VIVADO_BIN to your Vivado bin folder, then restart VS Code."
}
$projectRoot = Split-Path -Parent $PSScriptRoot
$labRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../..')).Path
$buildRoot = Join-Path $projectRoot 'build/vscode'
New-Item -ItemType Directory -Path $buildRoot -Force | Out-Null
$waveOutput = Join-Path $buildRoot 'logic_gate.vcd'
if (Test-Path -LiteralPath $waveOutput) { Remove-Item -LiteralPath $waveOutput }
$runRoot = Join-Path $buildRoot ('run-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $runRoot | Out-Null
$logOutput = Join-Path $buildRoot 'simulation.log'
'Simulation started. A final PASS line is required.' | Set-Content -LiteralPath $logOutput
$compiler = Find-Tool 'xvlog'
$elaborator = Find-Tool 'xelab'
$simulator = Find-Tool 'xsim'
$sources = @((Join-Path $labRoot 'common/rtl/logic_gate.v'), (Join-Path $labRoot 'common/tb/tb_logic_gate.sv'))
Push-Location -LiteralPath $runRoot
try {
    & $compiler --sv @sources *> compile.txt
    if ($LASTEXITCODE -ne 0) { Get-Content compile.txt; throw 'Compile failed. See compile.txt.' }
    & $elaborator tb_logic_gate --debug typical --snapshot logic_gate_sim *> elaborate.txt
    if ($LASTEXITCODE -ne 0) { Get-Content elaborate.txt; throw 'Elaboration failed. See elaborate.txt.' }
    & $simulator logic_gate_sim --runall *> simulation.txt
    $simExit = $LASTEXITCODE
    Get-Content simulation.txt | Tee-Object -FilePath $logOutput
    if ($simExit -ne 0) { throw 'Simulation failed.' }
    if (-not (Select-String -LiteralPath simulation.txt -SimpleMatch 'PASS: all 4 logic-gate input combinations' -Quiet)) {
        throw 'The testbench did not report all four cases passing.'
    }
    if (-not (Test-Path -LiteralPath logic_gate.vcd)) { throw 'No VCD was generated.' }
    Copy-Item -LiteralPath logic_gate.vcd -Destination $waveOutput
    Write-Host "Waveform: $waveOutput"
    Write-Host "Logs: $runRoot"
} finally { Pop-Location }
