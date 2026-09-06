function Find-VivadoTool {
    param([string]$Name, [string]$VivadoBin)
    if ($VivadoBin) {
        $candidate = Join-Path $VivadoBin ($Name + '.bat')
        if (Test-Path -LiteralPath $candidate -PathType Leaf) {
            return (Resolve-Path -LiteralPath $candidate).Path
        }
        throw "Missing $Name in VIVADO_BIN: $VivadoBin"
    }
    $found = Get-Command ($Name + '.bat') -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($found) { return $found.Source }
    throw "Cannot find $Name. Add Vivado/bin to PATH, or pass -VivadoBin. Restart VS Code after changing PATH."
}
