---
name: ssh-proxy-node-deployer
description: Guide users through safe beginner or expert SSH account setup, then deploy a personal sing-box node on an authorized VPS. Beginner account handling is based on the original SSH login identity; expert mode preserves existing accounts by default. Includes read-only checks, rollback, REALITY and Hysteria2 defaults, dual-stack detection, and optional features.
license: MIT
---

# SSH Proxy Node Deployer

Use this skill when the user asks to deploy, rebuild, or maintain a personal proxy node on a VPS they own or administer. It works across hosting providers by using SSH and inspecting the actual OS/network; it does not assume access to a provider console or API. The skill is self-contained: do not rely on another chat or user-specific history.

Use the defaults below whenever the user leaves a deployment choice unspecified. Ask the mode question at onboarding unless the user already chose; otherwise ask only for missing connection details or when a concrete safety conflict needs the user's decision.

## Q&A onboarding: choose a connection mode first

At the start of each deployment, ask this single-choice question in the user's language unless they already chose a mode: “新手模式：按初始 SSH 用户身份创建/复用 `vps` 或复用当前用户，并部署默认节点；高手模式：复用现有 SSH 和账户，自定义高级选项。” Then follow the selected flow. In beginner mode, ask for the server address, the initial SSH username, and port (default `22`). In expert mode, ask for an existing SSH Host alias or configured target.

- **Beginner mode, initial SSH user `root`:** after direct-connect verification and read-only inspection, plan to create `vps` only if it does not exist; audit and safely reuse an existing `vps` without overwriting its password, keys, groups, or other settings. For a newly created `vps`, configure a dedicated Ed25519 key and password-required sudo. For an existing `vps`, reuse its working authentication and sudo as-is; stop if either is missing or conflicting. Independently verify a fresh `vps` SSH login and sudo before deployment. Keep the root system account and its SSH access unchanged by default.
- **Beginner mode, initial SSH user is not `root`:** reuse that exact account (including `ubuntu`, `debian`, `overme`, or `vps`). Never create `vps`, rename the account, or change its password, SSH keys, or SSH policy. Check whether the current account has the required sudo access; if not, report the missing permission and stop before system changes.
- **Expert mode:** reuse the existing SSH user and authentication settings by default. Create or modify an account only when the user explicitly requests a specific account policy. Advanced SSH settings (host, port, alias, key, user strategy, sudo, root-login and password-authentication policy) and node/network options are available only in expert mode; “none” keeps defaults. Prefer a non-root operating account. If only root access exists and there is no already-configured non-root account, report the need and stop rather than creating one implicitly.

The account branch is determined only by the **initial SSH login identity**, captured before any `sudo`, `su`, or other privilege change. Never infer it from the effective user after elevation. If the initial identity cannot be established, stop before account changes.

Ask for only the connection details required by the selected mode. In **expert mode only**, ask once whether the user wants to change defaults or enable optional feature IDs (for example, `ports-443`, a Fusion Monster check, a panel, extra protocols, or network tuning); accepting `无` / `none` keeps the defaults. Do not present or ask about advanced settings in beginner mode. Beginner mode always uses the default profile. If the user selects beginner mode while also asking for an advanced add-on, explain that add-ons are expert-mode choices and ask whether they want to switch modes.

In **both modes**, ask which client app(s) the user uses before generating client files. Allow multiple selections and offer familiar examples such as Shadowrocket, Clash Verge/Mihomo, sing-box, and v2rayN, plus “other” for a named app. This is a normal setup question, not an advanced feature. Generate only formats supported by the selected apps. If the user is unsure, ask what device/operating system they use, check current compatibility when needed, recommend a suitable choice, and get confirmation before generating that format.

If secure interactive password input is unavailable, never move a password into chat, command arguments, environment variables, scripts, shell history, logs, or saved SSH configuration. For a new `vps` account, use a cryptographically secure generator for a password of at least 24 characters and set it only through a non-recording secure terminal; deliver it only through that protected channel. If the terminal cannot safely set and deliver the generated password, ask the user to set it themselves through a secure TTY before continuing. Do not echo or persist the password. Never put private keys in the repository or logs.

## Default profile

