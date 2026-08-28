# Foreman / HPE Automation Project

## Main scripts

```text
foreman/
├── create_foreman_host.py
├── create_dns_records.py
├── configure_ilo_RM.py
├── configure_ilo_BL.py
├── configure_raid_RM.py
├── configure_raid_BL.py
├── get_mac_RM.py
├── get_mac_BL.py
├── gen_oaconfig.py
├── gen_clusterconfig.py
├── functions/
│   ├── vars.py
│   ├── output_log.py
│   ├── reporting.py
│   ├── inventory.py
│   ├── foreman.py
│   ├── dns.py
│   ├── process_host.py
│   ├── process_vm.py
│   ├── orchestrator.py
│   └── shared.py
├── logs/
├── scripts/
│   └── add_dns_records.ps1
└── Templates/
    └── Resource List-v7.6.xlsx
```

## Central configuration

Project configuration is maintained in `functions/vars.py`. This includes the
shared workbook and sheet, global row range for range-based jobs, credentials,
DNS, iLO/OA, RAID, MAC collection, OA generation, cluster generation, output
paths, concurrency settings, and script artifact prefixes.

`gen_oaconfig.py` and `gen_clusterconfig.py` intentionally read the complete
configured worksheet. Other range-based automation uses the global
`START_ROW` / `END_ROW` values where applicable.

## Console logs

Every Python script in the main project folder runs through the shared
`functions/output_log.py` wrapper. Console stdout/stderr is still displayed
normally and is simultaneously written to a timestamped `.log` file under
`logs/`.

Pre-existing Python `logging.StreamHandler` instances are also rebound while a
script runs, so logger-based output such as the blade iLO workflow is captured
in the same console log.

## Standard summary report

Every main-folder script produces a standardized final summary using these
columns:

```text
ROW | TYPE | NAME | TARGET | STATUS | TIME (s) | DETAILS
```

A matching timestamped CSV is saved under `logs/` with the same seven fields:

```text
Row,Type,Name,Target,Status,TimeSeconds,Details
```

Scripts that have useful task-specific detailed reports, such as iLO and RAID,
retain those detailed reports as well. The standardized summary is the common
cross-script view.

## Foreman provisioning

`create_host.py` was renamed to `create_foreman_host.py`.

Run it with:

```powershell
python create_foreman_host.py
```

The Foreman workflow continues to track Foreman, DNS, and Ansible sub-statuses;
they are included in the standardized summary `Details` field.
