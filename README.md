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
- 按实际可达性判断 IPv4 / IPv6；有地址不代表从公网一定能连通。
- 有域名且你能控制 DNS 时，默认尝试申请受信任的 ACME 证书；否则用新生成的自签证书，并说明客户端验证身份的取舍。
- 默认生成 Shadowrocket 链接和 Clash Verge / Mihomo 配置，保存在仓库之外的私有目录。
- 默认保留现有 SSH 登录方式、主机防火墙策略和其他服务；不重启整台机器，不安装面板。
- **默认不下载、不运行融合怪。** 只有你明确要求测速或机器评测时才运行；完整测试可能增加 CPU、磁盘负载和流量。

高位端口只能减少部分只扫描常见端口的噪声，不能隐藏服务器 IP，也挡不住全端口扫描。请结合云厂商安全组、防火墙和账户安全设置使用。

### 安装

将仓库克隆到 Agent 能读取的 Skills 目录。以 Codex 为例：

**Windows PowerShell**

```powershell
$skills = Join-Path $HOME ".codex\skills"
New-Item -ItemType Directory -Force $skills | Out-Null
git clone https://github.com/0verme/ssh-proxy-node-deployer.git (Join-Path $skills "ssh-proxy-node-deployer")
```

**macOS / Linux**

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/0verme/ssh-proxy-node-deployer.git ~/.codex/skills/ssh-proxy-node-deployer
```

如果你的 Agent 使用不同的 Skills 目录，请把仓库放进它实际扫描的目录。重新加载或重启 Agent 后即可调用。

### 给 Agent 的提示词

把 SSH 地址、用户名和端口告诉 Agent；**密码不要粘贴到聊天里**。优先使用已经配置好的 SSH 密钥或 SSH Agent。若必须用密码，使用 Agent 提供的安全交互式终端输入。

```text
使用 ssh-proxy-node-deployer Skill，在我有权管理的 VPS 上部署自用节点。
SSH 主机：<IP 或域名>
SSH 用户：<用户名>
SSH 端口：<端口；默认 22>

先做只读检查并报告计划，再实施安全且可回滚的步骤。按默认方案使用高位端口；
保留现有 SSH 和防火墙策略。融合怪不要运行，除非我之后明确要求。
客户端配置请放在仓库外的私有目录，不要把密码或私钥写入聊天、仓库或日志。
```

如果希望先检查而不部署，可以这样说：

```text
使用 ssh-proxy-node-deployer 检查这台 VPS 是否适合部署。先只读检查并给我报告，
暂时不要安装软件、修改配置或防火墙。
```

### 可选功能

按需明确提出即可：

- 融合怪基础检查或完整评测（完整测试会产生额外负载和流量）。
- 启用 UFW / firewalld，或加固 SSH（需要先验证备用登录并准备回滚）。
- AnyTLS、TUIC、Shadowsocks 等额外协议、多个用户或流量统计。
- WARP、BBR / fq、交换空间及其他网络调优。
- 私有订阅、二维码或管理面板。

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
- Detect IPv4 and IPv6 based on actual reachability; an assigned address alone does not prove public connectivity.
- If you provide a domain and control its DNS, try to obtain a trusted ACME certificate by default. Otherwise, create a fresh self-signed certificate and explain the client identity-verification trade-off.
- Generate Shadowrocket links and a Clash Verge / Mihomo profile by default. Keep client files in a private directory outside the repository.
- Preserve existing SSH access, host firewall policy, and unrelated services. Do not reboot the VPS or install a web panel by default.
- **Fusion Monster is off by default.** Run it only when explicitly requested. A full benchmark can use CPU, disk, and network bandwidth.

High ports can reduce noise from scans limited to common ports. They do not hide the VPS IP or prevent full-range scans. Use cloud firewall rules and sound account security as well.

### Install

Clone this repository into a Skills directory scanned by your agent. For Codex:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/0verme/ssh-proxy-node-deployer.git ~/.codex/skills/ssh-proxy-node-deployer
```

On Windows, the same repository can be cloned into `%USERPROFILE%\.codex\skills\ssh-proxy-node-deployer`. If your agent uses another Skills directory, use its configured path. Reload or restart the agent to discover the Skill.

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

Ask explicitly for Fusion Monster basic checks or a full benchmark, host firewall setup, SSH hardening, extra protocols, multiple users, traffic accounting, WARP, BBR / fq, swap, a private subscription, QR codes, or a management panel. Some options add load, consume bandwidth, or need extra access safeguards.

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


