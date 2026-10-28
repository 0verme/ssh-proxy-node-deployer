# Port profile acceptance

These are proposed acceptance scenarios for an instruction-based Agent Skill. Static tests check document contracts only; simulated conversations/state reviews check decisions without writes. Real network, client and service behavior requires a separately authorized disposable VPS or isolated VM and test-only credentials. Do not run integration cases against production. No case below is evidence that it has been executed.

| ID | Prepared scenario | Expected result | Validation |
| --- | --- | --- | --- |
| P01 | Beginner, confirmed new install, both ports free | REALITY TCP/443 and Hysteria2 UDP/443; no advanced onboarding question. | Static, simulated; isolated integration |
| P02 | Expert, new install, `none` | Both protocols use 443. | Static, simulated |
| P03 | Expert, new install, explicit `ports-high` | TCP/46690 and UDP/46691 after independent checks. | Static, simulated; isolated integration |
| P04 | New install, `ports-443` | Alias selects dual 443; it is not migration consent. | Static, simulated |
| P05 | Both port feature IDs selected | Stop and ask for a choice before writes. | Static, simulated |
| P06 | TCP/443 occupied by HTTPS | Report TCP listener and stop both protocols; preserve website. | Simulated; isolated integration |
| P07 | UDP/443 occupied by HTTP/3 | Report UDP listener and stop both protocols; preserve service. | Simulated; isolated integration |
| P08 | TCP/443 and UDP/443 occupied | Report both conflicts and stop; no automatic port change. | Simulated; isolated integration |
| P09 | Explicit high profile has one occupied port | Stop both protocols; do not choose another port. | Simulated; isolated integration |
| P10 | User cancels or does not confirm plan | No account, node, firewall, or client-file writes. | Simulated |
| P11 | Repeat run on existing high-port node | Preserve ports, client files, firewall, certificates and credentials. | Simulated; isolated integration |
| P12 | Repeat run on existing 443 node | Preserve existing state; `ports-443` does not authorize migration. | Simulated; isolated integration |
| P13 | sing-box exists but inbound ownership/state is unclear | Do not apply new-install defaults; report and pause before node changes. | Simulated |
| P14 | Generate each selected client format | Both client ports match the actual corresponding server listeners. | Simulated; manual client acceptance |
| P15 | Beginner supplies domain and confirms DNS control | Preserve existing ACME trigger and fallback; check TCP/80 and TCP/443 for respective challenges. | Static, simulated; isolated ACME integration |
| P16 | SSH TCP or authentication fails, or root-only admin verification fails | Preserve existing SSH gates and root access; do not deploy. | Existing static and simulated SSH matrix; isolated integration |
| P17 | Review Chinese and English README | Same default, conflict, alias, migration and ACME boundaries. | Static and manual review |
| P18 | No domain feature selected or implemented | Port change alone does not enable domain endpoint or self-hosted fallback. | Static and simulated |

Include IPv4/IPv6 wildcard overlap, identifiable container mappings and forwarding rules, a late port conflict before bind, and cloud firewall uncertainty in simulated and isolated tests. Test each protocol from an external client. Record any existing paths and keep a verified recovery route; never infer successful connectivity from static checks.
