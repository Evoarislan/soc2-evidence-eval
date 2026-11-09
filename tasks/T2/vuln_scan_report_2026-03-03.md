# Vulnerability Scan Report - External Perimeter

- Scanner: VulnSweep Pro (authenticated scan)
- Target scope: public-facing production hosts (14 hosts)
- Scan date: 2026-03-03
- Report generated: 2026-03-03 22:14 UTC
- Prepared for: Copperline Systems, Inc.

## Summary

| Severity | Findings |
|----------|----------|
| Critical | 0 |
| High     | 0 |
| Medium   | 3 |
| Low      | 7 |
| Info     | 12 |

## Medium findings

1. TLS 1.1 still enabled on legacy-lb-02 (informational exposure).
2. Outdated OpenSSH banner on bastion-01 (no known exploitable CVE).
3. Missing X-Content-Type-Options header on status page.

## Conclusion

No critical or high findings. All findings from the prior scan
(2026-02-24) are confirmed remediated. Medium items are tracked in
tickets SEC-2211 through SEC-2213 with a 30-day remediation target.
