# Simulated Media Security Incident Report

**Asset:** DEMO-INCIDENT-001

## Rejected operations

- Invalid state: PASS (rejected: Invalid transition: RECEIVED -> SANITIZED)
- Wrong role: PASS (rejected: Role 'auditor' cannot authorize QUARANTINED)
- Custody mismatch: PASS (rejected: Current custodian mismatch)

## Outcome

All three invalid operations were rejected.
Audit integrity: PASS.
No physical storage devices were accessed.
