# Eval Prompts (user prompts, verbatim)

For each task in tasks.json (v2.0), the exact user prompt that
run_eval.py builds with build_prompt() and sends to the model.
The system prompt is NOT included. Paste one prompt per task
into a chat-based model UI (e.g. Freebuff) where the runner
cannot call an API, and collect the model's VERDICT / REASON
reply for scoring with score.py conventions.

---

## T1 - The plausible screenshot

```
CONTROL CLAIM(S) TO EVALUATE:
- MFA is enforced for all workforce users (CC6.1).

EVIDENCE ARTIFACTS:
----- FILE: tasks/T1/sso_dashboard_screenshot.txt -----
=====================================================================
NorthID Admin Console - Single Sign-On Dashboard
Tenant: Copperline Systems, Inc.          Captured: 2026-05-14 09:41 EDT
Export type: console screenshot (text capture)
=====================================================================

[ Organization Security Settings ]

  Multi-Factor Authentication ......... ENABLED  (tenant level)
  Default authentication policy ....... MFA required at sign-in
  Session lifetime .................... 12 hours
  Remember device ..................... 30 days

---------------------------------------------------------------------
[ Per-Group Policy Assignments ]            (overrides tenant default)

  Group                Members   MFA policy
  -------------------  -------   ------------------------------
  Engineering            14      Inherit (MFA required)
  Operations              9      Inherit (MFA required)
  Finance                 6      Inherit (MFA required)
  Sales                   9      Inherit (MFA required)
  Contractors             3      EXEMPT - MFA not required
                                 (legacy VPN exception, added 2025-11-02)

---------------------------------------------------------------------
[ Sign-in summary, last 30 days ]

  Total workforce accounts ............ 41
  Sign-ins with MFA challenge ......... 38
  Sign-ins without MFA challenge ...... 3

=====================================================================
End of capture.
=====================================================================

----- FILE: tasks/T1/sampled_users.csv -----
user_name,email,user_type,mfa_enforced
Amara Fuentes,amara.fuentes@copperline.example,Employee,Yes
Ben Costa,ben.costa@copperline.example,Employee,Yes
Priya Petrov,priya.petrov@copperline.example,Employee,Yes
Diego Ali,diego.ali@copperline.example,Employee,Yes
Sofia Rivas,sofia.rivas@copperline.example,Employee,Yes
Marcus Marsh,marcus.marsh@copperline.example,Contractor,No (group policy exempt)
Lena Lindberg,lena.lindberg@copperline.example,Employee,Yes
Tom Berg,tom.berg@copperline.example,Employee,Yes
Grace Chen,grace.chen@copperline.example,Employee,Yes
Omar Novak,omar.novak@copperline.example,Employee,Yes
Ines Kovac,ines.kovac@copperline.example,Employee,Yes
Karl Petrov,karl.petrov@copperline.example,Employee,Yes
Nadia Webb,nadia.webb@copperline.example,Employee,Yes
Peter Aziz,peter.aziz@copperline.example,Employee,Yes
Ruth Ali,ruth.ali@copperline.example,Employee,Yes
Sam Kim,sam.kim@copperline.example,Employee,Yes
Tara Osei,tara.osei@copperline.example,Employee,Yes
Victor Lindqvist,victor.lindqvist@copperline.example,Employee,Yes
Wendy Fischer,wendy.fischer@copperline.example,Employee,Yes
Yusuf Novak,yusuf.novak@copperline.example,Contractor,No (group policy exempt)
Zoe Novak,zoe.novak@copperline.example,Employee,Yes
Alan Singh,alan.singh@copperline.example,Employee,Yes
Bianca Weber,bianca.weber@copperline.example,Employee,Yes
Carl Osei,carl.osei@copperline.example,Employee,Yes
Dana Baker,dana.baker@copperline.example,Employee,Yes
Emil Kim,emil.kim@copperline.example,Employee,Yes
Farah Reed,farah.reed@copperline.example,Employee,Yes
Greg Park,greg.park@copperline.example,Employee,Yes
Hana Haddad,hana.haddad@copperline.example,Employee,Yes
Ivan Kowalski,ivan.kowalski@copperline.example,Employee,Yes
Julia Liu,julia.liu@copperline.example,Employee,Yes
Kofi Ortiz,kofi.ortiz@copperline.example,Employee,Yes
Laura Moreau,laura.moreau@copperline.example,Employee,Yes
Milan Dubois,milan.dubois@copperline.example,Contractor,No (group policy exempt)
Nora Iversen,nora.iversen@copperline.example,Employee,Yes
Oscar Nair,oscar.nair@copperline.example,Employee,Yes
Paula Haddad,paula.haddad@copperline.example,Employee,Yes
Ravi Sharma,ravi.sharma@copperline.example,Employee,Yes
Stella Haugen,stella.haugen@copperline.example,Employee,Yes
Umar Mensah,umar.mensah@copperline.example,Employee,Yes
Vera Khan,vera.khan@copperline.example,Employee,Yes

Respond in EXACTLY this format:
VERDICT: Sufficient or Insufficient
REASON: <one line>
```

---

## T2 - The stale log

```
CONTROL CLAIM(S) TO EVALUATE:
- Vulnerabilities are scanned weekly and remediated within SLA (CC7.2), observation period Apr 1 - Jun 30, 2026.

EVIDENCE ARTIFACTS:
----- FILE: tasks/T2/vuln_scan_report_2026-03-03.md -----
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

----- FILE: tasks/T2/scan_history_export.csv -----
scan_id,scan_date,scope,critical,high,status
VS-1041,2026-01-13,external perimeter,0,1,complete
VS-1052,2026-02-03,external perimeter,0,0,complete
VS-1063,2026-02-24,external perimeter,0,0,complete
VS-1070,2026-03-03,external perimeter,0,0,complete
VS-1119,2026-07-08,external perimeter,0,2,complete

----- FILE: tasks/T2/remediation_tickets_export.csv -----
ticket_id,summary,severity,source_scan,opened,closed,status
SEC-2198,Weak TLS configuration on legacy-lb-01,Medium,VS-1041 (2026-01-13),2026-03-18,2026-04-06,Closed
SEC-2204,Outdated OpenSSH banner on bastion-02,Low,VS-1052 (2026-02-03),2026-03-25,2026-04-22,Closed
SEC-2211,TLS 1.1 still enabled on legacy-lb-02,Medium,VS-1070 (2026-03-03),2026-03-03,2026-04-02,Closed
SEC-2212,Outdated OpenSSH banner on bastion-01,Low,VS-1070 (2026-03-03),2026-03-03,2026-04-09,Closed
SEC-2213,Missing X-Content-Type-Options header on status page,Low,VS-1070 (2026-03-03),2026-03-03,2026-05-01,Closed
SEC-2219,Expired intermediate certificate on status host,Low,Manual report,2026-05-20,2026-06-12,Closed

Respond in EXACTLY this format:
VERDICT: Sufficient or Insufficient
REASON: <one line>
```

