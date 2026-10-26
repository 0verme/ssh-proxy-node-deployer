<div align="center">

# SSH Proxy Node Deployer

**让 AI Agent 通过 SSH，为你检查并部署一台自用的 sing-box 节点。**  
**Let an AI agent inspect and deploy a personal sing-box node over SSH.**

[中文](#中文) · [English](#english) · [安全说明](#安全说明--security) · [License](#license)

<img src="assets/deployment-workflow.svg" alt="Deployment workflow: connect over SSH, inspect safely, deploy, and receive private client files" width="900">

</div>

## 中文

这是一个面向 AI Agent 的可复用 Skill。给 Agent 提供一台你有权管理的 Linux VPS 的 SSH 登录方式后，它会先检查系统、网络、端口和现有服务，再按需部署并生成客户端配置。它不绑定云厂商，也不依赖此前的聊天记录。

它提供一套谨慎的默认方案，不是一个盲目执行的安装脚本：关键步骤会根据服务器现状决定；遇到可能覆盖现有服务、系统不受支持或访问安全无法保证时，会先停下来说明情况。

### 默认行为

- 使用 sing-box，部署 VLESS + REALITY + Vision（TCP）和 Hysteria2（UDP）。
- 默认使用高位端口：REALITY `46690/TCP`，Hysteria2 `46691/UDP`。如端口冲突，只为冲突的协议选择其他可用高位端口。`443` 是兼容选项，不是默认端口。
- 部署前从实际使用的客户端网络直测 SSH `22/TCP`（或你指定的 SSH 端口），不走 SSH 跳板或应用层代理。失败只说明当前测试位置无法直连，不能单凭一次失败断定 IP 被封；会先停止部署并报告可能原因，不会自动换 IP 或切换代理。
- 按实际可达性判断 IPv4 / IPv6；有地址不代表从公网一定能连通。
- 有域名且你能控制 DNS 时，默认尝试申请受信任的 ACME 证书；否则用新生成的自签证书，并说明客户端验证身份的取舍。
- 默认生成 Shadowrocket 链接和 Clash Verge / Mihomo 配置，保存在仓库之外的私有目录。
- 默认保留现有 SSH 登录方式、主机防火墙策略和其他服务；不重启整台机器。sing-box API / Dashboard 和第三方面板默认关闭；节点转发不依赖管理页，低配机器建议保持关闭。
- **默认不下载、不运行融合怪。** 只有你明确要求测速或机器评测时才运行；完整测试可能增加 CPU、磁盘负载和流量。

高位端口只能减少部分只扫描常见端口的噪声，不能隐藏服务器 IP，也挡不住全端口扫描。请结合云厂商安全组、防火墙和账户安全设置使用。

如果 Agent 不在你实际使用的网络中，可在本机先测 SSH 端口（替换服务器 IP；自定义 SSH 端口时替换 `22`）：

```powershell
Test-NetConnection -ComputerName "SERVER_IP" -Port 22 -InformationLevel Detailed
```

macOS / Linux 可用：

```bash
nc -vz -w 5 SERVER_IP 22
```

这只检查当前网络到该 TCP 端口是否可达，不验证 SSH 用户名/密钥，也不能单独证明 IP 被封。

### 首次安装

通常只需安装一次；后续调用方式由 Agent 平台决定。

**通用安装提示词**

```text
请从公开 GitHub 仓库 https://github.com/0verme/ssh-proxy-node-deployer 安装名为 ssh-proxy-node-deployer 的 Skill。
入口文件在仓库根目录的 SKILL.md。请使用当前 Agent 平台支持的标准安装方式，
并告诉我之后如何调用。如果平台不支持持久安装，请读取该文件并只在当前任务中遵循，
不要声称已经为后续会话安装。如果已存在同名 Skill，先告诉我更新方式，不要覆盖。
```

**只在当前任务使用，不做持久安装**

```text
请读取 https://raw.githubusercontent.com/0verme/ssh-proxy-node-deployer/main/SKILL.md，
并在本次任务中遵循其中的说明。这不会安装到后续会话。
```

<details>
<summary>Codex 安装与手动备用方式（可选）</summary>

**Codex 快捷方式**

```text
$skill-installer 请从 0verme/ssh-proxy-node-deployer 仓库根目录安装 Skill，入口文件为 SKILL.md，名称为 ssh-proxy-node-deployer。如果同名 Skill 已存在，先告诉我更新方式，不要覆盖。
```

Codex 手动安装备用方式：

Windows PowerShell：

```powershell
$skills = Join-Path $HOME ".codex\skills"
New-Item -ItemType Directory -Force $skills | Out-Null
git clone https://github.com/0verme/ssh-proxy-node-deployer.git (Join-Path $skills "ssh-proxy-node-deployer")
```

macOS / Linux：

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/0verme/ssh-proxy-node-deployer.git ~/.codex/skills/ssh-proxy-node-deployer
```

其他平台的持久安装目录和调用方式不同，请使用其标准 Skill 安装功能或配置的 Skills 目录。安装后可能需要重新加载 Agent。

</details>

### 给 Agent 的提示词

把 SSH 地址、用户名和端口告诉 Agent；**密码不要粘贴到聊天里**。优先使用已经配置好的 SSH 密钥或 SSH Agent。若必须用密码，使用 Agent 提供的安全交互式终端输入。

```text
使用 ssh-proxy-node-deployer Skill，在我有权管理的 VPS 上部署自用节点。
SSH 主机：<IP 或域名>
SSH 用户：<用户名>
SSH 端口：<端口；默认 22>

先做只读检查并报告计划，再实施安全且可回滚的步骤。按默认方案使用高位端口；
保留现有 SSH 和防火墙策略。融合怪不要运行，除非我之后明确要求。
部署前从我实际使用的客户端网络直测 SSH 22/TCP，不走 SSH 跳板或应用层代理；
如果你无法从我的客户端网络测试，先给我本机测试命令。测试失败时不要直接说 IP 被封，
先停止部署并报告原因，不要自动切换代理或更换 IP。
客户端配置请放在仓库外的私有目录，不要把密码或私钥写入聊天、仓库或日志。
```

如果希望先检查而不部署，可以这样说：

```text
使用 ssh-proxy-node-deployer 检查这台 VPS 是否适合部署。先只读检查并给我报告，
暂时不要安装软件、修改配置或防火墙。
```

### 可选功能

可以直接说中文功能名，也可以使用下表的功能码。复制下面的格式，并只保留你需要的项目：

```text
可选项：sing-box-dashboard, protocol-anytls
```

省略“可选项”或写 `可选项：无`，表示使用默认功能，不启用任何额外功能。Agent 只启用列出的项目；不认识的功能码或描述不清的范围会先向你确认。功能码不会跳过安全检查。

| 功能码 | 启用内容 | 注意事项 |
| --- | --- | --- |
| `ports-443` | REALITY 使用 TCP/443，Hysteria2 使用 UDP/443 | 两个端口和云安全组规则分别检查；这是兼容选项，不会隐藏 IP。 |
| `fusion-basic` | 融合怪基础检查 | 轻量、限时并关闭上传和重负载测试；运行前会告知基础 IP 查询可能把 VPS 公网 IP 发送给第三方。 |
| `fusion-full` | 融合怪完整评测 | 会产生 CPU / 磁盘负载和额外流量。 |
| `firewall-ufw` / `firewall-firewalld` | 配置对应的主机防火墙 | 先检查现有规则并确保 SSH 不会被锁在外面；不会盲目替换现有防火墙。 |
| `ssh-hardening` | SSH 加固，例如禁用密码登录 | 先验证备用管理员登录并准备回滚；未说明具体改动时会先确认。 |
| `protocol-anytls` / `protocol-tuic` / `protocol-shadowsocks` / `protocol-other` | 添加对应协议 | 使用 `protocol-other` 时需同时写明协议名称。 |
| `multi-user` / `traffic-accounting` | 多用户凭据 / 流量或配额统计 | 统计方式可能有存储和准确性限制，部署前会说明。 |
| `warp` | 配置 WARP | 先检查系统兼容性及路由影响。 |
| `bbr-fq` / `swap` / `udp-buffer-tuning` | BBR/fq、交换空间 / UDP 缓冲区调优 | 检查兼容性和系统影响后再修改。 |
| `sing-box-dashboard` | sing-box 官方 Dashboard（1.14.0+） | 先检查资源；低配机器默认不启用。使用强 API 密钥、本机监听和 SSH 隧道。直接公网开放需要单独明确要求、TLS 和严格网络限制。详见 [sing-box 官方 API 文档](https://sing-box.sagernet.org/configuration/service/api/)。 |
| `third-party-panel` | 第三方面板 | 请同时写出面板名称；先检查资源、安装来源和访问安全。 |
| `private-subscription` | 私有 HTTPS 订阅 | 需保持访问受控，不放入公开仓库或网页。 |
| `qr-code` | 客户端配置二维码 | 二维码包含连接凭据，按私密配置文件同等保护。 |
| `client-format-sing-box` / `client-format-v2rayn` | 额外导出对应客户端格式 | 默认仍提供 Shadowrocket 和 Clash Verge / Mihomo 配置。 |

### 图片与实际测试

上方图片是工作流程示意图，不是某台服务器的测试结果。真实部署截图、客户端连通截图和融合怪输出会在完成真实机器测试后补充；本仓库不会用虚构结果冒充实测。

### 适用范围

- 目标是你拥有或明确获准管理的 Linux VPS。
- Agent 需要能够使用 SSH，并在必要时安全地交互式输入凭据。
- 服务器能访问 sing-box 官方软件源；IPv4、IPv6 和云安全组情况因服务商与实例而异。
- 当前 Skill 是 Agent 执行指南，不是独立的一键安装程序，也不保证任何网络环境都可连接。

## English

This is a reusable Skill for AI agents. Give your agent SSH access to a Linux VPS you own or are authorized to administer. It inspects the operating system, network, ports, and existing services before making changes, then deploys a personal node and creates client profiles as appropriate. It is provider-independent and does not rely on previous chat history.

This is a cautious operating guide, not a blind installer. The agent adapts to the host and pauses when it finds an unsafe conflict, an unsupported system, or a change that could jeopardize access.

### Defaults

- sing-box with VLESS + REALITY + Vision over TCP and Hysteria2 over UDP.
- High ports by default: REALITY on `46690/TCP`, Hysteria2 on `46691/UDP`. If a port is occupied, choose another available high port for that protocol only. Port `443` is an opt-in compatibility profile.
- Before deployment, test SSH TCP/22 (or the specified SSH port) directly from the actual client network, without an SSH jump host or application proxy. A failure only shows that the current test location cannot connect; it does not prove the IP is banned. Stop and report likely causes instead of switching proxies or replacing the IP automatically.
- Detect IPv4 and IPv6 based on actual reachability; an assigned address alone does not prove public connectivity.
- If you provide a domain and control its DNS, try to obtain a trusted ACME certificate by default. Otherwise, create a fresh self-signed certificate and explain the client identity-verification trade-off.
- Generate Shadowrocket links and a Clash Verge / Mihomo profile by default. Keep client files in a private directory outside the repository.
- Preserve existing SSH access, host firewall policy, and unrelated services. Do not reboot the VPS. Keep the sing-box API / Dashboard and third-party panels disabled by default; node traffic does not depend on a management page, and low-resource hosts should normally leave it off.
- **Fusion Monster is off by default.** Run it only when explicitly requested. A full benchmark can use CPU, disk, and network bandwidth.

High ports can reduce noise from scans limited to common ports. They do not hide the VPS IP or prevent full-range scans. Use cloud firewall rules and sound account security as well.

If your agent is not running on the network you will use, test the SSH port locally (replace the server IP and use your custom SSH port instead of `22` when applicable):

```powershell
Test-NetConnection -ComputerName "SERVER_IP" -Port 22 -InformationLevel Detailed
```

On macOS / Linux:

```bash
nc -vz -w 5 SERVER_IP 22
```

This only tests whether the current network can reach the TCP port; it does not validate SSH credentials or prove the IP is banned.

### First-time setup

You usually install the Skill once. The persistent install location and invocation syntax depend on your agent platform.

**Generic installation prompt**

```text
Install the Skill named ssh-proxy-node-deployer from the public GitHub repository
https://github.com/0verme/ssh-proxy-node-deployer. Its entrypoint is SKILL.md at the
repository root. Use the standard installation method for this agent platform and
tell me how to invoke it later. If persistent installation is unsupported, read the
file and follow it for this task only; do not claim it is installed for future
sessions. If a Skill with that name already exists, tell me how to update it and
do not overwrite it.
```

**Use for this task only, without persistent installation**

```text
Read https://raw.githubusercontent.com/0verme/ssh-proxy-node-deployer/main/SKILL.md
and follow it for this task. This does not install the Skill for future sessions.
```

<details>
<summary>Optional Codex installation and manual fallback</summary>

**Codex shortcut**

```text
$skill-installer Install the Skill from the root of 0verme/ssh-proxy-node-deployer.
Its entrypoint is SKILL.md and its name is ssh-proxy-node-deployer. If that Skill
already exists, tell me how to update it; do not overwrite it.
```

Codex manual fallback:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/0verme/ssh-proxy-node-deployer.git ~/.codex/skills/ssh-proxy-node-deployer
```

On Windows, clone into `%USERPROFILE%\.codex\skills\ssh-proxy-node-deployer`. Other platforms use their configured Skills directory and invocation syntax. Reload the agent if needed.

</details>

### Prompt your agent

Provide the SSH host, username, and port. **Do not paste a password into chat.** Prefer an existing SSH key or SSH agent. If password login is necessary, enter it only through the agent's secure interactive terminal.

```text
Use the ssh-proxy-node-deployer Skill to deploy a personal node on a VPS I own
or am authorized to administer.
SSH host: <IP address or hostname>
SSH user: <username>
SSH port: <port; default 22>

Start with read-only checks and report the plan. Use the default high-port profile,
preserve existing SSH access and firewall policy, and make reversible changes.
Before deployment, test SSH TCP/22 directly from the client network I will use,
without an SSH jump host or application proxy. If you cannot test from that network,
give me a local command to run. If it fails, report that it is unreachable from this
test location, stop deployment, and do not automatically switch proxy or IP.
Do not run Fusion Monster unless I explicitly ask later. Save client profiles in a
private directory outside the repository. Never put passwords or private keys in
chat, the repository, or logs.
```

To inspect without deploying:

```text
Use ssh-proxy-node-deployer to assess whether this VPS is suitable. Perform
read-only checks and report your findings. Do not install software or change
configuration or firewall rules yet.
```

### Optional features

You can name a feature in plain language or copy its ID from the table below. For example:

```text
Optional features: sing-box-dashboard, protocol-anytls
```

Omit this line or write `Optional features: none` to keep the default profile without add-ons. The agent enables only the listed features. Unknown IDs or unclear scope require clarification; IDs do not bypass safety checks.

| Feature ID | Enables | Notes |
| --- | --- | --- |
| `ports-443` | REALITY on TCP/443 and Hysteria2 on UDP/443 | Check both listeners and provider rules independently. This compatibility option does not hide the IP. |
| `fusion-basic` | Basic Fusion Monster check | Time-limited, with uploads and heavy suites disabled. Basic IP lookups may send the VPS public IP to third parties; the agent will tell you before running it. |
| `fusion-full` | Full Fusion Monster benchmark | Adds CPU/disk load and network traffic. |
| `firewall-ufw` / `firewall-firewalld` | Configure the named host firewall | Check existing rules and preserve SSH access; do not blindly replace an existing firewall. |
| `ssh-hardening` | SSH hardening, such as disabling password login | Test alternate administrator access and prepare rollback first; clarify unspecified changes. |
| `protocol-anytls` / `protocol-tuic` / `protocol-shadowsocks` / `protocol-other` | Add the named protocol | Name the protocol when using `protocol-other`. |
| `multi-user` / `traffic-accounting` | Multiple user credentials / traffic or quota tracking | Explain storage and accuracy limits before choosing an accounting method. |
| `warp` | Configure WARP | Check system compatibility and routing impact first. |
| `bbr-fq` / `swap` / `udp-buffer-tuning` | BBR/fq, swap, or UDP buffer tuning | Check compatibility and system-wide effects before changes. |
| `sing-box-dashboard` | Official sing-box Dashboard (1.14.0+) | Check resources; keep it off on low-resource hosts by default. Use a strong API secret, loopback binding, and SSH tunnel. Direct public exposure needs a separate explicit request, TLS, and strict network restrictions. See the [official API documentation](https://sing-box.sagernet.org/configuration/service/api/). |
| `third-party-panel` | A third-party panel | Name the panel; check resources, installation source, and access security first. |
| `private-subscription` | Private HTTPS subscription | Keep access controlled and out of public repositories and pages. |
| `qr-code` | Client configuration QR codes | QR codes contain credentials; protect them like private client files. |
| `client-format-sing-box` / `client-format-v2rayn` | Export the additional client format | Shadowrocket and Clash Verge / Mihomo remain the defaults. |

### Screenshots and real-world validation

The image above is a workflow illustration, not a test result from a VPS. Real deployment screenshots, client connectivity evidence, and Fusion Monster output will be added after testing on an actual machine. No synthetic output is presented as real evidence.

### Scope

- For Linux VPS instances you own or are explicitly authorized to administer.
- The agent must be able to use SSH and, when needed, obtain credentials through a secure interactive prompt.
- The host must be able to reach the official sing-box package source. IPv4, IPv6, and cloud firewall behavior varies by provider and instance.
- This repository contains agent instructions, not a standalone one-click installer. No network can be guaranteed to work in every environment.

## 安全说明 / Security

仅在你拥有或明确获准管理的服务器上使用。请在提交前检查提示词、日志和生成文件，确认没有 SSH 密码、私钥、UUID、订阅链接、真实 IP 或其他凭据。客户端配置属于私密凭据，不应公开上传。发现安全问题时，请通过 GitHub 私下联系维护者，不要在公开 Issue 中发布可利用的服务器信息。

Use this only on servers you own or are authorized to administer. Before sharing logs or opening an issue, remove SSH passwords, private keys, UUIDs, subscription links, real IP addresses, and other credentials. Client profiles are secrets and must not be published. Report security issues privately through GitHub rather than posting exploitable server details in a public issue.

## License

MIT. See [LICENSE](LICENSE).

