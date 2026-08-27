param(
    [Parameter(Mandatory = $true)]
    [string]$FileName,

    [Parameter(Mandatory = $true)]
    [string]$DnsServer,

    [Parameter(Mandatory = $true)]
    [string]$DomainName,

    [Parameter(Mandatory = $true)]
    [string]$Username,

    [Parameter(Mandatory = $true)]
    [string]$Password
)


# =============================================================================
# INITIALIZATION
# =============================================================================

$ErrorActionPreference = "Stop"

$hadErrors = $false
$session = $null

$totalRecords = 0
$successfulRecords = 0
$failedRecords = 0
$skippedRecords = 0


# =============================================================================
# IMPORT DNS MODULE
# =============================================================================

try {
    Import-Module DnsServer -ErrorAction Stop
}
catch {
    Write-Host "ERROR: Failed to import DnsServer module: $($_.Exception.Message)" -ForegroundColor Red
    exit 10
}


# =============================================================================
# VALIDATE INPUT FILE
# =============================================================================

if (-not (Test-Path -LiteralPath $FileName)) {
    Write-Host "ERROR: DNS input file not found: $FileName" -ForegroundColor Red
    exit 11
}


# =============================================================================
# CREATE CREDENTIAL OBJECT
#
# Avoid ConvertTo-SecureString because your previous run showed
# Microsoft.PowerShell.Security module loading failures.
# =============================================================================

try {
    $securePassword = New-Object System.Security.SecureString

    foreach ($character in $Password.ToCharArray()) {
        $securePassword.AppendChar($character)
    }

    $securePassword.MakeReadOnly()

    $creds = New-Object System.Management.Automation.PSCredential ($Username, $securePassword)
}
catch {
    Write-Host "ERROR: Failed to create credential object: $($_.Exception.Message)" -ForegroundColor Red
    exit 12
}


# =============================================================================
# MAIN EXECUTION
# =============================================================================

