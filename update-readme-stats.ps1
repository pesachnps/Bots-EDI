#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Updates the Development Activity section in README.md with lines added per day.

.DESCRIPTION
    This script calculates the total lines of code added per day from git history
    and updates the Development Activity table in README.md. It can be run manually
    or automatically via git hooks.

.EXAMPLE
    .\update-readme-stats.ps1
#>

# Change to script directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

Write-Host "Updating README.md with development activity statistics..." -ForegroundColor Cyan

# Calculate lines added per day from git history
Write-Host "Analyzing git history..." -ForegroundColor Gray
$totals = @{}
$currentDate = ''

git --no-pager log --all --pretty=format:'%ad' --date=short --numstat | ForEach-Object {
    if ($_ -match '^\d{4}-\d{2}-\d{2}$') {
        $currentDate = $_
    } 
    elseif ($_ -match '^(\d+)\s+(\d+)\s+') {
        $added = [int]$matches[1]
        if (!$totals.ContainsKey($currentDate)) {
            $totals[$currentDate] = 0
        }
        $totals[$currentDate] += $added
    }
}

if ($totals.Count -eq 0) {
    Write-Host "No git history found. Exiting." -ForegroundColor Yellow
    exit 0
}

# Generate the table rows
$tableRows = $totals.GetEnumerator() | 
    Sort-Object Name | 
    ForEach-Object { 
        $formattedLines = "{0:N0}" -f $_.Value
        "| $($_.Name) | +$formattedLines |"
    }

# Build the new stats section
$newStatsSection = @"
## 📊 Development Activity

Tracking lines of code added with each push to the repository:

| Date | Lines Added |
|------|-------------|
$($tableRows -join "`n")

*This table is automatically updated by the ``update-readme-stats.ps1`` script.*
"@

# Read the current README
$readmePath = "README.md"
if (!(Test-Path $readmePath)) {
    Write-Host "ERROR: README.md not found!" -ForegroundColor Red
    exit 1
}

$readmeContent = Get-Content $readmePath -Raw

# Find and replace the stats section
$pattern = '(?s)## 📊 Development Activity.*?\*This table is automatically updated by the `update-readme-stats\.ps1` script\.\*'

if ($readmeContent -match $pattern) {
    # Update existing section
    $updatedContent = $readmeContent -replace $pattern, $newStatsSection
    Write-Host "Updating existing Development Activity section..." -ForegroundColor Green
} else {
    Write-Host "ERROR: Could not find Development Activity section in README.md" -ForegroundColor Red
    Write-Host "Please ensure the section exists with the marker comment." -ForegroundColor Yellow
    exit 1
}

# Write back to README
Set-Content -Path $readmePath -Value $updatedContent -NoNewline

Write-Host "✓ README.md updated successfully!" -ForegroundColor Green
Write-Host "  Total dates tracked: $($totals.Count)" -ForegroundColor Gray
