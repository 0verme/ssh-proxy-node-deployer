# SSH preflight acceptance cases

These are reproducible, read-only acceptance cases for the instructions in `SKILL.md`. Use only authorized test hosts and existing test keys. Do not deploy software, change a server, start the SSH Agent, edit the user's SSH configuration, or expose key/password contents while running them.

## Windows PowerShell procedure

Set the alias to a prepared OpenSSH `Host` entry. Resolve only the endpoint used by the raw TCP check; keep the full `ssh -G` output private and do not print it:

```powershell
$sshHostAlias = "YOUR_SSH_HOST"
$sshResolvedConfig = & ssh -G $sshHostAlias
if ($LASTEXITCODE -ne 0) { throw "Could not resolve the OpenSSH Host configuration." }
$sshHostLine = $sshResolvedConfig | Where-Object { $_ -match '^hostname\s+' } | Select-Object -First 1
$sshPortLine = $sshResolvedConfig | Where-Object { $_ -match '^port\s+' } | Select-Object -First 1
if (-not $sshHostLine -or -not $sshPortLine) { throw "The resolved HostName or Port is missing." }
$sshTargetHost = $sshHostLine -replace '^hostname\s+', ''
$sshTargetPort = [int]($sshPortLine -replace '^port\s+', '')
Test-NetConnection -ComputerName $sshTargetHost -Port $sshTargetPort -InformationLevel Detailed
```

This is a raw TCP connection to the configured target `HostName` and `Port`; it does not use `ProxyJump`. If the test specifically requires TCP/22 in addition to a custom SSH port, test `22` separately. After a passing TCP result, run the authentication probe without overriding the existing Host configuration:

```powershell
ssh -o BatchMode=yes -o ConnectTimeout=10 $sshHostAlias "whoami && hostname"
$LASTEXITCODE
```

Keep the remote output and exit code; do not collect or publish key material, passwords, or the complete SSH configuration. If the test agent is not on the intended client network, have the user run the TCP probe locally.

## Acceptance matrix

| Prepared test condition | Expected result |
| --- | --- |
| Windows `ssh-agent` is stopped or disabled; configured `IdentityFile` is valid; direct TCP passes | SSH command exits 0 and returns the configured login user and host name. Continue even though the Agent is unavailable; do not start or enable it. |
| SSH Agent is running with an authorized key; direct TCP passes | SSH command exits 0 and returns the configured login user and host name. |
| The selected test key is not authorized | Report `Permission denied` as an authentication failure and stop. Do not change `IdentityFile`, add keys, or modify SSH configuration. |
| The test Host Key is unknown, changed, or mismatched | Report a Host Key verification error and stop. Do not accept it automatically, disable checking, or edit `known_hosts`. |
| The raw TCP target port times out, refuses, or is unreachable | Apply the direct-connect stop policy and report the TCP result. SSH authentication cannot override it. |
| OpenSSH Host config specifies a custom port | The raw TCP probe uses the effective configured port. Test TCP/22 separately only if requested. |
| The Host config specifies `ProxyJump` and authentication succeeds through it | The SSH authentication probe may succeed through the configured jump. The TCP probe still targets the final HostName and Port directly; report it independently and do not call the target directly reachable when that probe fails. If direct TCP reachability is a required condition, stop even though authentication succeeded through the jump. |
| The failure is not a timeout, Host Key error, or `Permission denied` | Report it as another SSH/configuration error with a concise, sanitized diagnostic, then stop. |

## 中文验收矩阵

| 测试条件 | 预期结果 |
| --- | --- |
| Windows `ssh-agent` 已停止或禁用；现有 `IdentityFile` 有效；TCP 直连通过 | SSH 命令退出码为 0，并返回配置的登录用户和主机名；Agent 不可用时仍继续，不启动或启用 Agent。 |
| SSH Agent 正在运行且包含有效密钥；TCP 直连通过 | SSH 命令退出码为 0，并返回配置的登录用户和主机名。 |
| 测试密钥未获目标主机授权 | 明确报告 `Permission denied` 认证失败并停止；不改 `IdentityFile`、不添加密钥、不修改 SSH 配置。 |
| 测试 Host Key 未知、已变化或不匹配 | 报告 Host Key 验证错误并停止；不自动接受、不关闭验证、不改 `known_hosts`。 |
| 原始 TCP 目标端口超时、拒绝连接或不可达 | 按直连安全策略停止并报告 TCP 结果；SSH 认证成功不能覆盖此结果。 |
| SSH Host 配置指定自定义端口 | 原始 TCP 探测使用配置中的有效端口；只有用户要求时才额外测试 TCP/22。 |
| SSH Host 配置使用 `ProxyJump` 且跳板认证成功 | SSH 认证可按配置使用跳板；TCP 探测仍直连最终 HostName 和 Port，单独报告，不可把失败称为目标直连成功。 |
| 其他 SSH 或配置错误 | 使用简短且脱敏的诊断归类为“其他错误”，然后停止。 |
