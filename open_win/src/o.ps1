# o — directory alias navigation (PowerShell wrapper).
#
# All logic lives in open.py. This wrapper exists only because a child
# process cannot change the shell's current directory: for `o -t <alias>`
# open.py prints the target path and this script runs Set-Location on it.
# Since .ps1 scripts run inside the calling PowerShell session, no
# dot-sourcing is needed (unlike the bash version of this tool).

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$openPy = Join-Path $scriptDir 'open.py'

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command py -ErrorAction SilentlyContinue
}
if (-not $python) {
    Write-Error 'Python not found on PATH. Install Python or add it to PATH.'
    return
}

if ($args.Count -ge 1 -and $args[0] -eq '-t') {
    $target = & $python.Source $openPy @args
    if ($LASTEXITCODE -eq 0 -and $target) {
        Set-Location -LiteralPath $target
    }
} else {
    & $python.Source $openPy @args
}
