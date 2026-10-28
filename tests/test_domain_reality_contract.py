"""Offline static contract and mock acceptance coverage; no network operations."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
README = (ROOT / "README.md").read_text(encoding="utf-8")
MATRIX = (ROOT / "tests/domain-reality-acceptance.md").read_text(encoding="utf-8")
CONTRACT = SKILL.split("## Expert domain and REALITY target contract", 1)[1].split("## Finish", 1)[0]

class DomainRealityContractTests(unittest.TestCase):
    def require(self, *phrases):
        for phrase in phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, CONTRACT)

    def test_modes_and_combinations(self):
        self.require("not environment variables parsed", "No owned domain is required", "does not enable `domain-endpoint`", "does not enable `reality-nearby-target` or `reality-custom-target`", "Both target feature IDs together", "`none` combined with feature IDs", "before any writes", "may be combined with either target feature and with `ports-high`")

    def test_dns_and_endpoint_isolation(self):
        self.require("A, AAAA and CNAME", "Compare each final address", "actual IPv4/IPv6 availability", "ordinary CDN proxying", "DNS-only cannot be proved solely", "Do not create or change DNS records", "Only put the domain in explicitly authorized client connection address fields", "separate roles")

    def test_passive_discovery_and_tls_evidence(self):
        self.require("read-only observation", "public passive sources", "no entire /24 bulk port scan", "not proof of ownership", "TLS 1.3", "HTTP/2 ALPN", "certificate chain", "hostname and validity", "redirect destination", "at most five", "reject loopback/self-target risks", "unknown metrics")

    def test_choice_failure_and_existing_nodes(self):
        self.require("keep the existing configuration and target", "explicitly choose a nearby candidate", "require explicit confirmation before any write", "Cancellation or no confirmation", "Existing nodes are never migrated", "separate explicit request")

    def test_ordered_candidate_workflow_is_opt_in_and_confirmed(self):
        self.require("explicitly chooses the expert nearby-target workflow", "(1) discover same-ASN", "(2) if none qualifies", "(3) if those do not qualify", "Ask before moving to the major-provider or user-owned alternative", "sequential mode transition", "not automatic failover", "Reject any target whose resolution or routing can loop back", "preserve the current configuration", "for a new installation without an existing target", "separately confirmed change plan", "`none`, beginner mode and default target behavior remain unchanged", "do not silently broaden or override it")

    def test_version_specific_fields(self):
        self.require("`reality.handshake.server` / `reality.handshake.server_port`", "do not copy Xray fields", "installed version", "validate the client/server pairing")

    def test_simulated_acceptance_scenarios_are_present(self):
        self.assertEqual({f"D{i:02d}" for i in range(1, 22)}, set(re.findall(r"^\| (D\d{2}) \|", MATRIX, re.M)))
        for evidence in ("192.0.2.10", "mock ASN unavailable", "certificate mismatch", "user cancels", "at most five"):
            self.assertIn(evidence, MATRIX)

    def test_readme_is_bilingual_and_example_is_not_runtime_parser(self):
        for phrase in ("高手模式：域名入口与 REALITY 目标", "Expert mode: domain endpoint and REALITY target", "并非环境变量解析器", "not an environment-variable parser", "Hysteria2", "`same-prefix24`"):
            self.assertIn(phrase, README)

if __name__ == "__main__":
    unittest.main()
