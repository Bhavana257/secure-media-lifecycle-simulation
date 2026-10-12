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
