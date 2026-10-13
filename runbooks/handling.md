# Media handling runbook (training simulation)
1. Assign dummy asset ID, record date and fictional handler.
2. Generate disposable test file only; record its original nonzero state.
3. Execute simulated overwrite, record timestamp and SHA-256.
4. Verify every byte of disposable file is zero.
5. Document chain of custody and limitations.
6. For real equipment: follow your organization's approved NIST SP 800-88-aligned policy, device-specific methods, authorization and independent verification. This lab **does not** implement a real device sanitization procedure.