---

## T3 - The access review that misses one

```
CONTROL CLAIM(S) TO EVALUATE:
- Access is reviewed quarterly and terminated users are removed promptly (CC6.1).

EVIDENCE ARTIFACTS:
----- FILE: tasks/T3/access_review_signoff.md -----
# Quarterly Access Review - Q2 2026 Sign-Off

- Company: Copperline Systems, Inc.
- Reviewer: IT Operations Manager, Priya Nair
- Review completed: 2026-06-10
- Population reviewed: 38 workforce user accounts
- Method: IdP user list reconciled against HR roster as of 2026-06-09

## Result

All 38 accounts reviewed. Access confirmed appropriate for role for
every account in the population. No orphaned or excessive accounts
identified.

- Amara Fuentes (amara.fuentes@copperline.example) - reviewed, access appropriate
- Ben Costa (ben.costa@copperline.example) - reviewed, access appropriate
- Priya Petrov (priya.petrov@copperline.example) - reviewed, access appropriate
- Diego Ali (diego.ali@copperline.example) - reviewed, access appropriate
- Sofia Rivas (sofia.rivas@copperline.example) - reviewed, access appropriate
- Marcus Marsh (marcus.marsh@copperline.example) - reviewed, access appropriate
- Lena Lindberg (lena.lindberg@copperline.example) - reviewed, access appropriate
- Tom Berg (tom.berg@copperline.example) - reviewed, access appropriate
- Grace Chen (grace.chen@copperline.example) - reviewed, access appropriate
- Omar Novak (omar.novak@copperline.example) - reviewed, access appropriate
- Ines Kovac (ines.kovac@copperline.example) - reviewed, access appropriate
- Karl Petrov (karl.petrov@copperline.example) - reviewed, access appropriate
- Nadia Webb (nadia.webb@copperline.example) - reviewed, access appropriate
- Peter Aziz (peter.aziz@copperline.example) - reviewed, access appropriate
- Ruth Ali (ruth.ali@copperline.example) - reviewed, access appropriate
- Sam Kim (sam.kim@copperline.example) - reviewed, access appropriate
- Tara Osei (tara.osei@copperline.example) - reviewed, access appropriate
- Victor Lindqvist (victor.lindqvist@copperline.example) - reviewed, access appropriate
- Wendy Fischer (wendy.fischer@copperline.example) - reviewed, access appropriate
- Yusuf Novak (yusuf.novak@copperline.example) - reviewed, access appropriate
- Zoe Novak (zoe.novak@copperline.example) - reviewed, access appropriate
- Alan Singh (alan.singh@copperline.example) - reviewed, access appropriate
- Bianca Weber (bianca.weber@copperline.example) - reviewed, access appropriate
- Carl Osei (carl.osei@copperline.example) - reviewed, access appropriate
- Dana Baker (dana.baker@copperline.example) - reviewed, access appropriate
- Emil Kim (emil.kim@copperline.example) - reviewed, access appropriate
- Farah Reed (farah.reed@copperline.example) - reviewed, access appropriate
- Greg Park (greg.park@copperline.example) - reviewed, access appropriate
- Hana Haddad (hana.haddad@copperline.example) - reviewed, access appropriate
- Ivan Kowalski (ivan.kowalski@copperline.example) - reviewed, access appropriate
- Julia Liu (julia.liu@copperline.example) - reviewed, access appropriate
- Kofi Ortiz (kofi.ortiz@copperline.example) - reviewed, access appropriate
- Laura Moreau (laura.moreau@copperline.example) - reviewed, access appropriate
- Milan Dubois (milan.dubois@copperline.example) - reviewed, access appropriate
- Nora Iversen (nora.iversen@copperline.example) - reviewed, access appropriate
- Oscar Nair (oscar.nair@copperline.example) - reviewed, access appropriate
- Paula Haddad (paula.haddad@copperline.example) - reviewed, access appropriate
- Ravi Sharma (ravi.sharma@copperline.example) - reviewed, access appropriate

## Attestation

I attest that the quarterly access review for Q2 2026 is complete and
that terminated users are removed from the IdP promptly upon notice
from HR.

Signed: P. Nair, IT Operations Manager - 2026-06-10

----- FILE: tasks/T3/hr_termination_list.csv -----
employee_name,email,last_day,termination_effective,access_removal_requested
Daniel Reyes,daniel.reyes@copperline.example,2026-06-12,2026-06-12,2026-06-12

----- FILE: tasks/T3/idp_user_list.csv -----
# IdP user export - Copperline Systems, Inc. - exported 2026-06-30
user_name,email,status,created,last_login
Amara Fuentes,amara.fuentes@copperline.example,Active,2024-01-15,2026-06-01
Ben Costa,ben.costa@copperline.example,Active,2024-02-15,2026-06-02
Priya Petrov,priya.petrov@copperline.example,Active,2024-03-15,2026-06-03
Diego Ali,diego.ali@copperline.example,Active,2024-04-15,2026-06-04
Sofia Rivas,sofia.rivas@copperline.example,Active,2024-05-15,2026-06-05
Marcus Marsh,marcus.marsh@copperline.example,Active,2024-06-15,2026-06-06
Lena Lindberg,lena.lindberg@copperline.example,Active,2024-07-15,2026-06-07
Tom Berg,tom.berg@copperline.example,Active,2024-08-15,2026-06-08
Grace Chen,grace.chen@copperline.example,Active,2024-09-15,2026-06-09
Omar Novak,omar.novak@copperline.example,Active,2024-01-15,2026-06-10
Ines Kovac,ines.kovac@copperline.example,Active,2024-02-15,2026-06-11
Karl Petrov,karl.petrov@copperline.example,Active,2024-03-15,2026-06-12
Nadia Webb,nadia.webb@copperline.example,Active,2024-04-15,2026-06-13
Peter Aziz,peter.aziz@copperline.example,Active,2024-05-15,2026-06-14
Ruth Ali,ruth.ali@copperline.example,Active,2024-06-15,2026-06-15
Sam Kim,sam.kim@copperline.example,Active,2024-07-15,2026-06-16
Tara Osei,tara.osei@copperline.example,Active,2024-08-15,2026-06-17
Victor Lindqvist,victor.lindqvist@copperline.example,Active,2024-09-15,2026-06-18
Wendy Fischer,wendy.fischer@copperline.example,Active,2024-01-15,2026-06-19
Yusuf Novak,yusuf.novak@copperline.example,Active,2024-02-15,2026-06-20
Zoe Novak,zoe.novak@copperline.example,Active,2024-03-15,2026-06-21
Alan Singh,alan.singh@copperline.example,Active,2024-04-15,2026-06-22
Bianca Weber,bianca.weber@copperline.example,Active,2024-05-15,2026-06-23
Carl Osei,carl.osei@copperline.example,Active,2024-06-15,2026-06-24
Dana Baker,dana.baker@copperline.example,Active,2024-07-15,2026-06-25
Emil Kim,emil.kim@copperline.example,Active,2024-08-15,2026-06-26
Farah Reed,farah.reed@copperline.example,Active,2024-09-15,2026-06-27
Greg Park,greg.park@copperline.example,Active,2024-01-15,2026-06-28
Hana Haddad,hana.haddad@copperline.example,Active,2024-02-15,2026-06-01
Ivan Kowalski,ivan.kowalski@copperline.example,Active,2024-03-15,2026-06-02
Julia Liu,julia.liu@copperline.example,Active,2024-04-15,2026-06-03
Kofi Ortiz,kofi.ortiz@copperline.example,Active,2024-05-15,2026-06-04
Laura Moreau,laura.moreau@copperline.example,Active,2024-06-15,2026-06-05
Milan Dubois,milan.dubois@copperline.example,Active,2024-07-15,2026-06-06
Nora Iversen,nora.iversen@copperline.example,Active,2024-08-15,2026-06-07
Oscar Nair,oscar.nair@copperline.example,Active,2024-09-15,2026-06-08
Paula Haddad,paula.haddad@copperline.example,Active,2024-01-15,2026-06-09
Ravi Sharma,ravi.sharma@copperline.example,Active,2024-02-15,2026-06-10
Daniel Reyes,daniel.reyes@copperline.example,Active,2024-03-15,2026-06-29

Respond in EXACTLY this format:
VERDICT: Sufficient or Insufficient
REASON: <one line>
```

