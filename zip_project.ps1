# Define paths
$ProjectRoot = Get-Item $PSScriptRoot
$ZipName = "fairshare_project.zip"
$ZipPath = Join-Path $ProjectRoot.Parent.FullName $ZipName
$TempDir = Join-Path $env:TEMP "fairshare_temp_$(Get-Date -Format 'yyyyMMddHHmmss')"

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "        Creating Clean Shareable ZIP         " -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

# Remove old zip if it exists
if (Test-Path $ZipPath) {
    Remove-Item $ZipPath -Force
}

# Create temp dir
New-Item -ItemType Directory -Path $TempDir -Force | Out-Null

# Copy directories and files (excluding caches, virtual envs, local db, local uploads)
Write-Host "[1/3] Copying files to temporary directory..." -ForegroundColor Yellow

# Copy backup_backendddd
$DestBackend = Join-Path $TempDir "backup_backendddd"
New-Item -ItemType Directory -Path $DestBackend -Force | Out-Null
Get-ChildItem -Path (Join-Path $ProjectRoot "backup_backendddd") | ForEach-Object {
    $Name = $_.Name
    if ($Name -eq "__pycache__" -or $Name -eq "rental_blossoms.db") {
        # Skip pycache and DB
        return
    }
    if ($Name -eq "uploads") {
        # Copy uploads but skip files inside it
        $DestUploads = Join-Path $DestBackend "uploads"
        New-Item -ItemType Directory -Path $DestUploads -Force | Out-Null
        return
    }
    Copy-Item -Path $_.FullName -Destination $DestBackend -Recurse -Force
}

# Copy frontend
$DestFrontend = Join-Path $TempDir "frontend"
Copy-Item -Path (Join-Path $ProjectRoot "frontend") -Destination $DestFrontend -Recurse -Force

# Copy root files
Copy-Item -Path (Join-Path $ProjectRoot "start.bat") -Destination $TempDir -Force
Copy-Item -Path (Join-Path $ProjectRoot "README.md") -Destination $TempDir -Force
Copy-Item -Path (Join-Path $ProjectRoot ".gitignore") -Destination $TempDir -Force

# Compress to ZIP
Write-Host "[2/3] Compressing files into $ZipName..." -ForegroundColor Yellow
Compress-Archive -Path "$TempDir\*" -DestinationPath $ZipPath -Force

# Clean up
Write-Host "[3/3] Cleaning up temporary files..." -ForegroundColor Yellow
Remove-Item -Path $TempDir -Recurse -Force

Write-Host ""
Write-Host "Success! Your clean, shareable project zip has been created at:" -ForegroundColor Green
Write-Host "$ZipPath" -ForegroundColor Green
Write-Host "You can now send this ZIP to anyone without sharing personal db records or virtual environments." -ForegroundColor White
Write-Host "=============================================" -ForegroundColor Cyan
Read-Host -Prompt "Press Enter to exit"
