# Offline simulated acceptance matrix

These are mock scenarios for reviewing an instruction contract, not executed network or deployment tests. Addresses and names are documentation examples only. No real VPS, DNS, TLS, or installation is contacted.

| ID | Mock input / evidence | Expected agent decision |
| --- | --- | --- |
| D01 | Beginner, no domain | No advanced prompts; default dual 443 and normal deployment plan. |
| D02 | Beginner, certificate domain and DNS control | Existing Hysteria2 ACME trigger and fallback apply; no domain endpoint. |
| D03 | Expert `none`, domain supplied | No new feature; existing certificate-domain rules remain. |
| D04 | Endpoint `node.example.com`, mock A 192.0.2.10 and VPS 192.0.2.10, reachable IPv4, no AAAA | Offer domain only for authorized client protocol; no IPv6 claim or target change. |
| D05 | Endpoint A 192.0.2.11, mock VPS 192.0.2.10 | Pause endpoint; report mismatch and offer correction or cancellation. |
| D06 | Mock CNAME to CDN, mixed AAAA and A | Report proxy/ambiguity; do not assume TCP or UDP forwarding. |
| D07 | Endpoint plus nearby, mock same-ASN, valid TLS 1.3/h2 and certificate | Show evidence and candidate, wait for selection and plan confirmation. |
| D08 | Nearby, same-prefix24, mock 192.0.2.20 and VPS 192.0.2.10 | Prefix match alone is not compatibility; no subnet scan. |
| D09 | Nearby, mock ASN unavailable or no compatible TLS candidate | Report missing evidence and retain original target. |
| D10 | Nearby, candidate resolves to mock VPS address | Reject self-loop, preserve target. |
| D11 | Custom hostname, mock certificate mismatch or redirect loop | Reject and report failure; no replacement. |
| D12 | Nearby and custom both selected, or none plus feature | Stop and ask for explicit choice before writes. |
| D13 | Existing node, selected target, user cancels | No target, client, port or credential change. |
| D14 | Endpoint with ports-high | Preserve high-port selection; neither feature authorizes migration. |
| D15 | Mock five eligible candidates and one extra | Display at most five; no automatic selection. |
| D16 | Custom target accepted and plan confirmed | Validate version-specific sing-box schema and client pairing before any authorized write. |