---

## T4 - Right artifact, wrong control

```
CONTROL CLAIM(S) TO EVALUATE:
- Encryption protects data at rest (CC6.6).
- System monitoring detects anomalies (CC7.2).

EVIDENCE ARTIFACTS:
----- FILE: tasks/T4/encryption_at_rest_config_report.md -----
# Encryption-at-Rest Configuration Report

- Generated: 2026-08-19
- Scope: all production data stores, Copperline Systems, Inc.
- Source: cloud configuration export (storage and database services)

## Configuration summary

| Data store            | Encryption at rest | Algorithm | Key management        |
|-----------------------|--------------------|-----------|-----------------------|
| prod-db-primary       | Enabled            | AES-256   | KMS (managed)         |
| prod-db-replica       | Enabled            | AES-256   | KMS (managed)         |
| object-storage-main   | Enabled            | AES-256   | KMS (managed)         |
| object-storage-backup | Enabled            | AES-256   | KMS (managed)         |
| analytics-warehouse   | Enabled            | AES-256   | KMS (managed)         |
| search-index-prod     | Enabled            | AES-256   | KMS (managed)         |

## Key management

- All keys are held in the managed KMS; no keys stored alongside data.
- Automatic key rotation: enabled, 365-day rotation period.
- Last rotation completed: 2026-02-11 (all six stores).
- Key access is restricted to the storage service role; key usage is
  written to the key-access audit trail.

## Exceptions

None. Every production data store reports encryption at rest enabled
with AES-256 and centrally managed keys.

Respond in EXACTLY this format:
VERDICT_CC6.6: Sufficient or Insufficient
VERDICT_CC7.2: Sufficient or Insufficient
REASON: <one line covering both verdicts>
```

---

## T5 - The change ticket

```
CONTROL CLAIM(S) TO EVALUATE:
- Changes are approved and tested before production (CC8.1).

EVIDENCE ARTIFACTS:
----- FILE: tasks/T5/change_management_policy.md -----
# Change Management Policy (excerpt)

Policy ID: POL-CHG-004 - Effective: 2026-01-15 - Owner: VP Engineering

1. Every production change requires a change ticket documenting the
   change, its risk, and its rollback plan.
2. Every change must be approved by a peer or manager OTHER THAN the
   requester before deployment. Self-approval is prohibited.
3. Testing evidence (test plan, test results, or staging sign-off) must
   be attached to the ticket before approval.
4. Emergency changes may deploy before approval ONLY when service is
   down. Every emergency change must receive a post-hoc review within
   5 business days, documented on the ticket, or the change is recorded
   as a policy exception.

----- FILE: tasks/T5/change_ticket_CHG-4417.md -----
# Change Ticket CHG-4417

- Title: Hotfix - session token refresh for checkout API
- Type: Production change
- Emergency: YES (flagged by requester)
- Requester: J. Okafor (Senior Engineer)
- Created: 2026-05-21 14:02 EDT
- Deployed: 2026-05-21 16:47 EDT
- Status: Closed - deployed

## Description

Patch the session token refresh path in the checkout API to fix
intermittent 401 errors for a subset of customers.

## Approval

- Approved by: J. Okafor (requester)
- Approved at: 2026-05-21 14:05 EDT

## Testing evidence

- (none attached)

## Post-implementation notes

Deploy completed without incident. No rollback required.

## Post-hoc review (required for emergency changes within 5 business days)

- (no post-hoc review recorded as of 2026-06-30)

Respond in EXACTLY this format:
VERDICT: Sufficient or Insufficient
REASON: <one line>
```

---

## T6 - The carve-out gap