try {

    # =========================================================================
    # CREATE CIM SESSION
    # =========================================================================

    Write-Host "Connecting to DNS server $DnsServer..." -ForegroundColor Cyan

    $sessionOption = New-CimSessionOption -Protocol Dcom

    $session = New-CimSession `
        -ComputerName $DnsServer `
        -Credential $creds `
        -SessionOption $sessionOption `
        -ErrorAction Stop

    Write-Host "Connected successfully to $DnsServer" -ForegroundColor Green


    # =========================================================================
    # READ CSV
    # =========================================================================

    try {
        $records = Import-Csv `
            -LiteralPath $FileName `
            -ErrorAction Stop
    }
    catch {
        Write-Host "ERROR: Failed to read DNS CSV file '${FileName}': $($_.Exception.Message)" -ForegroundColor Red
        exit 14
    }


    if (-not $records) {
        Write-Warning "DNS input file contains no records."
        exit 0
    }


    # =========================================================================
    # PROCESS DNS RECORDS
    # =========================================================================

    foreach ($row in $records) {

        $totalRecords++

        $fqdn = ([string]$row.hostname).Trim()
        $type = ([string]$row.RecordType).Trim().ToUpperInvariant()
        $target = ([string]$row.Target).Trim()


        # =====================================================================
        # BASIC VALIDATION
        # =====================================================================

        if ([string]::IsNullOrWhiteSpace($fqdn)) {
            Write-Warning "Record $totalRecords has an empty hostname. Skipping."
            $hadErrors = $true
            $failedRecords++
            continue
        }

        if ([string]::IsNullOrWhiteSpace($type)) {
            Write-Warning "DNS record '$fqdn' has no RecordType. Skipping."
            $hadErrors = $true
            $failedRecords++
            continue
        }

        if ([string]::IsNullOrWhiteSpace($target)) {
            Write-Warning "DNS record '$fqdn' has no target. Skipping."
            $hadErrors = $true
            $failedRecords++
            continue
        }


        # =====================================================================
        # SUPPORTED TYPES
        # =====================================================================

        if (($type -ne "A") -and ($type -ne "CNAME")) {
            Write-Warning "Unsupported record type '$type' for '$fqdn'."
            $hadErrors = $true
            $failedRecords++
            continue
        }


        # =====================================================================
        # DETERMINE RECORD NAME AND ZONE
        # =====================================================================

        $firstDot = $fqdn.IndexOf(".")

        if ($firstDot -gt 0) {

            if ($firstDot -ge ($fqdn.Length - 1)) {
                Write-Warning "Invalid FQDN '$fqdn'. Nothing exists after the dot."
                $hadErrors = $true
                $failedRecords++
                continue
            }

            $shortName = $fqdn.Substring(0, $firstDot)
            $currentZone = $fqdn.Substring($firstDot + 1)
        }
        else {
            $shortName = $fqdn
            $currentZone = $DomainName
        }

        $shortName = ([string]$shortName).Trim()
        $currentZone = ([string]$currentZone).Trim().TrimEnd(".")


        if ([string]::IsNullOrWhiteSpace($shortName)) {
            Write-Warning "Could not determine DNS record name from '$fqdn'."
            $hadErrors = $true
            $failedRecords++
            continue
        }

        if ([string]::IsNullOrWhiteSpace($currentZone)) {
            Write-Warning "Could not determine DNS zone for '$fqdn'."
            $hadErrors = $true
            $failedRecords++
            continue
        }


        Write-Host ""
        Write-Host "Processing: $shortName ($type) -> $target" -ForegroundColor Cyan
        Write-Host "Zone      : $currentZone"


        try {

            # =================================================================
            # VERIFY ZONE EXISTS
            # =================================================================

            $zoneExists = Get-DnsServerZone `
                -CimSession $session `
                -Name $currentZone `
                -ErrorAction SilentlyContinue

            if (-not $zoneExists) {
                Write-Warning "Zone '$currentZone' not found on DNS server '$DnsServer'."
                $hadErrors = $true
                $failedRecords++
                continue
            }


            # =================================================================
            # READ EXISTING A AND CNAME RECORDS
            # =================================================================

            $existingA = @(
                Get-DnsServerResourceRecord `
                    -CimSession $session `
                    -ZoneName $currentZone `
                    -Name $shortName `
                    -RRType "A" `
                    -ErrorAction SilentlyContinue
            )

            $existingCNAME = @(
                Get-DnsServerResourceRecord `
                    -CimSession $session `
                    -ZoneName $currentZone `
                    -Name $shortName `
                    -RRType "CNAME" `
                    -ErrorAction SilentlyContinue
            )


            # =================================================================
            # A RECORD
            # =================================================================

            if ($type -eq "A") {

                # -------------------------------------------------------------
                # Validate target before deleting anything
                # -------------------------------------------------------------

                $parsedAddress = $null

                $validAddress = [System.Net.IPAddress]::TryParse(
                    $target,
                    [ref]$parsedAddress
                )

                if (-not $validAddress) {
                    throw "Target '$target' is not a valid IP address."
                }

                if ($parsedAddress.AddressFamily -ne [System.Net.Sockets.AddressFamily]::InterNetwork) {
                    throw "Target '$target' is not a valid IPv4 address."
                }


                # -------------------------------------------------------------
                # Check whether correct A already exists
                # -------------------------------------------------------------

                $correctAExists = $false

                foreach ($record in $existingA) {
                    try {
                        $existingAddress = $record.RecordData.IPv4Address.IPAddressToString

                        if ($existingAddress -eq $target) {
                            $correctAExists = $true
                        }
                    }
                    catch {
                        # Ignore malformed record
                    }
                }


                # -------------------------------------------------------------
                # Remove conflicting CNAME
                # -------------------------------------------------------------

                if ($existingCNAME.Count -gt 0) {

                    Write-Host "Conflicting CNAME record found. Removing..." -ForegroundColor Yellow

                    foreach ($record in $existingCNAME) {

                        Remove-DnsServerResourceRecord `
                            -CimSession $session `
                            -ZoneName $currentZone `
                            -InputObject $record `
                            -Force `
                            -ErrorAction Stop

                        Write-Host "Deleted conflicting CNAME for $shortName" -ForegroundColor Yellow
                    }
                }


                # -------------------------------------------------------------
                # Correct A already exists
                # -------------------------------------------------------------

                if ($correctAExists) {

                    Write-Host "A record already correct: $shortName -> $target" -ForegroundColor Green

                    $successfulRecords++
                    continue
                }


                # -------------------------------------------------------------
                # Remove wrong A record(s)
                # -------------------------------------------------------------

                if ($existingA.Count -gt 0) {

                    Write-Host "Existing A record found with different target. Replacing..." -ForegroundColor Yellow

                    foreach ($record in $existingA) {

                        Remove-DnsServerResourceRecord `
                            -CimSession $session `
                            -ZoneName $currentZone `
                            -InputObject $record `
                            -Force `
                            -ErrorAction Stop

                        Write-Host "Deleted existing A record for $shortName" -ForegroundColor Yellow
                    }
                }


                # -------------------------------------------------------------
                # CREATE A
                # -------------------------------------------------------------

                Add-DnsServerResourceRecordA `
                    -CimSession $session `
                    -ZoneName $currentZone `
                    -Name $shortName `
                    -IPv4Address $target `
                    -ErrorAction Stop

                Write-Host "A record created: $shortName -> $target" -ForegroundColor Green


                # -------------------------------------------------------------
                # VERIFY A
                # -------------------------------------------------------------

                $verifiedA = @(
                    Get-DnsServerResourceRecord `
                        -CimSession $session `
                        -ZoneName $currentZone `
                        -Name $shortName `
                        -RRType "A" `
                        -ErrorAction SilentlyContinue
                )

                $verifiedCorrect = $false

                foreach ($record in $verifiedA) {
                    try {
                        $verifiedAddress = $record.RecordData.IPv4Address.IPAddressToString

                        if ($verifiedAddress -eq $target) {
                            $verifiedCorrect = $true
                        }
                    }
                    catch {
                        # Ignore malformed record
                    }
                }


                if (-not $verifiedCorrect) {
                    throw "A record creation completed but verification failed."
                }


                # -------------------------------------------------------------
                # Verify CNAME conflict is gone
                # -------------------------------------------------------------

                $remainingCNAME = @(
                    Get-DnsServerResourceRecord `
                        -CimSession $session `
                        -ZoneName $currentZone `
                        -Name $shortName `
                        -RRType "CNAME" `
                        -ErrorAction SilentlyContinue
                )

                if ($remainingCNAME.Count -gt 0) {
                    throw "A record exists but a conflicting CNAME still remains."
                }


                $successfulRecords++

                Write-Host "Verified A record successfully." -ForegroundColor Green
            }


            # =================================================================
            # CNAME RECORD
            # =================================================================

            elseif ($type -eq "CNAME") {

                $desiredAlias = ([string]$target).Trim().TrimEnd(".")

                if ([string]::IsNullOrWhiteSpace($desiredAlias)) {
                    throw "CNAME target is empty after normalization."
                }


                # -------------------------------------------------------------
                # Check whether correct CNAME already exists
                # -------------------------------------------------------------

                $correctCNAMEExists = $false

                foreach ($record in $existingCNAME) {
                    try {
                        $existingAlias = ([string]$record.RecordData.HostNameAlias).Trim().TrimEnd(".")

                        if (
                            $existingAlias.Equals(
                                $desiredAlias,
                                [System.StringComparison]::OrdinalIgnoreCase
                            )
                        ) {
                            $correctCNAMEExists = $true
                        }
                    }
                    catch {
                        # Ignore malformed record
                    }
                }


                # -------------------------------------------------------------
                # Remove conflicting A
                # -------------------------------------------------------------

                if ($existingA.Count -gt 0) {

                    Write-Host "Conflicting A record found. Removing..." -ForegroundColor Yellow

                    foreach ($record in $existingA) {

                        Remove-DnsServerResourceRecord `
                            -CimSession $session `
                            -ZoneName $currentZone `
                            -InputObject $record `
                            -Force `
                            -ErrorAction Stop

                        Write-Host "Deleted conflicting A record for $shortName" -ForegroundColor Yellow
                    }
                }


                # -------------------------------------------------------------
                # Correct CNAME already exists
                # -------------------------------------------------------------

                if ($correctCNAMEExists) {

                    Write-Host "CNAME already correct: $shortName -> $target" -ForegroundColor Green

                    $successfulRecords++
                    continue
                }


                # -------------------------------------------------------------
                # Remove wrong CNAME
                # -------------------------------------------------------------

                if ($existingCNAME.Count -gt 0) {

                    Write-Host "Existing CNAME found with different target. Replacing..." -ForegroundColor Yellow

                    foreach ($record in $existingCNAME) {

                        Remove-DnsServerResourceRecord `
                            -CimSession $session `
                            -ZoneName $currentZone `
                            -InputObject $record `
                            -Force `
                            -ErrorAction Stop

                        Write-Host "Deleted existing CNAME for $shortName" -ForegroundColor Yellow
                    }
                }


                # -------------------------------------------------------------
                # CREATE CNAME
                # -------------------------------------------------------------

                Add-DnsServerResourceRecordCName `
                    -CimSession $session `
                    -ZoneName $currentZone `
                    -Name $shortName `
                    -HostNameAlias $target `
                    -ErrorAction Stop

                Write-Host "CNAME created: $shortName -> $target" -ForegroundColor Green


                # -------------------------------------------------------------
                # VERIFY CNAME
                # -------------------------------------------------------------

                $verifiedCNAME = @(
                    Get-DnsServerResourceRecord `
                        -CimSession $session `
                        -ZoneName $currentZone `
                        -Name $shortName `
                        -RRType "CNAME" `
                        -ErrorAction SilentlyContinue
                )

                $verifiedCorrect = $false

                foreach ($record in $verifiedCNAME) {
                    try {
                        $verifiedAlias = ([string]$record.RecordData.HostNameAlias).Trim().TrimEnd(".")

                        if (
                            $verifiedAlias.Equals(
                                $desiredAlias,
                                [System.StringComparison]::OrdinalIgnoreCase
                            )
                        ) {
                            $verifiedCorrect = $true
                        }
                    }
                    catch {
                        # Ignore malformed record
                    }
                }


                if (-not $verifiedCorrect) {
                    throw "CNAME creation completed but verification failed."
                }


                # -------------------------------------------------------------
                # Verify A conflict is gone
                # -------------------------------------------------------------

                $remainingA = @(
                    Get-DnsServerResourceRecord `
                        -CimSession $session `
                        -ZoneName $currentZone `
                        -Name $shortName `
                        -RRType "A" `
                        -ErrorAction SilentlyContinue
                )

                if ($remainingA.Count -gt 0) {
                    throw "CNAME exists but a conflicting A record still remains."
                }


                $successfulRecords++

                Write-Host "Verified CNAME successfully." -ForegroundColor Green
            }
        }
        catch {
            Write-Warning "Could not process '${fqdn}': $($_.Exception.Message)"

            $hadErrors = $true
            $failedRecords++
        }
    }
}
catch {
    Write-Host "ERROR: DNS processing terminated unexpectedly: $($_.Exception.Message)" -ForegroundColor Red

    $hadErrors = $true
}
finally {

    # =========================================================================
    # CLEANUP
    # =========================================================================

    if ($session) {

        try {
            Remove-CimSession `
                -CimSession $session `
                -ErrorAction Stop

            Write-Host ""
            Write-Host "CIM session closed successfully." -ForegroundColor DarkGray
        }
        catch {
            Write-Warning "Unable to cleanly remove CIM session: $($_.Exception.Message)"
            $hadErrors = $true
        }
    }
}


# =============================================================================
# SUMMARY
# =============================================================================

Write-Host ""
Write-Host ("=" * 80)
Write-Host "DNS EXECUTION SUMMARY"
Write-Host ("=" * 80)

Write-Host "DNS Server         : $DnsServer"
Write-Host "Default Domain     : $DomainName"
Write-Host "Total Records      : $totalRecords"
Write-Host "Successful         : $successfulRecords"
Write-Host "Failed             : $failedRecords"
Write-Host "Skipped            : $skippedRecords"

Write-Host ("=" * 80)


# =============================================================================
# EXIT CODE
# =============================================================================
#
# 0  = all records processed successfully
# 1  = one or more DNS records failed
# 10 = DnsServer module import failed
# 11 = input CSV missing
# 12 = credential creation failed
# 14 = CSV import failed
# =============================================================================

if ($hadErrors) {

    Write-Host ""
    Write-Host "DNS processing completed WITH ERRORS." -ForegroundColor Red

    exit 1
}

Write-Host ""
Write-Host "DNS processing completed successfully." -ForegroundColor Green

exit 0