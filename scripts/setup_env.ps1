<#
Usage:  powershell -ExecutionPolicy Bypass -File scripts/setup_env.ps1 [-Help]
Creates a .venv using Python 3.12 (preferred) or 3.11 if available. Installs requirements.
#>
[CmdletBinding()]
param(
  [switch]$Help
)
if($Help){
  Write-Host "Usage: setup_env.ps1 [-Help]" -ForegroundColor Yellow
  Write-Host "  Creates .venv using Python 3.12 (preferred) or 3.11, upgrades pip tooling, installs requirements.";
  Write-Host "  Re-run anytime; existing .venv will be reused.";
  exit 0
}

$ErrorActionPreference = 'Stop'

function Find-Python {
    param([string[]]$candidates)
    foreach ($c in $candidates) {
        try {
            $v = & $c --version 2>$null
            if ($LASTEXITCODE -eq 0 -and ($v -match 'Python (3\.11|3\.12)')) { return $c }
        } catch { }
    }
    return $null
}

$candidate = Find-Python @('python3.12','py -3.12','python3.11','py -3.11','python')
if (-not $candidate) {
    Write-Host 'ERROR: Python 3.12 or 3.11 not found. Install from https://www.python.org/downloads/ then re-run.' -ForegroundColor Red
    exit 1
}

$version = & $candidate --version
if ($version -notmatch 'Python (3\.11|3\.12)') {
    Write-Host "ERROR: Resolved interpreter $candidate is $version. Need 3.11 or 3.12." -ForegroundColor Red
    exit 1
}

Write-Host "Using $candidate ($version)"

if (Test-Path .venv) {
    Write-Host '.venv already exists. Skipping creation.' -ForegroundColor Yellow
} else {
    & $candidate -m venv .venv
    Write-Host 'Created virtual environment .venv'
}

# Activate for this session
$activate = Join-Path .venv Scripts Activate.ps1
. $activate

python -m pip install --upgrade pip setuptools wheel
if (Test-Path requirements.txt) { pip install -r requirements.txt }
if (Test-Path requirements-dev.txt) { pip install -r requirements-dev.txt }

Write-Host 'Environment ready.' -ForegroundColor Green