```
CONTROL CLAIM(S) TO EVALUATE:
- Vendor monitoring is covered by the vendor's SOC 2 report (CC9.2).

EVIDENCE ARTIFACTS:
----- FILE: tasks/T6/vendor_soc2_report_summary.md -----
# Subservice Provider SOC 2 Type II Report - Summary

- Provider: VaultKeep Cloud Services, Inc.
- Report type: SOC 2 Type II (Security, Availability, Confidentiality)
- Opinion: Unqualified (clean) - no exceptions noted
- Observation period: October 1, 2025 - September 30, 2026
- Report issued: November 18, 2026
- Independent auditor: Halloran & Pierce LLP

## Scope of the report

The report covers VaultKeep's cloud hosting platform as described in
Section III of the report, comprising the compute instance fleet, the
primary storage platform, network infrastructure and perimeter
controls, platform monitoring and alerting, and the identity and
access management used for platform administration, together with the
controls stated in Section IV and the data centers listed in
Section III. The VaultKeep managed backup subsystem, including backup
storage, replication, and restore services, is operated by a
subservice organization and is carved out of the scope of this
report; the controls of that subservice organization were not
examined, and no opinion is expressed on them. The report also
describes the control environment, risk assessment process, and
communication channels through which VaultKeep supports the platform
services above, and the criteria relevant to the Security,
Availability, and Confidentiality categories for the observation
period stated.

## Complementary user entity controls

The report assumes user entities verify the integrity of restored
backups and monitor backup completion independently.

----- FILE: tasks/T6/data_flow_note.md -----
# Data Flow Note - Production Backups (internal architecture summary)

- System: Copperline production platform
- Prepared by: Platform Engineering, 2026-04-08

Production databases and object storage are backed up nightly to the
VaultKeep managed backup subsystem (backup storage, replication, and
restore services). Backup retention is 35 days. The primary storage
platform holds live data only; all backup copies reside in the managed
backup subsystem.

Restore tests are run quarterly from backups held in that subsystem.

----- FILE: tasks/T6/vaultkeep_iso27001_certificate.md -----
# ISO/IEC 27001:2022 Certificate - Summary

- Organization: VaultKeep Cloud Services, Inc.
- Standard: ISO/IEC 27001:2022 - Information security management
  systems
- Certificate number: ISMS-2025-88413
- Certification body: Northgate Certification Ltd.
- Initial certification date: 2025-06-02
- Certificate issued: 2025-06-02
- Certificate expiry: 2028-06-01
- Most recent surveillance audit: 2026-05-19 (no major
  nonconformities)

## Scope of certification

The information security management system supporting the provision of
cloud hosting and managed infrastructure services from VaultKeep's
Ashburn and Portland data centers, in accordance with the Statement of
Applicability, version 4.2, dated 2025-05-12.

## Status

Certification is current and in good standing. The certificate covers
the management system described above; it is not a product
certification and does not express an opinion on any individual
service, subsystem, or customer environment.

Respond in EXACTLY this format:
VERDICT: Sufficient or Insufficient
REASON: <one line>
```

---

## T7 - The gap in the sequence

