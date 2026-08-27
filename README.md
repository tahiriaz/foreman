# Foreman Provisioning Project

## Structure

```text
provisioning_architecture/
├── create_host.py
├── functions/
│   ├── __init__.py
│   ├── vars.py
│   ├── shared.py
│   ├── inventory.py
│   ├── foreman.py
│   ├── dns.py
│   ├── process_host.py
│   ├── process_vm.py
│   ├── orchestrator.py
│   └── reporting.py
├── scripts/
│   └── add_dns_records.ps1
└── Templates/
    └── Resource List-v7.6.xlsx   # copy your workbook here
```

## Responsibilities

- `create_host.py`: application entry point and row-range selection.
- `inventory.py`: Excel loading, required columns, and row validation.
- `foreman.py`: Foreman REST helpers and shared resource-ID cache.
- `dns.py`: DNS record generation, temporary CSV handling, and PowerShell execution.
- `process_host.py`: physical-host Foreman payload and provisioning flow.
- `process_vm.py`: VM payload, Foreman creation, DNS, and Ansible scheduling.
- `orchestrator.py`: processor mapping, concurrent execution, and result collection.
- `reporting.py`: final provisioning table and summary.
- `shared.py`: shared value-validation helper.
- `vars.py`: environment/project configuration.
- `scripts/add_dns_records.ps1`: Windows DNS operations.

## Result model

Foreman-backed processors return these common fields:

- `status`: `Successful`, `Partial`, or `Failed`
- `foreman_status`
- `dns_status`
- `ansible_status`
- `details`

DNS-only resources return `status` and `details`; the orchestrator maps their
status into the DNS column automatically.

## Running

1. Copy `Resource List-v7.6.xlsx` into `Templates/`.
2. Review credentials and environment values in `functions/vars.py`.
3. Adjust `START_ROW` and `END_ROW` in `create_host.py`.
4. Run:

```powershell
python create_host.py
```

The program runs valid rows concurrently and prints a final report containing
overall, Foreman, DNS, and Ansible status.
