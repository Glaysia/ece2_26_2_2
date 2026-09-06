param(
    [string]$VivadoBin = 'C:\AMDDesignTools\2026.1\Vivado\bin'
)
$ErrorActionPreference = 'Stop'
foreach ($tool in @('xvlog.bat', 'xelab.bat', 'xsim.bat')) {
    if (-not (Test-Path -LiteralPath (Join-Path $VivadoBin $tool))) {
        throw "Missing simulator: $tool in $VivadoBin"
    }
}
# A unique temporary directory preserves the evidence used in the PDF.
$runRoot = Join-Path ([IO.Path]::GetTempPath()) ('prelab-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $runRoot | Out-Null
foreach ($number in 16..21) {
    $sourceFolder = Join-Path $PSScriptRoot "simulation/exp$number"
    $runFolder = Join-Path $runRoot "exp$number"
    New-Item -ItemType Directory -Path $runFolder | Out-Null
    Get-ChildItem -LiteralPath $sourceFolder -File | Where-Object { $_.Extension -in '.v', '.sv' } |
        Copy-Item -Destination $runFolder
    Push-Location -LiteralPath $runFolder
    try {
        & (Join-Path $VivadoBin 'xvlog.bat') --sv clock_divider.v counter.v piano.v stepper.v tb_top_main.sv tone.v top_main.v watch.v *> compile.txt
        if ($LASTEXITCODE -ne 0) { throw "Compile failed: $runFolder" }
        & (Join-Path $VivadoBin 'xelab.bat') tb_top_main --debug typical --snapshot top_sim *> elaborate.txt
        if ($LASTEXITCODE -ne 0) { throw "Elaborate failed: $runFolder" }
        & (Join-Path $VivadoBin 'xsim.bat') top_sim --runall *> run.txt
        if ($LASTEXITCODE -ne 0) { throw "Simulation failed: $runFolder" }
        if (-not (Select-String -LiteralPath run.txt -SimpleMatch '101020 ns' -Quiet)) {
            throw "Unexpected finish time: $runFolder"
        }
        Write-Output "Finished exp$number : $runFolder"
    } finally { Pop-Location }
}
Write-Output "New VCDs and logs: $runRoot"