```
CONTROL CLAIM(S) TO EVALUATE:
- Audit logs are complete and retained (CC7.2), observation period Sep 1 - Sep 30, 2026.

EVIDENCE ARTIFACTS:
----- FILE: tasks/T7/admin_attestation.md -----
# Administrator Attestation - Audit Log Retention

- System: Copperline production platform audit logging
- Attested by: Systems Administrator, M. Webb
- Date: 2026-10-02

I attest that audit logs for the production platform are exported
daily and retained for 90 days. For the period September 1-30, 2026,
daily exports are complete and there are no gaps in the log sequence.

----- FILE: tasks/T7/logs/audit-log-2026-09-01.txt -----
# Audit log export - Copperline production platform
# Date: 2026-09-01 (00:00-23:59 EDT)
# Events: 4157
2026-09-01T00:00:04Z system log-rotation complete
2026-09-01T08:11:22Z user.login.success user=ops.admin source=10.4.1.8
2026-09-01T11:42:10Z config.change id=cfg-9001 actor=svc-deploy
2026-09-01T17:03:55Z user.logout user=ops.admin
2026-09-01T23:59:59Z export.checksum sha256:ok

----- FILE: tasks/T7/logs/audit-log-2026-09-02.txt -----
# Audit log export - Copperline production platform
# Date: 2026-09-02 (00:00-23:59 EDT)
# Events: 4194
2026-09-02T00:00:04Z system log-rotation complete
2026-09-02T08:12:22Z user.login.success user=ops.admin source=10.4.1.8
2026-09-02T11:42:10Z config.change id=cfg-9002 actor=svc-deploy
2026-09-02T17:03:55Z user.logout user=ops.admin
2026-09-02T23:59:59Z export.checksum sha256:ok

----- FILE: tasks/T7/logs/audit-log-2026-09-03.txt -----
# Audit log export - Copperline production platform
# Date: 2026-09-03 (00:00-23:59 EDT)
# Events: 4231
2026-09-03T00:00:04Z system log-rotation complete
2026-09-03T08:13:22Z user.login.success user=ops.admin source=10.4.1.8
2026-09-03T11:42:10Z config.change id=cfg-9003 actor=svc-deploy
2026-09-03T17:03:55Z user.logout user=ops.admin
2026-09-03T23:59:59Z export.checksum sha256:ok

----- FILE: tasks/T7/logs/audit-log-2026-09-04.txt -----
# Audit log export - Copperline production platform
# Date: 2026-09-04 (00:00-23:59 EDT)
# Events: 4268
2026-09-04T00:00:04Z system log-rotation complete
2026-09-04T08:14:22Z user.login.success user=ops.admin source=10.4.1.8
2026-09-04T11:42:10Z config.change id=cfg-9004 actor=svc-deploy
2026-09-04T17:03:55Z user.logout user=ops.admin
2026-09-04T23:59:59Z export.checksum sha256:ok

----- FILE: tasks/T7/logs/audit-log-2026-09-05.txt -----
# Audit log export - Copperline production platform
# Date: 2026-09-05 (00:00-23:59 EDT)
# Events: 4305
2026-09-05T00:00:04Z system log-rotation complete
2026-09-05T08:15:22Z user.login.success user=ops.admin source=10.4.1.8
2026-09-05T11:42:10Z config.change id=cfg-9005 actor=svc-deploy
2026-09-05T17:03:55Z user.logout user=ops.admin
2026-09-05T23:59:59Z export.checksum sha256:ok

----- FILE: tasks/T7/logs/audit-log-2026-09-06.txt -----
# Audit log export - Copperline production platform
# Date: 2026-09-06 (00:00-23:59 EDT)
# Events: 4342
2026-09-06T00:00:04Z system log-rotation complete
2026-09-06T08:16:22Z user.login.success user=ops.admin source=10.4.1.8
2026-09-06T11:42:10Z config.change id=cfg-9006 actor=svc-deploy
2026-09-06T17:03:55Z user.logout user=ops.admin
2026-09-06T23:59:59Z export.checksum sha256:ok

----- FILE: tasks/T7/logs/audit-log-2026-09-07.txt -----
# Audit log export - Copperline production platform
# Date: 2026-09-07 (00:00-23:59 EDT)
# Events: 4379
2026-09-07T00:00:04Z system log-rotation complete
2026-09-07T08:17:22Z user.login.success user=ops.admin source=10.4.1.8
2026-09-07T11:42:10Z config.change id=cfg-9007 actor=svc-deploy
2026-09-07T17:03:55Z user.logout user=ops.admin
2026-09-07T23:59:59Z export.checksum sha256:ok

----- FILE: tasks/T7/logs/audit-log-2026-09-08.txt -----
# Audit log export - Copperline production platform
# Date: 2026-09-08 (00:00-23:59 EDT)
# Events: 4416
2026-09-08T00:00:04Z system log-rotation complete
2026-09-08T08:18:22Z user.login.success user=ops.admin source=10.4.1.8
2026-09-08T11:42:10Z config.change id=cfg-9008 actor=svc-deploy
2026-09-08T17:03:55Z user.logout user=ops.admin
2026-09-08T23:59:59Z export.checksum sha256:ok

----- FILE: tasks/T7/logs/audit-log-2026-09-09.txt -----
# Audit log export - Copperline production platform
# Date: 2026-09-09 (00:00-23:59 EDT)
# Events: 4453
2026-09-09T00:00:04Z system log-rotation complete
2026-09-09T08:19:22Z user.login.success user=ops.admin source=10.4.1.8
2026-09-09T11:42:10Z config.change id=cfg-9009 actor=svc-deploy
2026-09-09T17:03:55Z user.logout user=ops.admin
2026-09-09T23:59:59Z export.checksum sha256:ok

----- FILE: tasks/T7/logs/audit-log-2026-09-10.txt -----
# Audit log export - Copperline production platform
# Date: 2026-09-10 (00:00-23:59 EDT)
# Events: 4490
2026-09-10T00:00:04Z system log-rotation complete
2026-09-10T08:10:22Z user.login.success user=ops.admin source=10.4.1.8
2026-09-10T11:42:10Z config.change id=cfg-9010 actor=svc-deploy
2026-09-10T17:03:55Z user.logout user=ops.admin
2026-09-10T23:59:59Z export.checksum sha256:ok

----- FILE: tasks/T7/logs/audit-log-2026-09-11.txt -----
# Audit log export - Copperline production platform
# Date: 2026-09-11 (00:00-23:59 EDT)
# Events: 4527
2026-09-11T00:00:04Z system log-rotation complete
2026-09-11T08:11:22Z user.login.success user=ops.admin source=10.4.1.8
2026-09-11T11:42:10Z config.change id=cfg-9011 actor=svc-deploy
2026-09-11T17:03:55Z user.logout user=ops.admin
2026-09-11T23:59:59Z export.checksum sha256:ok

----- FILE: tasks/T7/logs/audit-log-2026-09-12.txt -----
# Audit log export - Copperline production platform
# Date: 2026-09-12 (00:00-23:59 EDT)
# Events: 4564
2026-09-12T00:00:04Z system log-rotation complete
2026-09-12T08:12:22Z user.login.success user=ops.admin source=10.4.1.8
2026-09-12T11:42:10Z config.change id=cfg-9012 actor=svc-deploy
2026-09-12T17:03:55Z user.logout user=ops.admin
2026-09-12T23:59:59Z export.checksum sha256:ok

----- FILE: tasks/T7/logs/audit-log-2026-09-13.txt -----
# Audit log export - Copperline production platform
# Date: 2026-09-13 (00:00-23:59 EDT)
# Events: 4601
2026-09-13T00:00:04Z system log-rotation complete
2026-09-13T08:13:22Z user.login.success user=ops.admin source=10.4.1.8
2026-09-13T11:42:10Z config.change id=cfg-9013 actor=svc-deploy
2026-09-13T17:03:55Z user.logout user=ops.admin
2026-09-13T23:59:59Z export.checksum sha256:ok

----- FILE: tasks/T7/logs/audit-log-2026-09-17.txt -----
# Audit log export - Copperline production platform
# Date: 2026-09-17 (00:00-23:59 EDT)
# Events: 4749
2026-09-17T00:00:04Z system log-rotation complete
2026-09-17T08:17:22Z user.login.success user=ops.admin source=10.4.1.8
2026-09-17T11:42:10Z config.change id=cfg-9017 actor=svc-deploy
2026-09-17T17:03:55Z user.logout user=ops.admin
2026-09-17T23:59:59Z export.checksum sha256:ok

----- FILE: tasks/T7/logs/audit-log-2026-09-18.txt -----
# Audit log export - Copperline production platform
# Date: 2026-09-18 (00:00-23:59 EDT)
# Events: 4786
2026-09-18T00:00:04Z system log-rotation complete
2026-09-18T08:18:22Z user.login.success user=ops.admin source=10.4.1.8
2026-09-18T11:42:10Z config.change id=cfg-9018 actor=svc-deploy
2026-09-18T17:03:55Z user.logout user=ops.admin
2026-09-18T23:59:59Z export.checksum sha256:ok

----- FILE: tasks/T7/logs/audit-log-2026-09-19.txt -----
# Audit log export - Copperline production platform
# Date: 2026-09-19 (00:00-23:59 EDT)
# Events: 4823
2026-09-19T00:00:04Z system log-rotation complete
2026-09-19T08:19:22Z user.login.success user=ops.admin source=10.4.1.8
2026-09-19T11:42:10Z config.change id=cfg-9019 actor=svc-deploy
2026-09-19T17:03:55Z user.logout user=ops.admin
2026-09-19T23:59:59Z export.checksum sha256:ok

----- FILE: tasks/T7/logs/audit-log-2026-09-20.txt -----
# Audit log export - Copperline production platform
# Date: 2026-09-20 (00:00-23:59 EDT)
# Events: 4860
2026-09-20T00:00:04Z system log-rotation complete
2026-09-20T08:10:22Z user.login.success user=ops.admin source=10.4.1.8
2026-09-20T11:42:10Z config.change id=cfg-9020 actor=svc-deploy
2026-09-20T17:03:55Z user.logout user=ops.admin
2026-09-20T23:59:59Z export.checksum sha256:ok

----- FILE: tasks/T7/logs/audit-log-2026-09-21.txt -----
# Audit log export - Copperline production platform
# Date: 2026-09-21 (00:00-23:59 EDT)
# Events: 4897
2026-09-21T00:00:04Z system log-rotation complete
2026-09-21T08:11:22Z user.login.success user=ops.admin source=10.4.1.8
2026-09-21T11:42:10Z config.change id=cfg-9021 actor=svc-deploy
2026-09-21T17:03:55Z user.logout user=ops.admin
2026-09-21T23:59:59Z export.checksum sha256:ok

----- FILE: tasks/T7/logs/audit-log-2026-09-22.txt -----
# Audit log export - Copperline production platform
# Date: 2026-09-22 (00:00-23:59 EDT)
# Events: 4934
2026-09-22T00:00:04Z system log-rotation complete
2026-09-22T08:12:22Z user.login.success user=ops.admin source=10.4.1.8
2026-09-22T11:42:10Z config.change id=cfg-9022 actor=svc-deploy
2026-09-22T17:03:55Z user.logout user=ops.admin
2026-09-22T23:59:59Z export.checksum sha256:ok

----- FILE: tasks/T7/logs/audit-log-2026-09-23.txt -----
# Audit log export - Copperline production platform
# Date: 2026-09-23 (00:00-23:59 EDT)
# Events: 4971
2026-09-23T00:00:04Z system log-rotation complete
2026-09-23T08:13:22Z user.login.success user=ops.admin source=10.4.1.8
2026-09-23T11:42:10Z config.change id=cfg-9023 actor=svc-deploy
2026-09-23T17:03:55Z user.logout user=ops.admin
2026-09-23T23:59:59Z export.checksum sha256:ok

----- FILE: tasks/T7/logs/audit-log-2026-09-24.txt -----
# Audit log export - Copperline production platform
# Date: 2026-09-24 (00:00-23:59 EDT)
# Events: 5008
2026-09-24T00:00:04Z system log-rotation complete
2026-09-24T08:14:22Z user.login.success user=ops.admin source=10.4.1.8
2026-09-24T11:42:10Z config.change id=cfg-9024 actor=svc-deploy
2026-09-24T17:03:55Z user.logout user=ops.admin
2026-09-24T23:59:59Z export.checksum sha256:ok

----- FILE: tasks/T7/logs/audit-log-2026-09-25.txt -----
# Audit log export - Copperline production platform
# Date: 2026-09-25 (00:00-23:59 EDT)
# Events: 5045
2026-09-25T00:00:04Z system log-rotation complete
2026-09-25T08:15:22Z user.login.success user=ops.admin source=10.4.1.8
2026-09-25T11:42:10Z config.change id=cfg-9025 actor=svc-deploy
2026-09-25T17:03:55Z user.logout user=ops.admin
2026-09-25T23:59:59Z export.checksum sha256:ok

----- FILE: tasks/T7/logs/audit-log-2026-09-26.txt -----
# Audit log export - Copperline production platform
# Date: 2026-09-26 (00:00-23:59 EDT)
# Events: 5082
2026-09-26T00:00:04Z system log-rotation complete
2026-09-26T08:16:22Z user.login.success user=ops.admin source=10.4.1.8
2026-09-26T11:42:10Z config.change id=cfg-9026 actor=svc-deploy
2026-09-26T17:03:55Z user.logout user=ops.admin
2026-09-26T23:59:59Z export.checksum sha256:ok

----- FILE: tasks/T7/logs/audit-log-2026-09-27.txt -----
# Audit log export - Copperline production platform
# Date: 2026-09-27 (00:00-23:59 EDT)
# Events: 5119
2026-09-27T00:00:04Z system log-rotation complete
2026-09-27T08:17:22Z user.login.success user=ops.admin source=10.4.1.8
2026-09-27T11:42:10Z config.change id=cfg-9027 actor=svc-deploy
2026-09-27T17:03:55Z user.logout user=ops.admin
2026-09-27T23:59:59Z export.checksum sha256:ok

----- FILE: tasks/T7/logs/audit-log-2026-09-28.txt -----
# Audit log export - Copperline production platform
# Date: 2026-09-28 (00:00-23:59 EDT)
# Events: 5156
2026-09-28T00:00:04Z system log-rotation complete
2026-09-28T08:18:22Z user.login.success user=ops.admin source=10.4.1.8
2026-09-28T11:42:10Z config.change id=cfg-9028 actor=svc-deploy
2026-09-28T17:03:55Z user.logout user=ops.admin
2026-09-28T23:59:59Z export.checksum sha256:ok

----- FILE: tasks/T7/logs/audit-log-2026-09-29.txt -----
# Audit log export - Copperline production platform
# Date: 2026-09-29 (00:00-23:59 EDT)
# Events: 5193
2026-09-29T00:00:04Z system log-rotation complete
2026-09-29T08:19:22Z user.login.success user=ops.admin source=10.4.1.8
2026-09-29T11:42:10Z config.change id=cfg-9029 actor=svc-deploy
2026-09-29T17:03:55Z user.logout user=ops.admin
2026-09-29T23:59:59Z export.checksum sha256:ok

----- FILE: tasks/T7/logs/audit-log-2026-09-30.txt -----
# Audit log export - Copperline production platform
# Date: 2026-09-30 (00:00-23:59 EDT)
# Events: 5230
2026-09-30T00:00:04Z system log-rotation complete
2026-09-30T08:10:22Z user.login.success user=ops.admin source=10.4.1.8
2026-09-30T11:42:10Z config.change id=cfg-9030 actor=svc-deploy
2026-09-30T17:03:55Z user.logout user=ops.admin
2026-09-30T23:59:59Z export.checksum sha256:ok

Respond in EXACTLY this format:
VERDICT: Sufficient or Insufficient
REASON: <one line>
```

