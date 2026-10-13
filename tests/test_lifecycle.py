import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from lifecycle import MediaLifecycle, LifecycleError


class LifecycleTests(unittest.TestCase):

    def setUp(self):
        self.asset = MediaLifecycle(
            "DEMO-002", "SSD", "FAKE-SSD-002"
        )

    def test_complete_lifecycle(self):
        steps = [
            ("QUARANTINED", "technician"),
            ("AUTHORIZED", "supervisor"),
            ("SANITIZED", "technician"),
            ("VERIFIED", "auditor"),
            ("RELEASED", "supervisor"),
        ]

        for state, role in steps:
            self.asset.transition(state, "Test Operator", role)

        self.assertEqual(self.asset.state, "RELEASED")
        self.assertTrue(self.asset.verify_audit_chain())

    def test_unauthorized_action_rejected(self):
        with self.assertRaises(LifecycleError):
            self.asset.transition(
                "QUARANTINED", "Unauthorized User", "auditor"
            )

    def test_invalid_transition_rejected(self):
        with self.assertRaises(LifecycleError):
            self.asset.transition(
                "RELEASED", "Supervisor", "supervisor"
            )

    def test_custody_mismatch_rejected(self):
        self.asset.transfer(
            None, "Technician A", "Technician A", "technician"
        )

        with self.assertRaises(LifecycleError):
            self.asset.transfer(
                "Wrong Handler", "Technician B",
                "Technician B", "technician"
            )

    def test_audit_tampering_detected(self):
        self.asset.transition(
            "QUARANTINED", "Technician A", "technician"
        )

        self.asset.events[0]["actor"] = "Tampered User"

        self.assertFalse(self.asset.verify_audit_chain())


if __name__ == "__main__":
    unittest.main()
