param(
    [Parameter(Mandatory=$true)]
    [string]$FileName,

    [Parameter(Mandatory=$true)]
    [string]$DnsServer,

    [Parameter(Mandatory=$true)]
    [string]$DomainName,

    [Parameter(Mandatory=$true)]
    [string]$Username,

    [Parameter(Mandatory=$true)]
    [string]$Password
)

Import-Module DnsServer

# 1. Create a Credential Object
$secPassword = ConvertTo-SecureString $Password -AsPlainText -Force
$creds = New-Object System.Management.Automation.PSCredential ($Username, $secPassword)

# 2. Establish a CIM Session to the DNS Server
# This allows the script to run commands as the specified user
$sessionOption = New-CimSessionOption -Protocol Dcom
try {
    $session = New-CimSession -ComputerName $DnsServer -Credential $creds -SessionOption $sessionOption -ErrorAction Stop
    Write-Host "Connected successfully to $DnsServer" -ForegroundColor Green
}
catch {
    Write-Error "Failed to connect to ${DnsServer}: $($_.Exception.Message)"
    exit
}

# 3. Read the CSV file
if (-not (Test-Path $FileName)) {
    Write-Error "File $FileName not found!"
    exit
}
$records = Import-Csv -Path $FileName

# 4. Process Records
foreach ($row in $records) {
    $fqdn   = $row.hostname
    $type   = $row.RecordType # Expected "A" or "CNAME"
    $target = $row.Target

    # --- LOGIC TO EXTRACT ZONE FROM FQDN ---
    if ($fqdn -like "*.*") {
        $parts = $fqdn.Split(".")
        $shortName = $parts[0]
        $currentZone = ($parts[1..($parts.Count - 1)] -join ".")
    }
    else {
        $shortName = $fqdn
        $currentZone = $DomainName
    }
    # ---------------------------------------

    Write-Host "`nProcessing: $name ($type) -> $target" -ForegroundColor Cyan

    try {
        # Check if the zone actually exists on this server first
        $zoneExists = Get-DnsServerZone -CimSession $session -Name $currentZone -ErrorAction SilentlyContinue
        if (-not $zoneExists) {
            Write-Warning "Zone '$currentZone' not found on $DnsServer. Skipping $shortName."
            continue
        }


        # Check for existing record via the Session
        $existing = Get-DnsServerResourceRecord -CimSession $session -ZoneName $currentZone -Name $shortName -ErrorAction SilentlyContinue

        if ($existing) {
            Write-Host "Old record found. Deleting..." -ForegroundColor Yellow
            # 3. Loop through each found record (in case there are multiple types)
             foreach ($record in $existing) {
                # Dynamically pass the exact RecordType found back into the Remove command
                Remove-DnsServerResourceRecord -CimSession $session -ZoneName $currentZone -Name $shortName -RRType $record.RecordType -Force
                Write-Output "Deleted $($record.RecordType) record for $shortName in zone $currentZone"
            }
        }

        # Create new record via the Session
        if ($type -eq "A") {
            Add-DnsServerResourceRecordA -CimSession $session -ZoneName $currentZone -Name $shortName -IPv4Address $target
            Write-Host "A record created for $shortName in zone $currentZone" -ForegroundColor Green
        }
        elseif ($type -eq "CNAME") {
            Add-DnsServerResourceRecordCName -CimSession $session -ZoneName $currentZone -Name $shortName -HostNameAlias $target
            Write-Host "CNAME record created for $shortName in zone $currentZone" -ForegroundColor Green
        }
    }
    catch {
        Write-Warning "Could not process ${shortName}: $($_.Exception.Message)"
    }
}

# Cleanup
Remove-CimSession $session