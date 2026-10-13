# Secure Media Sanitization & Chain-of-Custody **Simulation**

**Not a NIST-certified sanitization utility.** This project creates a disposable regular file, overwrites its bytes, verifies zeros, and writes a mock asset chain-of-custody log. It **never** erases disks, partitions, devices or real customer data. A regular file is not representative of SSD wear leveling, remapped blocks, caches or firmware behavior. Do not claim this demonstrates compliant physical media sanitization.

## Quick start
```bash
python3 scripts/media_lab.py init --workspace demo --size-kib 64
python3 scripts/media_lab.py sanitize --workspace demo --operator 'Lab Operator'
python3 scripts/media_lab.py verify --workspace demo
python3 -m unittest discover -s tests -v
```
The workspace must be a new or existing directory under the project. All operations target `demo/disposable_test_media.bin` only. To reset, manually remove the `demo/` directory after reviewing it.

## What to document
See `runbooks/handling.md` and `templates/custody_record.csv`. Use dummy asset IDs and redact any personal or business information. Never point this tool at a real drive.

## Advanced Media Lifecycle Simulation

The project includes `scripts/lifecycle.py`, a Python module that simulates asset tracking, role-based authorization, chain-of-custody transfers, and audit records.

### Lifecycle states

RECEIVED → QUARANTINED → AUTHORIZED → SANITIZED → VERIFIED → RELEASED

- Technician: quarantine and record simulated sanitization
- Supervisor: authorize processing and release
- Auditor: record simulated verification

The system rejects invalid state transitions, unauthorized roles, and custody transfers involving an incorrect current handler.

### Audit integrity

Each lifecycle event contains a sequence number, UTC timestamp, fictional asset ID, actor, role, state, and SHA-256 hash linked to the previous event.

The hash chain can detect changes within the recorded event sequence. It is not tamper-proof against complete replacement or deletion of the audit history.

### Test results and evidence

Run all tests:

    python3 -m unittest discover -s tests -v

Validated result: 8 automated tests passed.

Evidence files:
- `evidence/media_audit.jsonl`: Seven simulated lifecycle events
- `evidence/security_incident.md`: Three rejected operations

All assets, personnel, and serial numbers are fictional. Lifecycle states are simulated and do not prove physical media sanitization.
