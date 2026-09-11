param(
    [Parameter(Mandatory=$true)][string]$ManifestPath
)
$ErrorActionPreference = 'Stop'
$courseRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../..')).Path
$labRoot = (Resolve-Path -LiteralPath (Join-Path $courseRoot 'example/fpga_projects_hdl/LAB1')).Path
$backupRoot = [IO.Path]::GetFullPath((Join-Path $courseRoot 'tmp/pre-submodule-v2'))
$entries = Get-Content -LiteralPath $ManifestPath -Raw | ConvertFrom-Json
if ($entries.Count -ne 22) { throw 'Require exactly 22 published examples.' }

function Invoke-Git([string[]]$GitArgs) {
    $result = & git -C $courseRoot @GitArgs
    if ($LASTEXITCODE -ne 0) { throw "git failed: $GitArgs" }
    return $result
}

# Validate every recursive move target before touching the index or directories.
$moves = foreach ($entry in $entries) {
    if ($entry.status -ne 'PUBLISHED' -or $entry.commit -notmatch '^[0-9a-f]{40}$') {
        throw 'Every example must have a verified published commit.'
    }
    if ($entry.repository -notmatch '^https://github.com/Glaysia/fpga-lab-example-[a-z0-9-]+\.git$') {
        throw "Unexpected repository: $($entry.repository)"
    }
    $relative = 'example/fpga_projects_hdl/LAB1/' + $entry.project
    $source = (Resolve-Path -LiteralPath (Join-Path $courseRoot $relative)).Path
    $backup = [IO.Path]::GetFullPath((Join-Path $backupRoot $entry.project))
    if (-not $source.StartsWith($labRoot + [IO.Path]::DirectorySeparatorChar)) { throw 'Source escapes LAB1.' }
    if (-not $backup.StartsWith($backupRoot + [IO.Path]::DirectorySeparatorChar)) { throw 'Backup escapes backup directory.' }
    if (Test-Path -LiteralPath $backup) { throw "Backup already exists: $backup" }
    $changes = Invoke-Git @('status','--porcelain','--untracked-files=no','--',$relative)
    if ($changes) { throw "Uncommitted tracked changes in $relative" }
    $remote = Invoke-Git @('ls-remote',$entry.repository,'refs/heads/main')
    if (($remote -split '\s+')[0] -ne $entry.commit) { throw "Remote changed: $relative" }
    [PSCustomObject]@{ Entry=$entry; Relative=$relative; Source=$source; Backup=$backup }
}

foreach ($move in $moves) {
    New-Item -ItemType Directory -Path (Split-Path -Parent $move.Backup) -Force | Out-Null
    # Paths were resolved and checked against the explicit workspace roots above.
    Move-Item -LiteralPath $move.Source -Destination $move.Backup
    Invoke-Git @('rm','-r','--cached','--quiet','--',$move.Relative) | Out-Null
    Invoke-Git @('submodule','add','-b','main',$move.Entry.repository,$move.Relative) | Out-Null
    $actual = Invoke-Git @('-C',$move.Source,'rev-parse','HEAD')
    if ($actual -ne $move.Entry.commit) { throw "Wrong submodule commit: $($move.Relative)" }
    Write-Output "$($move.Relative) $actual"
}
Invoke-Git @('submodule','status')
