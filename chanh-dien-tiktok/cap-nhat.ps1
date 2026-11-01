# Cap nhat Chanh Dien LIVE tu GitHub.
# - File code (live/, nut bam, README): luon thay bang ban moi.
# - File noi dung (assets/, bai-giang/): chi tai neu may chua co, KHONG de len anh nen / bai giang chu da sua.
# - Khong dong toi cau-hinh.json, cong-duc/, nhac chu tu them.
$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$base = 'https://raw.githubusercontent.com/doanquocduyet/namban-panorama/claude/chua-online-tiktok-bzmruf/chanh-dien-tiktok/'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Host ''
Write-Host ' Dang lay danh sach file moi nhat...'
$list = (Invoke-WebRequest -UseBasicParsing ($base + 'cap-nhat.txt')).Content
if ($list -is [byte[]]) { $list = [Text.Encoding]::UTF8.GetString($list) }
$new = 0; $kept = 0; $updated = 0
foreach ($line in ($list -split "`n")) {
  $line = $line.Trim()
  if (-not $line -or $line.StartsWith('#')) { continue }
  $mode, $rel = $line -split '\s+', 2
  $dest = Join-Path $here ($rel -replace '/', '\')
  if ($mode -eq 'giu' -and (Test-Path $dest)) { $kept++; continue }
  $dir = Split-Path -Parent $dest
  if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
  $tmp = $dest + '.tai'
  Invoke-WebRequest -UseBasicParsing ($base + $rel) -OutFile $tmp
  if ($dest -like '*.bat') {
    $t = [IO.File]::ReadAllText($tmp) -replace "`r?`n", "`r`n"; [IO.File]::WriteAllText($tmp, $t)
  }
  $existed = Test-Path $dest
  Move-Item -Force $tmp $dest
  if ($existed) { $updated++ } else { $new++ }
  Write-Host ('   ' + $rel)
}
Write-Host ''
Write-Host (' Xong: cap nhat ' + $updated + ' file, them moi ' + $new + ' file, giu nguyen ' + $kept + ' file cua chu.')
