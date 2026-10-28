"""Static checks for the SSH account-initialization instruction contract.

This repository has no account-provisioning executable. These checks prevent
the Skill, README, agent metadata, and acceptance matrix from drifting; they do
not simulate or prove changes on a remote host.
"""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
README = (ROOT / "README.md").read_text(encoding="utf-8")
AGENT = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
ACCEPTANCE = (ROOT / "tests" / "ssh-preflight-acceptance.md").read_text(
    encoding="utf-8"
)


class AccountInitializationContractTests(unittest.TestCase):
    def require_contract(self, phrase, document):
        if phrase not in document:
            self.fail(f"Missing contract fragment: {phrase}")

    def test_all_required_scenarios_are_listed_in_acceptance_matrix(self):
        actual = set(re.findall(r"^\| (T\d{2}) \|", ACCEPTANCE, re.MULTILINE))
        expected = {f"T{number:02d}" for number in range(1, 19)}
        self.assertEqual(expected, actual)

    def test_expert_root_only_enters_three_way_interaction(self):
        required = (
            "Detected SSH login user: root",
            "create a new administrator (recommended)",
            "specify and verify an existing administrator",
            "pause deployment",
        )
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.require_contract(phrase.lower(), SKILL.lower())
        self.require_contract("高手模式可按计划和单独确认安全初始化自定义管理员", README)

    def test_creation_requires_a_validated_name_and_explicit_plan_confirmation(self):
        for phrase in (
            "`[a-z_][a-z0-9_-]{0,31}`",
            "distinct process argument",
            "never interpolate unvalidated input",
            "Ask for an explicit yes/no confirmation",
            "No confirmation, “no”, or cancellation means no account",
        ):
            self.require_contract(phrase, SKILL)

    def test_password_key_and_root_access_safeguards_are_documented(self):
        for phrase in (
            "at least 24 characters",
            "secure non-recording TTY",
            "Before the first write, confirm a safe interactive TTY path is available",
            "Do not enable SSH password authentication",
            "never upload it to the VPS",
            "IdentitiesOnly yes",
            "never overwrite an existing key",
            "Keep the original root SSH session open throughout",
        ):
            with self.subTest(phrase=phrase):
                self.require_contract(phrase.lower(), SKILL.lower())
        self.require_contract("NOPASSWD: ALL", SKILL)

    def test_new_account_uses_standard_tools_and_non_overwriting_ssh_setup(self):
        for phrase in (
            "system's standard account tool",
            "home directory",
            "valid login shell",
            "system's standard administrative group",
            "never add or preserve `NOPASSWD: ALL`",
            "append only the public key idempotently",
            "Validate the existing local SSH config first",
            "ask the user for another alias/key path or to pause",
        ):
            self.require_contract(phrase, SKILL)

    def test_ssh_and_sudo_must_be_verified_independently_before_deployment(self):
        for phrase in (
            "genuinely independent new SSH connection",
            "equals the selected username before any elevation",
            "sudo -l",
            "sudo -k",
            "sudo -v",
            "stop deployment, preserve root access",
        ):
            with self.subTest(phrase=phrase):
                self.require_contract(phrase, SKILL)

    def test_existing_accounts_are_audited_without_credential_or_policy_overwrite(self):
        for phrase in (
            "If the requested username already exists, do not recreate it",
            "or change its password, SSH keys, groups, sudo policy",
            "choose another name or pause",
        ):
            self.require_contract(phrase, SKILL)

    def test_beginner_mode_and_tcp_authentication_gates_remain_distinct(self):
        for phrase in (
            "beginner mode uses `vps` only for its initial-root branch",
            "reuse that exact user and its current authentication",
            "a raw TCP probe",
            "stop before deployment",
            "explicit selection of Beginner mode for this deployment authorizes only",
        ):
            self.require_contract(phrase.lower(), SKILL.lower())

    def test_agent_metadata_describes_the_root_only_flow(self):
        for phrase in ("root-only", "可自选用户名", "等待单独明确确认"):
            self.require_contract(phrase, AGENT)
        self.assertNotIn("高手默认不改账户", AGENT)

    def test_old_default_stop_behavior_is_absent(self):
        stale_phrases = (
            "report the need and stop rather than creating one implicitly",
            "If only root exists, report the need for non-root access and stop",
            "only root is available, report the need and stop unless I explicitly request",
            "高手默认不改账户",
        )
        combined = "\n".join((SKILL, README, AGENT))
        for phrase in stale_phrases:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, combined)


if __name__ == "__main__":
    unittest.main()
