#!/usr/bin/env python3
"""Safe simulation of storage media lifecycle and chain of custody."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

TRANSITIONS = {
    "RECEIVED": {"QUARANTINED"},
    "QUARANTINED": {"AUTHORIZED"},
    "AUTHORIZED": {"SANITIZED"},
    "SANITIZED": {"VERIFIED"},
    "VERIFIED": {"RELEASED"},
    "RELEASED": set(),
}

ROLES = {
    "RECEIVED": {"technician"},
    "QUARANTINED": {"technician"},
    "AUTHORIZED": {"supervisor"},
    "SANITIZED": {"technician"},
    "VERIFIED": {"auditor"},
    "RELEASED": {"supervisor"},
}

class LifecycleError(Exception):
    pass

class MediaLifecycle:
    def __init__(self, asset_id, media_type, serial_number):
        if not all((asset_id, media_type, serial_number)):
            raise LifecycleError("Asset fields cannot be empty")
        self.asset_id = asset_id
        self.media_type = media_type
        self.serial_number = serial_number
        self.state = "RECEIVED"
        self.custodian = None
        self.events = []
        self._record("CREATE", "system", "system", "Asset registered")

    def _record(self, action, actor, role, details):
        previous_hash = self.events[-1]["hash"] if self.events else "GENESIS"
        event = {
            "sequence": len(self.events) + 1,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "asset_id": self.asset_id,
            "action": action,
            "actor": actor,
            "role": role,
            "state": self.state,
            "details": details,
            "previous_hash": previous_hash,
        }
        payload = json.dumps(event, sort_keys=True).encode()
        event["hash"] = hashlib.sha256(payload).hexdigest()
        self.events.append(event)

    def transition(self, new_state, actor, role):
        allowed = TRANSITIONS.get(self.state, set())
        if new_state not in allowed:
            raise LifecycleError(
                f"Invalid transition: {self.state} -> {new_state}"
            )
        if role not in ROLES[new_state]:
            raise LifecycleError(
                f"Role '{role}' cannot authorize {new_state}"
            )
        if not actor:
            raise LifecycleError("Actor is required")
        self.state = new_state
        self._record("TRANSITION", actor, role, f"Moved to {new_state}")

    def transfer(self, from_handler, to_handler, actor, role):
        if not to_handler or not actor:
            raise LifecycleError("Handler and actor required")
        if role not in {"technician", "supervisor"}:
            raise LifecycleError("Unauthorized custody transfer")
        if self.state == "RELEASED":
            raise LifecycleError("Released asset cannot be transferred")
        if self.custodian != from_handler:
            raise LifecycleError("Current custodian mismatch")
        self.custodian = to_handler
        self._record(
            "CUSTODY_TRANSFER", actor, role,
            f"{from_handler} -> {to_handler}"
        )

    def verify_audit_chain(self):
        previous_hash = "GENESIS"
        for index, event in enumerate(self.events, 1):
            record = dict(event)
            stored_hash = record.pop("hash", None)
            if record["sequence"] != index:
                return False
            if record["previous_hash"] != previous_hash:
                return False
            calculated = hashlib.sha256(
                json.dumps(record, sort_keys=True).encode()
            ).hexdigest()
            if calculated != stored_hash:
                return False
            previous_hash = stored_hash
        return True

    def export(self, output_path):
        output = Path(output_path)
        if output.exists():
            raise LifecycleError("Refusing to overwrite existing audit file")
        output.parent.mkdir(parents=True, exist_ok=True)
        lines = [json.dumps(event, sort_keys=True) for event in self.events]
        output.write_text(chr(10).join(lines) + chr(10), encoding="utf-8")