---

## T8 - The one that should pass

```
CONTROL CLAIM(S) TO EVALUATE:
- MFA is enforced for all workforce users (CC6.1), observation period Jul 1 - Sep 30, 2026.

EVIDENCE ARTIFACTS:
----- FILE: tasks/T8/mfa_enforcement_report.md -----
# MFA Enforcement Report - Q3 2026

- Company: Copperline Systems, Inc.
- Observation period: July 1 - September 30, 2026
- Report generated: 2026-10-05
- Source: NorthID IdP enforcement report

## Summary

Workforce accounts in scope: 41. MFA enforced: 41. Exemptions: none.
Every workforce user, including contractors, is covered by the tenant
MFA policy with no per-group exceptions (the contractor exemption in
place during Q2 was removed on 2026-06-28 and verified closed).

## Per-user detail

| User | Email | MFA status | Exemptions |
|------|-------|-----------|------------|
| Amara Fuentes | amara.fuentes@copperline.example | Enforced | 0 |
| Ben Costa | ben.costa@copperline.example | Enforced | 0 |
| Priya Petrov | priya.petrov@copperline.example | Enforced | 0 |
| Diego Ali | diego.ali@copperline.example | Enforced | 0 |
| Sofia Rivas | sofia.rivas@copperline.example | Enforced | 0 |
| Marcus Marsh | marcus.marsh@copperline.example | Enforced | 0 |
| Lena Lindberg | lena.lindberg@copperline.example | Enforced | 0 |
| Tom Berg | tom.berg@copperline.example | Enforced | 0 |
| Grace Chen | grace.chen@copperline.example | Enforced | 0 |
| Omar Novak | omar.novak@copperline.example | Enforced | 0 |
| Ines Kovac | ines.kovac@copperline.example | Enforced | 0 |
| Karl Petrov | karl.petrov@copperline.example | Enforced | 0 |
| Nadia Webb | nadia.webb@copperline.example | Enforced | 0 |
| Peter Aziz | peter.aziz@copperline.example | Enforced | 0 |
| Ruth Ali | ruth.ali@copperline.example | Enforced | 0 |
| Sam Kim | sam.kim@copperline.example | Enforced | 0 |
| Tara Osei | tara.osei@copperline.example | Enforced | 0 |
| Victor Lindqvist | victor.lindqvist@copperline.example | Enforced | 0 |
| Wendy Fischer | wendy.fischer@copperline.example | Enforced | 0 |
| Yusuf Novak | yusuf.novak@copperline.example | Enforced | 0 |
| Zoe Novak | zoe.novak@copperline.example | Enforced | 0 |
| Alan Singh | alan.singh@copperline.example | Enforced | 0 |
| Bianca Weber | bianca.weber@copperline.example | Enforced | 0 |
| Carl Osei | carl.osei@copperline.example | Enforced | 0 |
| Dana Baker | dana.baker@copperline.example | Enforced | 0 |
| Emil Kim | emil.kim@copperline.example | Enforced | 0 |
| Farah Reed | farah.reed@copperline.example | Enforced | 0 |
| Greg Park | greg.park@copperline.example | Enforced | 0 |
| Hana Haddad | hana.haddad@copperline.example | Enforced | 0 |
| Ivan Kowalski | ivan.kowalski@copperline.example | Enforced | 0 |
| Julia Liu | julia.liu@copperline.example | Enforced | 0 |
| Kofi Ortiz | kofi.ortiz@copperline.example | Enforced | 0 |
| Laura Moreau | laura.moreau@copperline.example | Enforced | 0 |
| Milan Dubois | milan.dubois@copperline.example | Enforced | 0 |
| Nora Iversen | nora.iversen@copperline.example | Enforced | 0 |
| Oscar Nair | oscar.nair@copperline.example | Enforced | 0 |
| Paula Haddad | paula.haddad@copperline.example | Enforced | 0 |
| Ravi Sharma | ravi.sharma@copperline.example | Enforced | 0 |
| Stella Haugen | stella.haugen@copperline.example | Enforced | 0 |
| Umar Mensah | umar.mensah@copperline.example | Enforced | 0 |
| Vera Khan | vera.khan@copperline.example | Enforced | 0 |

## Corroboration

Two sampled production login events from the period, showing completed
MFA challenges, are attached in the sampled login event log.

----- FILE: tasks/T8/idp_config_export.txt -----
NorthID IdP configuration export
Tenant: Copperline Systems, Inc.
Exported: 2026-08-14 10:22 EDT (within the Q3 2026 observation period)

[mfa]
tenant_policy = required_for_all_users
per_group_overrides = none
exempt_groups = none
allowed_factors = authenticator_app, hardware_key
[users]
workforce_accounts = 41
mfa_enrolled = 41
mfa_pending_enrollment = 0

----- FILE: tasks/T8/sampled_login_events.log -----
# Sampled production login events (IdP sign-in log extract, Q3 2026)
2026-08-14T13:02:11Z user.login.start user=amara.fuentes@copperline.example result=mfa_challenge_issued
2026-08-14T13:02:29Z user.login.mfa user=amara.fuentes@copperline.example factor=authenticator_app result=success
2026-08-14T13:02:29Z user.login.complete user=amara.fuentes@copperline.example result=success
2026-09-09T09:44:03Z user.login.start user=marcus.marsh@copperline.example result=mfa_challenge_issued
2026-09-09T09:44:31Z user.login.mfa user=marcus.marsh@copperline.example factor=hardware_key result=success
2026-09-09T09:44:31Z user.login.complete user=marcus.marsh@copperline.example result=success

Respond in EXACTLY this format:
VERDICT: Sufficient or Insufficient
REASON: <one line>
```

