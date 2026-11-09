# Finding Disposition Memo - 2026 Penetration Test

- Memo ID: DM-2026-09
- Date: 2026-09-04
- From: Dana Okafor, Chief Information Security Officer
- To: GRC audit file
- Subject: Disposition of findings PT-2026-01 through PT-2026-03
  (Alder Security Partners report, issued 2026-08-14)

## PT-2026-01 (Critical, admin API authentication bypass)

Remediated. Fix deployed to production 2026-08-21; independent retest
by Alder Security Partners on 2026-08-28 confirmed closure. No further
action.

## PT-2026-02 (Medium, 12-hour session idle timeout)

I formally accept this risk in writing on behalf of Copperline Systems.
Rationale: reducing the idle timeout materially degrades a documented
long-running analyst workflow, and the compensating controls below
reduce the residual exposure to an acceptable level.

Compensating controls: (a) step-up authentication before sensitive
actions (password change, payout details, data export); (b) session
anomaly monitoring with alerting on concurrent or geographically
inconsistent sessions.

Retest and remediation review scheduled for 2026-11-30. This
acceptance expires on that date if not renewed.

## PT-2026-03 (Medium, TLS 1.1 on internal reporting endpoint)

I formally accept this risk in writing on behalf of Copperline Systems.
Rationale: the endpoint serves one legacy internal reporting client
that cannot yet negotiate TLS 1.2; replacement is planned with the Q1
2027 reporting upgrade.

Compensating controls: (a) the endpoint is reachable only from the
internal network; (b) a web application firewall rule blocks TLS 1.1
negotiation from any external source.

Retest and remediation review scheduled for 2026-11-30. This
acceptance expires on that date if not renewed.

Signed: D. Okafor, CISO, 2026-09-04
