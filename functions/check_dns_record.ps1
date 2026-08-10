param(
    [Parameter(Mandatory=$true)]
    [string]$DnsServer,

    [Parameter(Mandatory=$true)]
    [string]$DomainName,

    [Parameter(Mandatory=$true)]
    [string]$hostname,

    [Parameter(Mandatory=$true)]
    [string]$Username,

    [Parameter(Mandatory=$true)]
    [string]$Password
)

Import-Module DnsServer

$secPassword = ConvertTo-SecureString $Password -AsPlainText -Force
$creds = New-Object System.Management.Automation.PSCredential ($Username, $secPassword)
$sessionOption = New-CimSessionOption -Protocol Dcom
try {
    $session = New-CimSession -ComputerName $DnsServer -Credential $creds -SessionOption $sessionOption -ErrorAction Stop
    Write-Host "Connected successfully to $DnsServer" -ForegroundColor Green
    if ($hostname -like "*.*") {
        $parts = $hostname.Split(".")
        $shortName = $parts[0]
        $currentZone = ($parts[1..($parts.Count - 1)] -join ".")
    }
    else {
        $shortName = $hostname
        $currentZone = $DomainName
    }

    $zoneExists = Get-DnsServerZone -CimSession $session -Name $currentZone -ErrorAction SilentlyContinue
    if (-not $zoneExists) {
        Remove-CimSession $session
        exit 7
    }

    # $existing = Get-DnsServerResourceRecord -CimSession $session -ZoneName $currentZone -Name $shortName -RRType $type -ErrorAction SilentlyContinue
    $existing = Get-DnsServerResourceRecord -CimSession $session -ZoneName $currentZone -Name $shortName -ErrorAction SilentlyContinue
    if ($existing) {
        Remove-CimSession $session
        # Rerturn tru if host exists
        exit 0
    }
    else {
        Remove-CimSession $session
        # Rerturn false if host does not exists
        exit 1
    }
}
catch {
    Write-Error "Failed to connect to ${DnsServer}: $($_.Exception.Message)"
    exit 8
}
