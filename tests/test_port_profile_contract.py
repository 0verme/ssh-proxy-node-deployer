"""Static instruction checks, not proof of network or deployment behavior."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
README = (ROOT / "README.md").read_text(encoding="utf-8")
ACCEPTANCE = (ROOT / "tests" / "port-profile-acceptance.md").read_text(encoding="utf-8")


class PortProfileContractTests(unittest.TestCase):
    def test_new_install_defaults_and_explicit_high_profile(self):
        for phrase in ("`443/tcp` for REALITY", "`443/udp` for Hysteria2",
                       "`ports-high` for `46690/tcp` and `46691/udp`",
                       "`none` keeps the new-installation default"):
            self.assertIn(phrase, SKILL)
        self.assertIn("Beginner mode always uses the default profile for a new installation", SKILL)

    def test_alias_conflicting_selection_and_no_migration(self):
        self.assertIn("`ports-443` never authorizes migration", SKILL)
        self.assertIn("`ports-high` and `ports-443` are both selected", SKILL)
        self.assertIn("ask the user to choose explicitly before any writes", SKILL)

    def test_conflicts_stop_before_writes_and_never_switch(self):
        for phrase in ("Before any account or deployment write", "wildcard/dual-stack overlap",
                       "container port mappings and forwarding rules", "stop the entire dual-protocol deployment",
                       "Never automatically replace a port", "do not switch modes for the user",
                       "Cancellation or lack of explicit plan confirmation means no writes"):
            self.assertIn(phrase, SKILL)

    def test_existing_and_unknown_installations_are_protected(self):
        for phrase in ("repeated run, maintenance", "ownership/state cannot be established",
                       "preserve existing node ports, client files, firewall rules, certificates, and credentials",
                       "Port migration requires a separate explicit request"):
            self.assertIn(phrase, SKILL)

    def test_acme_existing_trigger_and_challenge_safety(self):
        for phrase in ("If the user provides a domain and confirms DNS control",
                       "If ACME would disrupt an existing service or require an unprovided DNS/cloud credential",
                       "Check TCP/80 for HTTP-01 and TCP/443 for TLS-ALPN-01",
                       "Never stop an existing service to obtain a certificate",
                       "or bypass certificate verification"):
            self.assertIn(phrase, SKILL)

    def test_client_ports_and_ssh_gates_remain_distinct(self):
        for phrase in ("keep server and client ports aligned", "a raw TCP probe",
                       "an SSH authentication probe", "Keep the original root SSH session open throughout"):
            self.assertIn(phrase.lower(), SKILL.lower())

    def test_bilingual_readme_and_no_domain_feature(self):
        for phrase in ("全新安装默认使用 REALITY `443/TCP`", "New installations default to REALITY on `443/TCP`",
                       "端口迁移必须单独明确请求", "port migration requires a separate explicit request",
                       "`ports-high`", "`ports-443`"):
            self.assertIn(phrase, README)
        self.assertNotIn("domain-endpoint", SKILL)
        self.assertNotIn("domain-endpoint", README)

    def test_acceptance_matrix_covers_all_scenarios(self):
        ids = set(re.findall(r"^\| (P\d{2}) \|", ACCEPTANCE, re.MULTILINE))
        self.assertEqual({f"P{i:02d}" for i in range(1, 19)}, ids)

    def test_old_automatic_replacement_is_absent(self):
        for phrase in ("change only that protocol to another unused high port",
                       "choose another available high port for that protocol only",
                       "如端口冲突，只为冲突的协议选择其他可用高位端口"):
            self.assertNotIn(phrase, SKILL + README)


if __name__ == "__main__":
    unittest.main()