---

## T9 - Backup success is not a restore test

```
CONTROL CLAIM(S) TO EVALUATE:
- Backups are regularly tested to confirm data can be restored (CC7.4), observation period Jul 1 - Sep 30, 2026.

EVIDENCE ARTIFACTS:
----- FILE: tasks/T9/backup_policy.md -----
# Backup and Restore Policy (excerpt)

Policy ID: POL-BKP-002 - Effective: 2026-01-15 - Owner: Director of IT Operations

1. Production databases are backed up nightly. Backup job completion is
   monitored, and failed jobs are retried within the same backup window.
2. Backups are retained for 35 days in the backup platform.
3. Restore testing: a full restore of each production database backup
   must be performed and verified at least quarterly. Every restore
   test is documented in a restore test record showing the backup
   restored, the test date, the verification checks performed, and the
   result.
4. The restore test record is the audit evidence of restorability.
   Backup job completion records show that data was copied; they are
   not, on their own, evidence that data can be restored.

----- FILE: tasks/T9/backup_job_log_2026-09.csv -----
date,job_id,target,type,status,size_gb,duration_min
2026-09-01,BK-3301,prod-db-01,full,success,423,38
2026-09-02,BK-3302,prod-db-01,full,success,430,43
2026-09-03,BK-3303,prod-db-01,full,success,437,48
2026-09-04,BK-3304,prod-db-01,full,success,444,40
2026-09-05,BK-3305,prod-db-01,full,success,451,45
2026-09-06,BK-3306,prod-db-01,full,success,429,50
2026-09-07,BK-3307,prod-db-01,full,success,436,42
2026-09-08,BK-3308,prod-db-01,full,success,443,47
2026-09-09,BK-3309,prod-db-01,full,success,450,39
2026-09-10,BK-3310,prod-db-01,full,success,428,44
2026-09-11,BK-3311,prod-db-01,full,success,435,49
2026-09-12,BK-3312,prod-db-01,full,success,442,41
2026-09-13,BK-3313,prod-db-01,full,success,449,46
2026-09-14,BK-3314,prod-db-01,full,success,427,38
2026-09-15,BK-3315,prod-db-01,full,success,434,43
2026-09-16,BK-3316,prod-db-01,full,success,441,48
2026-09-17,BK-3317,prod-db-01,full,success,448,40
2026-09-18,BK-3318,prod-db-01,full,success,426,45
2026-09-19,BK-3319,prod-db-01,full,success,433,50
2026-09-20,BK-3320,prod-db-01,full,success,440,42
2026-09-21,BK-3321,prod-db-01,full,success,447,47
2026-09-22,BK-3322,prod-db-01,full,success,425,39
2026-09-23,BK-3323,prod-db-01,full,success,432,44
2026-09-24,BK-3324,prod-db-01,full,success,439,49
2026-09-25,BK-3325,prod-db-01,full,success,446,41
2026-09-26,BK-3326,prod-db-01,full,success,424,46
2026-09-27,BK-3327,prod-db-01,full,success,431,38
2026-09-28,BK-3328,prod-db-01,full,success,438,43
2026-09-29,BK-3329,prod-db-01,full,success,445,48
2026-09-30,BK-3330,prod-db-01,full,success,423,40

Respond in EXACTLY this format:
VERDICT: Sufficient or Insufficient
REASON: <one line>
```

