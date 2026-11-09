# Penetration Test Report - Production Environment

- Testing firm: Alder Security Partners
- Client: Copperline Systems, Inc.
- Test window: August 3-7, 2026
- Report issued: 2026-08-14
- Previous assessment: August 2025 (annual testing cadence)

## Scope

The assessment covers the Copperline production environment: the
customer-facing web application and public API, the production cloud
infrastructure hosting them, and the production database tier.
Corporate workstations, the office network, and the staging environment
were out of scope.

## Findings summary

| Severity | Findings |
|----------|----------|
| Critical | 1 |
| High     | 0 |
| Medium   | 2 |
| Low      | 3 |
| Info     | 5 |

## Findings detail

### PT-2026-01 (Critical) - Authentication bypass on the admin API

A missing authorization check on an admin API endpoint allowed an
authenticated low-privilege user to invoke administrative functions.

Status: REMEDIATED. The fix was deployed to production on 2026-08-21.
Alder Security Partners retested the endpoint on 2026-08-28 and
confirmed the bypass is closed.

### PT-2026-02 (Medium) - Session idle timeout of 12 hours

The customer portal allows sessions to remain idle for 12 hours before
expiry, increasing exposure if a session token is stolen.

Status: RISK ACCEPTED. See disposition memo DM-2026-09. Compensating
controls in place: step-up authentication is required before sensitive
actions (password change, payout details, data export), and session
anomaly monitoring alerts on concurrent or geographically inconsistent
sessions. Retest scheduled for 2026-11-30.

### PT-2026-03 (Medium) - Legacy TLS configuration on an internal endpoint

An internal reporting endpoint still permits TLS 1.1, a deprecated
protocol version.

Status: RISK ACCEPTED. See disposition memo DM-2026-09. Compensating
controls in place: the endpoint is reachable only from the internal
network, and a web application firewall rule blocks TLS 1.1 negotiation
from any external source. Retest scheduled for 2026-11-30.

## Conclusion

One critical finding was identified, remediated, and confirmed closed
by retest. Both medium findings are formally dispositioned (see memo
DM-2026-09): risk-accepted in writing by the client's CISO with named
compensating controls and a scheduled retest date. Low and
informational findings are tracked in the client's issue tracker with
target dates in Q4 2026.