- Install sing-box from its current official signed package source for the detected system. Use the official configuration format and validate with the installed version.
- Configure one personal client with VLESS + REALITY + Vision over TCP and Hysteria2 over UDP. Offer IPv4 and IPv6 endpoints only for address families that actually work on the VPS.
- Default to the high-port profile `46690/tcp` for REALITY and `46691/udp` for Hysteria2. Check each socket independently; if one conflicts, change only that protocol to another unused high port. High ports can reduce noise from scans limited to common ports, but they do not hide the VPS IP, stop full-range scans, or replace security controls. Keep port `443` for both transports as the compatibility profile when the user requests it or network/provider testing shows high ports are unusable. TCP and UDP are separate transports, but still check each listener and provider rule independently. Keep server and client settings aligned; never take over an existing listener. SSH alone cannot verify cloud firewall rules, so report the provider-side rules needed and use external tests where possible.
- For REALITY, use a user-supplied target when given. Otherwise try `gateway.icloud.com`, verify the target from the VPS, and use another reachable TLS target only if needed. Do not claim any target or protocol guarantees bypass on every network.
- For Hysteria2, use Salamander obfuscation with a new random secret. If the user provides a domain and confirms DNS control, automatically use the current official ACME workflow for a publicly trusted certificate; this is part of the default profile and does not require a separate preference question. Open TCP/80 temporarily only if required and unused, then close it after issuance. If ACME would disrupt an existing service or require an unprovided DNS/cloud credential, use a new self-signed certificate instead and explain that skipping certificate checks weakens server identity verification.
- Generate new UUIDs, REALITY key pairs, short IDs, HY2 passwords, obfuscation secrets, and certificates for each server/client. Never reuse credentials from a different host.
- Ask which client app(s) the user uses and generate the corresponding supported configuration format(s), with separate IPv4/IPv6 endpoints where supported. Do not assume a default client. Save client files under the current task's designated private output directory (create it if needed), outside the repository and public web roots; apply restrictive permissions where supported. Link the files in the final report. Do not publish a subscription page or QR code by default.
- Keep the sing-box API service and Dashboard disabled by default; node traffic does not depend on them. Leave them disabled on resource-constrained hosts unless the user explicitly requests management access and available resources are suitable. The official Dashboard is served through the API in sing-box 1.14.0 and later; verify the installed version and consult the [official API documentation](https://sing-box.sagernet.org/configuration/service/api/) before enabling it. When enabled, require a strong, non-empty API secret, bind the API to loopback by default, and recommend access through an SSH tunnel. Never expose an unauthenticated API or dashboard publicly.
- Do not install a web panel, subscription server, WARP, additional protocols, BBR/fq tuning, swap, or other system optimizations by default.
- Do not run or download Fusion Monster by default. See the optional checks below.

## SSH and credential handling

- Connect only to the target host the user identifies. Reuse the configured SSH connection in expert mode. When the current authorized login path requires a password, accept it only through a secure interactive terminal after the reachability check. Never put passwords in chat, command arguments, URLs, environment variables, scripts, shell history, logs, or saved SSH configuration.
- Do not execute an unreviewed remote one-click installer or pipe remote content directly to a shell. Use official installation instructions; inspect any script and verify its source before execution.
- Do not echo credentials. Do not disable host-key checking globally. On first connection or a changed fingerprint, verify from a trusted source when possible and stop on an unexplained mismatch.
- Preserve the current SSH port, users, login methods, root access, and keys except for the beginner-mode `root` → new `vps` bootstrap defined below. SSH hardening is optional and requires an explicit user request.

## Account initialization and authentication

- Record the username used for the first SSH login before running any command that changes identity. Use that original login identity for all beginner/expert account decisions, even if a later command runs as root through `sudo` or `su`.
- Run ordinary remote work as a non-root account. If beginner mode starts with root, use that connection only for the read-only audit and the planned one-time `vps` bootstrap; after verifying `vps`, continue through that account and use `sudo` only for system commands that need it. Reuse the original non-root user in the other beginner branch. In expert mode, prefer an existing non-root user; use root only when the user explicitly requests it and the access plan supports recovery.
- In beginner mode with an initial `root` login, include the OS, SSH configuration, existing users, sudo/sudoers environment, current authentication paths, and the existence and state of `vps` in the read-only audit. Report the account plan before any write. If `vps` is absent, create a normal administrative user with a home directory and valid login shell, using the host's standard account tools. If present, reuse it only if its existing authentication and permissions safely support the requested access; do not overwrite or silently repair conflicting state. Stop and report any conflict.
- Give the new `vps` account a unique, cryptographically generated password of at least 24 characters for local account authentication and sudo; SSH access uses its dedicated key. Set and deliver the password only in a secure, non-recording interactive terminal. Do not place it in a command argument, environment variable, script, shell history, transcript, log, chat, or repository. If safe terminal entry and delivery are unavailable, have the user set it through a secure TTY and verify it there; do not continue with an unknown or undisclosed password.
- Only for a newly created `vps`, generate a dedicated local Ed25519 key under `~/.ssh/ssh-proxy-node-deployer/` after confirming the destination path does not exist. Keep the directory and private key restricted (typically `0700` and `0600`). Append its public key idempotently to `authorized_keys`; never truncate or replace that file, existing keys, or local SSH configuration. Use restrictive `.ssh` and `authorized_keys` permissions (typically `0700` and `0600`) only where needed. Add a unique alias containing the server host, `vps` user, SSH port, private-key path, and `IdentitiesOnly yes`, preserving all existing SSH config entries. For an existing `vps`, use its working key and account configuration unchanged.
- Configure password-required sudo only for a newly created `vps`, using the OS's standard admin group or a reviewed sudoers entry. Never configure `NOPASSWD: ALL`. For an existing `vps`, inspect and reuse its current sudo permissions; if insufficient, stop and report the conflict. Validate effective permissions with `sudo -l`; expire any cached sudo timestamp and verify `sudo -v` through an interactive password prompt.
- Keep the original root session open. From a genuinely separate SSH connection, verify the `vps` key login, confirm the remote login identity is `vps` before elevation, and verify password-required sudo succeeds. Do not treat a reused session, `su`, or a post-sudo identity check as independent login verification. If any check fails, stop, preserve the original working access, and report changes already made; do not deploy, disable an access path, or automatically delete the new account.
- In beginner mode with any initial non-root login, reuse that exact user and its current authentication. Read-only check its sudo capability. Do not create `vps`, alter its groups, add keys, change its password, or modify SSH settings. If authentication fails or sudo is insufficient, report the specific failed check and the permission needed; stop without attempting privilege escalation or creating another account.
- In expert mode, leave accounts and authentication untouched unless the user explicitly asks to create or change a named account or SSH policy. Prefer a non-root operating account; never create one implicitly. Inspect and report the proposed delta first; use the same secret handling, backup, independent verification, and rollback safeguards for any requested changes.
- Make account initialization repeatable: inspect whether the account, key, sudo rule, and local SSH alias already exist before writing. Do not duplicate users, key lines, aliases, or sudo rules; an already-correct state needs no change. For existing `vps`, reuse the current settings as-is or stop on a conflict.
- Never disable root SSH login by default. Do so only after a separate explicit request, a verified alternate administrator login, and a tested recovery path plus rollback plan. Check `sshd` syntax before reload/restart, preserve the active SSH session, and verify a second connection before considering the change accepted. Never delete the root system account or blindly modify a firewall.

## Workflow

### 0. Check direct SSH reachability before deployment

After the user selects a mode and provides its required connection details, test the specified SSH port directly from the device and network they intend to use to reach the VPS (port 22 by default). In beginner mode, do this before requesting the password or creating/installing a key. If they specifically want to know whether port 22 is reachable, test 22 even when the configured SSH port differs, and report both results separately.

- Use a short-timeout raw TCP probe, such as PowerShell `Test-NetConnection` on Windows or `nc` on Linux/macOS. This probe does not use SSH `ProxyCommand`/`ProxyJump` or an HTTP/SOCKS application proxy. Do not silently disable a system VPN or tunnel; if one is active, report that the path may still be routed through it. OpenSSH's `ProxyCommand=none` and `ProxyJump=none` disable those SSH proxy settings for an actual SSH probe ([OpenSSH documentation](https://man.openbsd.org/ssh_config)).
- If given a hostname, resolve it using the local resolver and report which address/family was tested. Test IPv4 and IPv6 separately when both are expected to work. Do not send the server IP to third-party checking sites.
- If the agent runs somewhere other than the user's client device/network, do not present that result as the user's direct-connect result. Give the user a local command to run, or clearly label the test location.
- Report a successful TCP handshake as “reachable from this test location”; it does not prove SSH authentication will succeed or that the address is unfiltered everywhere. A refusal usually means the port is closed or actively rejected. A timeout or unreachable result is inconclusive and can come from packet loss, routing, the server/provider firewall, a local network, or filtering.
- Never declare an IP “banned” from one failed probe. Check whether the SSH service uses a different port and whether host/cloud firewall rules or source-IP allowlists explain the result. If direct SSH access is a requirement and the port is unreachable, stop before deployment and report the evidence. Suggest one comparison from an independent network when useful; reachability from another network but not this one points to a network-specific path/filtering issue, not necessarily a globally banned IP.
- Do not fall back to a proxy or replace the server IP automatically. Let the user choose whether to retry from another network, continue via a specified route, or ask the provider about changing the IP.

### 1. Identify the host and inspect it before changes

If the SSH target or login method is missing, ask only for that detail. Validate the hostname/IP; do not connect over the public Internet to documentation, private, loopback, link-local, or reserved addresses unless the user confirms a private route/VPN. Then run read-only checks for:

- Distribution/release, architecture, package manager, systemd, available CPU/memory/disk, current sing-box installation and configuration.
- Public IPv4/IPv6 addresses, default routes, and whether each family is usable for inbound traffic. An assigned IPv6 address alone does not prove IPv6 reachability.
- TCP/UDP listeners and conflicts with the requested ports.
- Host firewall and existing rules. Keep these separate from cloud-provider firewall/security-group rules, which may not be visible over SSH.
- Services or configurations that a deployment might overwrite.

Do not perform a broad OS upgrade. If the OS/architecture is unsupported by current official sing-box installation guidance, or a safe install would overwrite an unrelated service, explain the specific issue and pause before changing it.

### 2. Account initialization and independent verification

After the read-only audit, report the deployment and account plan before any write. Then follow the account policy above: initialize `vps` only for beginner mode whose **initial** SSH user is root; otherwise reuse the initial user. Complete independent authentication and sudo checks before installing or changing sing-box. If the user requested assessment only, stop after reporting findings. If an account conflict, missing secure TTY, insufficient permissions, failed login, or failed sudo check prevents safe continuation, stop and explain the reason.

### 3. Optional machine benchmark

Run Fusion Monster only when the user explicitly asks for a machine check, benchmark, or performance test. Use the maintained Go edition from the [official oneclickvirt/ecs repository](https://github.com/oneclickvirt/ecs), resolve one official release, download the matching OS/architecture asset, and verify it against that release's SHA-256 file before execution. Run it from a unique temporary directory; do not pipe an unreviewed script to a shell or install the benchmark globally.

When the user requests a basic check, use the current release's documented system-only profile: disable CPU, memory, disk, speed, route, media/IP-quality suites, logging, and public result upload; verify the upload-off flag and bound runtime to 25 seconds. Basic IP lookups may still send the VPS public IP to third-party information services; tell the user before running. If upload cannot be disabled, checksum verification fails, or a reliable time limit is unavailable, skip the benchmark. Clean only this run's temporary files on success, failure, timeout, or interruption, then continue deployment unless a finding makes the VPS unsafe or unsuitable.

Full benchmark mode is opt-in. It can create CPU/disk load and consume substantial bandwidth, so run it only when the user explicitly requests comprehensive tests. Never publish results unless the user explicitly asks.

### 4. Install with minimal, reversible changes

- Choose the official package instructions for the detected Linux distribution. Do not run unrelated repositories' one-line installers as root. If installing from a binary release, verify its official checksum/signature before use.
- If sing-box or its configuration already exists, inspect and back it up before changes. Add or update only the requested inbound; do not replace unrelated configuration or remove an existing service. If safe coexistence is not possible, pause and explain the conflict.
- Write secrets in protected files (directory `0700`, files `0600` where suitable). Keep Hysteria2 certificate/key private. Use the service account/permissions specified by the official package when possible.
- Validate configuration before restarting. Keep a rollback copy and do not reboot.

### 5. Preserve firewall and SSH access

- If a host firewall is active, add only the exact TCP/UDP node-port rules while preserving its existing policy. For HTTP-based ACME validation, open TCP/80 temporarily and remove that rule after issuance. Do not flush rules or replace the firewall implementation.
- If no host firewall is active, leave it that way by default; report the cloud firewall/security-group rules the user needs to add. Enabling a host firewall is an opt-in feature.
- If the user explicitly asks to enable a firewall or harden SSH, protect the current session, preserve the real SSH port, and use a timed rollback when supported. Verify a second SSH login before removing old access or canceling rollback. If access cannot be protected, stop before the risky change.
- Never claim to have changed a provider firewall unless an authorized provider integration was actually used.

### 6. Verify and deliver

- Check configuration validity, service health, listening sockets, firewall rules, and logs without exposing secrets.
- Test REALITY and HY2 over every available address family. Prefer a real client from outside the VPS. Label server-side self-tests separately from external tests; do not claim a handshake or usable tunnel without evidence.
- Generate configurations for the client app(s) selected during onboarding, with separate IPv4/IPv6 endpoints where supported. Generate QR codes or a private HTTPS subscription only when requested.
- Keep client files private and out of repositories, public pages, and commits. Do not print full credentials in progress updates.

## Optional features

The README lists stable feature IDs. The user can write `可选项：feature-id, feature-id` or `Optional features: feature-id, feature-id`; ordinary language requests count too. Enable only the named options. An omitted list, an empty list, or `无` / `none` means keep the default profile with no optional features. If an ID is unknown or its requested scope is unclear, ask instead of guessing. Feature IDs do not bypass the safety checks below or elsewhere in this skill.

Supported IDs:

- `ports-443`: use TCP/443 for REALITY and UDP/443 for Hysteria2. Check both listeners and provider rules independently; this is a compatibility choice, not an IP-hiding or security guarantee.
- `fusion-basic`: run the documented, time-limited basic Fusion Monster check with upload and heavy suites disabled. Tell the user first that basic IP lookups may send the VPS public IP to third-party services.
- `fusion-full`: run a full benchmark only after explaining that it can load CPU/disk and consume substantial bandwidth. Never publish results unless separately asked.
- `firewall-ufw` / `firewall-firewalld`: set up the named host firewall only after checking current rules and preserving SSH access; do not replace an existing firewall blindly.
- `ssh-hardening`: harden SSH only after testing an alternate administrator login and preparing rollback. Confirm the intended changes if the user has not specified them.
- `protocol-anytls`, `protocol-tuic`, `protocol-shadowsocks`: add the named protocol. `protocol-other` requires the user to name the protocol.
- `multi-user`: add multiple users and separate credentials. `traffic-accounting`: add traffic/quota tracking; explain storage and accuracy limits before choosing a method.
- `warp`: configure WARP. `bbr-fq`: apply BBR/fq tuning. `swap`: configure swap. `udp-buffer-tuning`: change UDP buffer settings. Check compatibility and impact before applying system-wide changes.
- `sing-box-dashboard`: enable the official Dashboard only on sing-box 1.14.0 or later. Check resource headroom; keep it off on low-resource hosts unless the user explicitly accepts the trade-off. Require a strong, non-empty API secret and loopback binding with SSH-tunnel access by default. Direct remote exposure still requires a separate explicit request, TLS, and strict network restrictions.
- `third-party-panel`: install a third-party panel only when the user names the panel or approves a clearly described choice. Check resources, supported installation method, and exposure/security requirements first.
- `private-subscription`: create a private HTTPS subscription; keep it access-controlled and out of public repositories/pages. A domain-backed ACME certificate remains the default when the user provides a domain and controls its DNS.
- `qr-code`: generate QR codes for client configurations; treat them as credentials and save/share them only through the same private path as client files.

## Finish with a concise report

Summarize the detected OS, sing-box version, addresses actually usable, selected ports, firewall/provider rules, backup/config paths, client files, and validation results. State which checks were external versus server-side. Call out any optional feature that was skipped and why. Redact passwords and private keys.
