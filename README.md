# SSH Proxy Node Deployer

让 AI Agent 通过 SSH，谨慎检查并部署自用 sing-box 节点。

An Agent Skill for inspecting and deploying a personal sing-box node over SSH.

[中文快速开始](#中文快速开始) · [English Quick Start](#english-quick-start) · [高级功能](#高级功能--advanced-features) · [安全与文档](#安全与文档--security-and-documentation)

![Deployment workflow: inspect, plan, deploy, and deliver private client files](assets/deployment-workflow.svg)

这是一个 **Agent Skill**，不是传统一键安装脚本。仅用于你拥有或获授权管理的 Linux 服务器；[SKILL.md](SKILL.md) 是权威执行规范。

## 中文快速开始

### 1. 安装或仅用于当前任务

将以下提示词发送给 Agent：

```text
请从 https://github.com/0verme/ssh-proxy-node-deployer 安装 ssh-proxy-node-deployer Skill，入口是根目录 SKILL.md。使用当前平台的标准安装方式并告诉我如何调用；如已存在同名 Skill，先告诉我更新方式，不要覆盖。如不支持持久安装，请仅在当前任务读取并遵循，勿声称已安装。
```

无需安装，仅在当前任务使用：

```text
请读取 https://raw.githubusercontent.com/0verme/ssh-proxy-node-deployer/main/SKILL.md，并仅在本次任务中遵循它。
```

### 2. 选择模式并发送提示词

替换占位符；`CLIENT` 可填写 Shadowrocket、Clash Verge / Mihomo、sing-box、v2rayN 等。其他必要信息由 Agent 交互收集。**不要在聊天中输入密码、私钥或其他敏感凭据。**

**新手模式：**

```text
使用 ssh-proxy-node-deployer Skill，以新手模式部署我有权管理的服务器：
SERVER_IP=<服务器 IP>
SSH_USER=<初始 SSH 用户>
SSH_PORT=<SSH 端口，如 22>
CLIENT=<客户端名称>
先按照 SKILL.md 完成只读检查、展示计划和必要确认；保留现有 SSH 访问和服务，不得跳过安全检查。
```

**高手模式：** `SSH_HOST` 是现有 SSH Config 的 Host 别名；不需要高级功能时保留 `none`。

```text
使用 ssh-proxy-node-deployer Skill，以高手模式部署我有权管理的服务器：
SSH_HOST=<现有 SSH Host 别名>
OPTIONAL_FEATURES=none
先按照 SKILL.md 完成只读检查、展示计划和必要确认；保留现有 SSH 访问和服务，不得跳过安全检查。
```

高手模式会在需要时询问客户端及所选功能的其他参数。只读评估时，可明确要求“仅检查并报告，不安装或修改配置”。

## English Quick Start

This is an **Agent Skill**, not a one-click installer. Use it only on Linux servers you own or are authorized to administer. [SKILL.md](SKILL.md) is the authoritative execution contract.

### 1. Install or use for this task only

Send this prompt to your agent:

```text
Install the ssh-proxy-node-deployer Skill from https://github.com/0verme/ssh-proxy-node-deployer; its entry point is SKILL.md at the repository root. Use this platform's standard installation method and explain how to invoke it. If it already exists, explain how to update it before overwriting. If persistent installation is unsupported, read and follow it for this task only; do not claim it was installed.
```

For this task only, without installation:

```text
Read https://raw.githubusercontent.com/0verme/ssh-proxy-node-deployer/main/SKILL.md and follow it for this task only.
```

### 2. Choose a mode and send a prompt

Replace the placeholders. `CLIENT` can be Shadowrocket, Clash Verge / Mihomo, sing-box, v2rayN, or another client. The agent collects other required details interactively. **Do not put passwords, private keys, or other secrets in chat.**

**Beginner mode:**

```text
Use the ssh-proxy-node-deployer Skill in Beginner mode on a server I am authorized to administer:
SERVER_IP=<server IP>
SSH_USER=<initial SSH user>
SSH_PORT=<SSH port, e.g. 22>
CLIENT=<client name>
Follow SKILL.md for read-only checks, the plan, and required confirmations; preserve existing SSH access and services and do not skip safety checks.
```

**Expert mode:** `SSH_HOST` is an existing SSH Config Host alias; keep `none` for defaults.

```text
Use the ssh-proxy-node-deployer Skill in Expert mode on a server I am authorized to administer:
SSH_HOST=<existing SSH Host alias>
OPTIONAL_FEATURES=none
Follow SKILL.md for read-only checks, the plan, and required confirmations; preserve existing SSH access and services and do not skip safety checks.
```

The agent asks for the client and any other details required by your selections. For an assessment only, request read-only checks and no installation or configuration changes.

## 默认行为 / Defaults

- 新安装使用 **VLESS + REALITY + Vision** (`443/TCP`) 和 **Hysteria2** (`443/UDP`)。任一端口冲突或无法确认可用时停止，不自动换端口；443 不保证连接成功或免于识别、封锁。
- 新手模式仅在初始 SSH 用户为 `root` 时安全创建或复用 `vps`；否则复用初始非 root 用户。高手模式可按计划和单独确认安全初始化自定义管理员，并验证 SSH 和 sudo。
- 默认保留 root SSH、现有 SSH 登录方式和已有服务；已有节点不自动迁移。操作前只读检查、展示计划并取得必要确认。
- Hysteria2 不默认关闭 TLS 证书验证。自签证书须安全验证服务器身份；客户端无法可靠验证时，不交付该客户端的 HY2 配置。
- 融合怪和管理面板默认不启用。客户端配置和二维码包含私密凭据，须保存在仓库外的私有位置。

- New installations use **VLESS + REALITY + Vision** (`443/TCP`) and **Hysteria2** (`443/UDP`). A conflict or uncertain availability stops deployment without automatically changing ports; 443 does not guarantee connectivity or prevent identification or blocking.
- Beginner mode safely creates or reuses `vps` only when the initial SSH user is `root`; otherwise it reuses the initial non-root user. Expert mode can safely initialize a custom administrator after a plan and separate confirmation, with SSH and sudo verification.
- Existing root SSH access, SSH login methods, and services are preserved by default. Existing nodes are not automatically migrated. Read-only checks, a plan, and required confirmations precede changes.
- Hysteria2 does not disable TLS certificate verification by default. Self-signed identities must be verified securely; withhold a client's HY2 profile if it cannot verify the identity reliably.
- Fusion Monster and management panels are off by default. Client profiles and QR codes are private credentials; keep them in a private location outside the repository.

## 高级功能 / Advanced features

仅高手模式明确选择以下功能；`OPTIONAL_FEATURES=none` 保留默认值。选择功能后，Agent 会收集所需参数并按 Skill 验证、确认。Expert mode requires explicit selection; the agent collects the remaining parameters and follows the Skill's checks and confirmations.

| 功能 / Feature | 作用 / Purpose |
| --- | --- |
| `ports-high` | 新安装改用 REALITY `46690/TCP` + Hysteria2 `46691/UDP`；冲突时停止。Explicit high-port profile for new installations; stop on conflict. |
| `domain-endpoint` | 使用你控制的域名作为获授权的客户端连接地址。Use your domain for authorized client connection addresses. |
| `reality-nearby-target` | 被动发现并由用户选择握手目标。Passively discover candidates and let the user choose a handshake target. |
| `reality-custom-target` | 使用用户指定并经验证、确认的握手目标。Use a user-specified, verified and confirmed handshake target. |

`reality-nearby-target` 与 `reality-custom-target` 互斥；`domain-endpoint` 不会自动启用任一目标功能，可与其中一个及 `ports-high` 组合。`ports-443` 是新安装默认端口的兼容别名，与 `ports-high` 同选时须明确择一；它不授权迁移。仅提供域名或目标参数不等于选择相应功能。同 ASN 或同网段不代表确定的安全等级。

The two REALITY target features are mutually exclusive; `domain-endpoint` enables neither and can be combined with either and `ports-high`. `ports-443` is a new-installation default alias, conflicts with `ports-high`, and does not authorize migration. A domain or target parameter alone does not select a feature. A shared ASN or subnet is not a security guarantee.

其他可选功能包括测速、额外协议、防火墙、SSH 加固、网络调优、面板和私有订阅；完整代码、组合限制和执行规则见 [Optional features](SKILL.md#optional-features) 与 [Expert domain and REALITY target contract](SKILL.md#expert-domain-and-reality-target-contract)。

Other options include benchmarks, extra protocols, firewall and SSH changes, tuning, panels, and private subscriptions. See [Optional features](SKILL.md#optional-features) and the [domain and REALITY contract](SKILL.md#expert-domain-and-reality-target-contract) for all IDs and constraints.

## 真实使用截图 / Real session screenshots

以下是真实会话截图，展示会话步骤及 Agent 当时报告的结果；本次 README 修改没有独立重跑 VPS、客户端或网络测试。The images show actual sessions and the agent's reports; VPS, client and network results were not independently rerun for this README update.

![在当前任务读取 Skill / Reading the Skill for the current task](assets/screenshots/01-skill-read-in-current-task.png)

1. 当前任务读取 Skill；截图显示未安装到后续会话。The Skill was read for this task, not installed for later sessions.

![高手模式部署会话 / Expert deployment session](assets/screenshots/02-expert-mode-vps-deployment.png)

2. 会话报告部署及 Mihomo IPv4/IPv6 连通和本地配置检查成功；Shadowrocket 链接尚未在 iOS 导入验证。The session reports deployment and Mihomo IPv4/IPv6 and local profile checks; the Shadowrocket link was not imported on iOS.

![融合怪评测报告 / Fusion Monster benchmark report](assets/screenshots/03-fusion-monster-benchmark.png)

3. 会话报告融合怪完整评测，运行约 8 分 7 秒。The session reports a full Fusion Monster benchmark of about 8 minutes 7 seconds.

## 安全与文档 / Security and documentation

- [SKILL.md](SKILL.md)：执行规范、账户初始化、SSH 检查、证书验证与可选功能。Execution contract, account initialization, SSH checks, certificate verification, and optional features.
- [验收用例 / Acceptance scenarios](tests/)：离线契约及验收材料，不能替代真实部署验证。Offline contracts and acceptance material do not prove a real deployment.
- 分享日志前移除密码、私钥、UUID、订阅链接、真实 IP 等敏感信息；安全问题请通过 GitHub 私下联系维护者。Remove secrets and identifying server details before sharing logs; report security issues privately to the maintainer through GitHub.

## License

[MIT](LICENSE)