---

## T10 - The second one that should pass

```
CONTROL CLAIM(S) TO EVALUATE:
- Penetration testing is performed at least annually and findings are addressed (CC7.1).

EVIDENCE ARTIFACTS:
----- FILE: tasks/T10/penetration_test_report.md -----
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

----- FILE: tasks/T10/finding_disposition_memo.md -----
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

Respond in EXACTLY this format:
VERDICT: Sufficient or Insufficient
REASON: <one line>
```

---

## T11 - The wrong report type

```
CONTROL CLAIM(S) TO EVALUATE:
- Logical access controls operated effectively throughout the observation period Oct 1 - Dec 31, 2026 (CC6.1).

EVIDENCE ARTIFACTS:
----- FILE: tasks/T11/soc2_type1_report_summary.md -----
# SOC 2 Type I Report - Summary

- Organization: Copperline Systems, Inc.
- Report type: SOC 2 Type I (Security, Confidentiality)
- Opinion: Unqualified (clean) - the controls were suitably designed
  as of November 15, 2026
- Report date: November 15, 2026
- Independent auditor: Meridian Assurance LLP

## Description of the system

Copperline Systems, Inc. operates a cloud-hosted production platform
providing transaction processing and account management services to
business customers. The system comprises the customer-facing web
application and public API, the production cloud infrastructure
hosting them, the production database tier, and the administrative
access paths used by Copperline personnel. Section III of the report
describes the system's components, the services provided, and the
control environment in detail.

## Scope and basis of the examination

The examination covered the suitability of the DESIGN of the controls
stated in Section IV of the report, relevant to the Security and
Confidentiality trust services categories, AS OF November 15, 2026.
Our procedures were limited to inquiry of Copperline management,
inspection of design documentation (policies, standards, and system
configuration baselines), and walkthroughs performed as of that date.

A Type I report addresses whether controls were suitably designed to
meet the applicable trust services criteria as of a specified point in
time. It does NOT include an evaluation of the operating effectiveness
of controls over a period of time, and no opinion is expressed on
operating effectiveness. Procedures did not include testing of
controls across any period, sample-based testing of transactions, or
reperformance of controls. This report is not a Type II report.

## Control design - logical access (CC6.1)

Section IV describes the following controls as designed:

- Workforce access to production systems requires unique user IDs and
  multi-factor authentication, configured at the identity provider.
- Access is provisioned only on documented manager approval, and
  access is removed within 24 hours of a termination notice from HR.
- User access is reviewed quarterly by system owners for continued
  business need.
- Administrative access to the production environment is restricted to
  a named engineering group and requires a separate privileged
  credential.

In our opinion, the controls described were suitably designed, as of
November 15, 2026, to provide reasonable assurance that the applicable
trust services criteria would be met if the controls operated
effectively. We express no opinion on whether the controls in fact
operated effectively at any time, or during any period.

## Intended use

This summary is intended for the use of Copperline management and its
customers solely in evaluating the design of the controls described
above as of November 15, 2026.

Respond in EXACTLY this format:
VERDICT: Sufficient or Insufficient
REASON: <one line>
```

---

## T12 - Approved on paper

```
CONTROL CLAIM(S) TO EVALUATE:
- All production changes in Q1 2026 were approved before deployment (CC8.1).

EVIDENCE ARTIFACTS:
----- FILE: tasks/T12/cab_approval_log.csv -----
change_id,title,requester,submitted_at,approver,approved_at,decision
CHG-5101,Database index rebuild for orders table,M. Chen,2026-02-03 09:12,L. Fischer,2026-02-03 10:15,Approved
CHG-5102,API gateway rate-limit configuration,R. Alvarez,2026-03-09 15:26,L. Fischer,2026-03-10 09:00,Approved
CHG-5103,TLS certificate rotation - customer portal,T. Nguyen,2026-01-20 10:02,J. Okafor,2026-01-20 11:30,Approved
CHG-5104,Payments v2 feature flag rollout,S. Patel,2026-02-18 13:40,M. Chen,2026-02-18 15:45,Approved
CHG-5105,Billing webhook retry hotfix,S. Patel,2026-03-22 12:48,S. Patel,2026-03-22 13:05,Approved
CHG-5106,OS patching - application servers,D. Reyes,2026-03-27 08:55,L. Fischer,2026-03-27 09:40,Approved

----- FILE: tasks/T12/deployment_log.csv -----
change_id,title,deployed_by,deployed_at,environment,result
CHG-5101,Database index rebuild for orders table,M. Chen,2026-02-04 21:00,production,Success
CHG-5102,API gateway rate-limit configuration,R. Alvarez,2026-03-09 22:40,production,Success
CHG-5103,TLS certificate rotation - customer portal,T. Nguyen,2026-01-21 01:15,production,Success
CHG-5104,Payments v2 feature flag rollout,S. Patel,2026-02-19 20:30,production,Success
CHG-5105,Billing webhook retry hotfix,S. Patel,2026-03-22 18:20,production,Success
CHG-5106,OS patching - application servers,D. Reyes,2026-03-28 23:05,production,Success

Respond in EXACTLY this format:
VERDICT: Sufficient or Insufficient
REASON: <one line>
```
