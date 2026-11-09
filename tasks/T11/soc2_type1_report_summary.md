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
