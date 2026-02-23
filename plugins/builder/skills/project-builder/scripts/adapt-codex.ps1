<#
.SYNOPSIS
    Create symlinks from .project/ to Codex CLI locations.

.DESCRIPTION
    Maps the .project standard directory structure to where OpenAI Codex CLI
    expects its configuration files. Uses relative symlinks so the repo
    stays portable across machines.

    Requires Developer Mode enabled (Settings > Update & Security > For developers)
    or an elevated (Administrator) PowerShell session.

.PARAMETER ProjectRoot
    Path to the project root containing .project/. Defaults to the parent of
    the directory containing this script.

.PARAMETER Clean
    Remove previously created symlinks instead of creating them.

.EXAMPLE
    .\project-standard\scripts\adapt-codex.ps1
    .\project-standard\scripts\adapt-codex.ps1 -Clean
    .\project-standard\scripts\adapt-codex.ps1 -ProjectRoot C:\repos\my-app
#>

[CmdletBinding()]
param(
    [string]$ProjectRoot,
    [switch]$Clean
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# ---------------------------------------------------------------------------
# Resolve paths
# ---------------------------------------------------------------------------

if (-not $ProjectRoot) {
    $ProjectRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSCommandPath))
}
$ProjectRoot = (Resolve-Path $ProjectRoot).Path

# ---------------------------------------------------------------------------
# Discover .project or .aiproject (or scaffold)
# ---------------------------------------------------------------------------

$DotProjectDir = $null
if ((Test-Path (Join-Path $ProjectRoot '.project') -PathType Container) -and
    (Test-Path (Join-Path $ProjectRoot '.project\PROJECT.md'))) {
    $DotProjectDir = '.project'
}
elseif ((Test-Path (Join-Path $ProjectRoot '.aiproject') -PathType Container) -and
        (Test-Path (Join-Path $ProjectRoot '.aiproject\PROJECT.md'))) {
    $DotProjectDir = '.aiproject'
}
elseif (-not $Clean) {
    $DotProjectDir = '.project'
    Write-Host 'No .project/ or .aiproject/ found. Creating .project/ scaffold...'
    $scaffoldDir = Join-Path $ProjectRoot '.project'
    New-Item -ItemType Directory -Path (Join-Path $scaffoldDir 'instructions') -Force | Out-Null
    @"
---
spec: "1.0"
name: ""
description: ""
---

# Project

Add project overview and getting started instructions here.
"@ | Set-Content -Path (Join-Path $scaffoldDir 'PROJECT.md') -Encoding UTF8
    @"
---
name: base
description: Base project instructions, always loaded.
activation: always
---

# Instructions

Add project coding standards and conventions here.
"@ | Set-Content -Path (Join-Path $scaffoldDir 'instructions\index.md') -Encoding UTF8
    Write-Host '  CREATED: .project\PROJECT.md'
    Write-Host '  CREATED: .project\instructions\index.md'
}
else {
    Write-Error "No .project/ or .aiproject/ directory found at $ProjectRoot"
    exit 1
}

$DotProject = Join-Path $ProjectRoot $DotProjectDir

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

function New-Symlink {
    param(
        [string]$Target,
        [string]$Link
    )

    if ($Clean) {
        if (Test-Path $Link) {
            $item = Get-Item $Link -Force -ErrorAction SilentlyContinue
            if ($item.LinkType -eq 'SymbolicLink') {
                Remove-Item $Link -Force
                Write-Host "  REMOVED: $Link"
            }
        }
        return
    }

    if (Test-Path $Link) {
        $item = Get-Item $Link -Force -ErrorAction SilentlyContinue
        if ($item.LinkType -ne 'SymbolicLink') {
            Write-Warning "  SKIP: $Link exists and is not a symlink"
            return
        }
    }

    $parentDir = Split-Path -Parent $Link
    if (-not (Test-Path $parentDir)) {
        New-Item -ItemType Directory -Path $parentDir -Force | Out-Null
    }

    if (Test-Path $Link) {
        Remove-Item $Link -Force
    }

    try {
        New-Item -ItemType SymbolicLink -Path $Link -Target $Target -Force | Out-Null
        Write-Host "  LINK: $Link -> $Target"
    }
    catch {
        Write-Warning "  FAIL: $Link (enable Developer Mode or run as Administrator)"
    }
}

function Remove-EmptyDir {
    param([string]$Path)
    if ((Test-Path $Path -PathType Container) -and
        @(Get-ChildItem $Path -Force).Count -eq 0) {
        Remove-Item $Path -Force
    }
}

# ---------------------------------------------------------------------------
# 1. instructions/index.md -> AGENTS.md
# ---------------------------------------------------------------------------

$InstructionsDir = Join-Path $DotProject 'instructions'
if ((Test-Path (Join-Path $InstructionsDir 'index.md')) -or $Clean) {
    New-Symlink -Target "$DotProjectDir\instructions\index.md" `
                -Link (Join-Path $ProjectRoot 'AGENTS.md')
}

# ---------------------------------------------------------------------------
# 2. skills/<name>/index.md -> .agents/skills/<name>/SKILL.md
# ---------------------------------------------------------------------------

$SkillsSource = Join-Path $DotProject 'skills'
$SkillsDir = Join-Path $ProjectRoot '.agents\skills'

if ($Clean) {
    if (Test-Path $SkillsDir) {
        Get-ChildItem $SkillsDir -Directory -Force | ForEach-Object {
            $skillMd = Join-Path $_.FullName 'SKILL.md'
            if (Test-Path $skillMd) {
                $item = Get-Item $skillMd -Force -ErrorAction SilentlyContinue
                if ($item.LinkType -eq 'SymbolicLink') {
                    New-Symlink -Target '' -Link $skillMd
                }
            }
        }
    }
}
elseif (Test-Path $SkillsSource -PathType Container) {
    Get-ChildItem $SkillsSource -Directory | ForEach-Object {
        $indexMd = Join-Path $_.FullName 'index.md'
        if (Test-Path $indexMd) {
            $name = $_.Name
            New-Symlink -Target "..\..\..\$DotProjectDir\skills\$name\index.md" `
                        -Link (Join-Path $SkillsDir "$name\SKILL.md")
        }
    }
}

# ---------------------------------------------------------------------------
# Clean up empty directories on --clean
# ---------------------------------------------------------------------------

if ($Clean) {
    if (Test-Path $SkillsDir) {
        Get-ChildItem $SkillsDir -Directory -Force | ForEach-Object {
            Remove-EmptyDir $_.FullName
        }
    }
    Remove-EmptyDir $SkillsDir
    $agentsDir = Join-Path $ProjectRoot '.agents'
    Remove-EmptyDir $agentsDir

    Write-Host 'Done. Symlinks removed.'
}
else {
    Write-Host 'Done. Codex symlinks created.'
}
