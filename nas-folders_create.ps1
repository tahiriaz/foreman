# =====================================================================
# GENERATE ONEFS NVR HIERARCHY + QUOTAS (SEPARATE FILES)
# =====================================================================

# ============================================================
# CONFIGURATION
# ============================================================

$excelFile = "C:\Users\Lotfi\OneDrive\Thales\Dell Laptop\Makkah\MTR\MTR-RTR\nvr.xlsx"

$outputFolders = "C:\Users\Lotfi\OneDrive\Thales\Dell Laptop\Makkah\MTR\MTR-RTR\nas_folders3.sh"

$outputQuota = "C:\Users\Lotfi\OneDrive\Thales\Dell Laptop\Makkah\MTR\MTR-RTR\nas_folders3_quotas.sh"

$owner = "recorder:recorder"

# ============================================================
# QUOTAS
# ============================================================

$enableQuota = $true

$serviceQuota = "8TB"

# hard | advisory
$quotaMode = "hard"

# ============================================================
# IMPORT
# ============================================================

Import-Module ImportExcel -ErrorAction Stop

$data = Import-Excel -Path $excelFile

# ============================================================
# ARRAYS
# ============================================================

$folders=@()

$quotas=@()

# ============================================================
# HEADERS
# ============================================================

$folders += "#!/bin/bash"
$folders += ""
$folders += "set -e"
$folders += ""

$quotas += "#!/bin/bash"
$quotas += ""
$quotas += "set -e"
$quotas += ""

# ============================================================
# TRACKING
# ============================================================

$processedRG=@{}

$processedCluster=@{}

# ============================================================
# LOOP
# ============================================================

foreach ($row in $data) {

$clusterType="$($row.cluster_type)".Trim()

$clusterName="$($row.cluster_name)".Trim()

$rgName="$($row.picata_rg_instances)".Trim()

$nasRoot="$($row.nas_root)".Trim()

if (!$clusterType -or !$clusterName -or !$rgName -or !$nasRoot) {

continue

}

# ------------------------------------------------------------
# 1+1
# ------------------------------------------------------------

if ($clusterType -eq "1+1") {

if ($processedCluster.ContainsKey($clusterName)) {

continue

}

$processedCluster[$clusterName]=$true

}

$key="$nasRoot|$rgName"

if ($processedRG.ContainsKey($key)) {

continue

}

$processedRG[$key]=$true

$rgRoot="$nasRoot/$rgName"

# ------------------------------------------------------------
# ROOT
# ------------------------------------------------------------

$folders += ""
$folders += "################################################"

$folders += "# $rgName"

$folders += "################################################"

$folders += ""

$folders += "mkdir -p '$rgRoot'"

$folders += "chown $owner '$rgRoot'"

$folders += ""

# ------------------------------------------------------------
# STANDARD
# ------------------------------------------------------------

$folders += "mkdir -p '$rgRoot/app'"

$folders += "mkdir -p '$rgRoot/data'"

$folders += "mkdir -p '$rgRoot/etc/picata'"

$folders += "mkdir -p '$rgRoot/log'"

$folders += ""

$folders += "chown -R $owner '$rgRoot/app'"

$folders += "chown -R $owner '$rgRoot/data'"

$folders += "chown -R $owner '$rgRoot/etc'"

$folders += ""

switch ($clusterType) {

"7+1" {

$count=4

}

"1+1" {

$count=28

}

default {

continue

}

}

# ------------------------------------------------------------
# SERVICES
# ------------------------------------------------------------

for ($i=1;$i -le $count;$i++) {

$svc="{0}_p{1:D2}" -f $rgName,$i

$svcRoot="$rgRoot/$svc"

# --------------------------------------------------------
# FOLDERS
# --------------------------------------------------------

$folders += "mkdir -p '$svcRoot'"

$folders += "mkdir -p '$svcRoot/area-LQ'"

$folders += "mkdir -p '$svcRoot/area-LQ/alarms'"

$folders += "mkdir -p '$svcRoot/area-LQ/records'"

$folders += ""

$folders += "chown -R $owner '$svcRoot'"

$folders += ""

# --------------------------------------------------------
# QUOTAS
# --------------------------------------------------------

if ($enableQuota) {

$quotas += ""
$quotas += "################################################"

$quotas += "# $svc"

$quotas += "################################################"

$quotas += ""

$quotas += "isi quota quotas create '$svcRoot' --type=directory"

if ($quotaMode -eq "hard") {

$quotas += "isi quota quotas modify '$svcRoot' directory --hard-threshold $serviceQuota"

}
else {

$quotas += "isi quota quotas modify '$svcRoot' directory --advisory-threshold $serviceQuota"

}

$quotas += ""

}

}

}

# ============================================================
# SAVE
# ============================================================

$folders | Out-File `
-FilePath $outputFolders `
-Encoding utf8 `
-Force

$quotas | Out-File `
-FilePath $outputQuota `
-Encoding utf8 `
-Force

Write-Host ""

Write-Host "Folders : $outputFolders"

Write-Host "Quotas  : $outputQuota"

Write-Host ""

Write-Host "Quota Enabled : $enableQuota"

Write-Host "Quota Size    : $serviceQuota"

Write-Host ""