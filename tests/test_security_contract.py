"""Offline reference decisions, not execution of an actual agent or client."""
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
README = (ROOT / "README.md").read_text(encoding="utf-8")

def reject_insecure_config(value):
    if isinstance(value, dict):
        return any((k in ("insecure", "skip-cert-verify", "skip_cert_verify") and v is True)
                   or reject_insecure_config(v) for k, v in value.items())
    if isinstance(value, list): return any(reject_insecure_config(v) for v in value)
    return False

def decide(x):
    if not x.get("ssh", True) or not x.get("sudo", True): return "stop_access"
    if x.get("existing") and x.get("cancel"): return "preserve"
    if x.get("existing") and x.get("rerun"): return "preserve"
    if x.get("mode") == "beginner" and x.get("custom_param"): return "ask_switch"
    features = set(x.get("features", ()))
    if {"custom", "nearby"} <= features: return "conflict"
    if "custom" in features:
        if not x.get("valid", True): return "preserve" if x.get("existing") else "pause"
        return "check_confirm"
    if "nearby" in features:
        if not x.get("tls", True): return "reject_candidate"
        if not x.get("same_asn", True): return "ask_next_tier"
        return "discover_choose"
    if x.get("hy2"):
        if x.get("insecure"): return "reject"
        if x.get("acme"): return "verify_chain_hostname"
        if x.get("self_signed"): return "secure_trust" if x.get("supported") and x.get("matched") else "withhold"
        if x.get("domain") and x.get("dns_control"): return "try_acme"
    return "default"

CASES = [
    ("F01", {}, "default"),
    ("F02", {"mode":"beginner", "custom_param":True}, "ask_switch"),
    ("F03", {"mode":"expert", "features":["none"]}, "default"),
    ("F04", {"mode":"expert", "features":["custom"]}, "check_confirm"),
    ("F05", {"mode":"expert", "features":["nearby"]}, "discover_choose"),
    ("F06", {"mode":"expert", "features":["nearby", "custom"]}, "conflict"),
    ("F07", {"mode":"expert", "custom_param":True}, "default"),
    ("F08", {"mode":"expert", "features":["custom"], "valid":False, "existing":True}, "preserve"),
    ("F09", {"mode":"expert", "features":["nearby"], "same_asn":False}, "ask_next_tier"),
    ("F10", {"mode":"expert", "features":["nearby"], "tls":False}, "reject_candidate"),
    ("F11", {"mode":"expert", "endpoint":True}, "default"),
    ("F12", {"hy2":True, "domain":True, "dns_control":True}, "try_acme"),
    ("F13", {"hy2":True, "acme":True}, "verify_chain_hostname"),
    ("F14", {"hy2":True, "self_signed":True, "supported":True, "matched":True}, "secure_trust"),
    ("F15", {"hy2":True, "self_signed":True}, "withhold"),
    ("F16", {"hy2":True, "insecure":True}, "reject"),
    ("F17", {"existing":True, "cancel":True}, "preserve"),
    ("F18", {"existing":True, "rerun":True}, "preserve"),
    ("F19", {}, "default"),
    ("F20", {"ssh":False}, "stop_access"),
]

class OfflineReferenceTests(unittest.TestCase):
    def test_decision_scenarios(self):
        for name, inputs, expected in CASES:
            with self.subTest(case=name): self.assertEqual(decide(inputs), expected)
        self.assertEqual(decide({"sudo":False}), "stop_access")
        self.assertEqual(decide({"features":["custom"], "valid":False}), "pause")
        self.assertEqual(decide({"hy2":True,"self_signed":True,"supported":True,"matched":False}), "withhold")
    def test_rejected_configuration_examples(self):
        # Explicit negative fixtures, never client configurations for delivery.
        for config in ({"tls":{"insecure":True}}, {"proxies":[{"skip-cert-verify":True}]}):
            self.assertTrue(reject_insecure_config(config))
        self.assertFalse(reject_insecure_config({"tls":{"insecure":False}}))

    def test_document_binding(self):
        self.assertNotIn("use a user-supplied target when given", SKILL)
        for phrase in ("A target parameter alone never selects", "Both target feature IDs together", "explicitly permits leaving", "Cancellation or no confirmation causes no target changes", "client identity verification is mandatory", "certificate hostname normally", "separate trusted channel", "Never generate `insecure: true`", "enable `skip-cert-verify`", "A TLS connection alone does not prove server identity", "stop delivery of its HY2 profile", "`443/tcp` for REALITY", "`443/udp` for Hysteria2"):
            self.assertIn(phrase, SKILL)
        self.assertIn("不得默认关闭证书验证", README)
        self.assertIn("Never disable verification", README)
