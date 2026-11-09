"""Scripted model outputs for grader validation (run_eval.py --mock).

Two sets:
  all-correct : every verdict matches the answer key in tasks.json, with
                reasons that cite the real defect (or, for T8 and T10, the
                real corroboration / dispositions). Expected headline
                score: 12.0/12.0.
  naive       : the "accept everything plausible" failure mode the eval is
                designed to expose: every claim judged Sufficient with a
                generic, surface-level reason. Expected headline score:
                2.5/12.0 (T8 correct = 1.0; T10 correct verdict = 1.0 but
                with a generic reason that earns no reason-hit; T4
                half-correct = 0.5).
"""

ALL_CORRECT = {
    "T1": (
        "VERDICT: Insufficient\n"
        "REASON: The tenant MFA toggle is on, but the group policy exempts "
        "the Contractors group and 3 of the 41 sampled users are contractors, "
        "so enforcement is not org-wide."
    ),
    "T2": (
        "VERDICT: Insufficient\n"
        "REASON: The only clean report is dated Mar 3, outside the period; "
        "the scan history shows no in-period scans between Apr 1 and Jun 30 "
        "and the next scan is Jul 8, after period end."
    ),
    "T3": (
        "VERDICT: Insufficient\n"
        "REASON: The user terminated on Jun 12 is still active in the IdP on "
        "Jun 30, 18 days later, and the review sign-off predates the "
        "termination and covers a stale population of 38 while the IdP "
        "lists 39 active accounts."
    ),
    "T4": (
        "VERDICT_CC6.6: Sufficient\n"
        "VERDICT_CC7.2: Insufficient\n"
        "REASON: AES-256 encryption at rest with rotated KMS keys directly "
        "supports CC6.6, but a configuration report is not monitoring "
        "evidence and does not detect anomalies, so it cannot support CC7.2."
    ),
    "T5": (
        "VERDICT: Insufficient\n"
        "REASON: The ticket was self-approved by the requester with no peer "
        "review, no testing evidence attached, and the emergency flag was "
        "used without the required post-hoc review."
    ),
    "T6": (
        "VERDICT: Insufficient\n"
        "REASON: The vendor report carves out the backup subsystem as a "
        "carved-out subservice organization, and the in-scope system stores "
        "its backups exactly there, so the clean opinion does not cover it."
    ),
    "T7": (
        "VERDICT: Insufficient\n"
        "REASON: Exports for Sep 14, 15 and 16 are missing, a 3-day gap in "
        "the 30-day sequence, and the attestation claiming no gaps "
        "contradicts the artifacts."
    ),
    "T8": (
        "VERDICT: Sufficient\n"
        "REASON: The report covers all 41 users with no exemptions, the "
        "config export is dated in period, and sampled login events show "
        "MFA challenges corroborating enforcement."
    ),
    "T9": (
        "VERDICT: Insufficient\n"
        "REASON: All 30 nightly backup jobs show Success, but there is no "
        "restore test record anywhere in the evidence: successful backups "
        "prove data was copied, not that it can be restored, and the "
        "quarterly restore testing the policy requires is unevidenced."
    ),
    "T10": (
        "VERDICT: Sufficient\n"
        "REASON: The test was performed in period on the production scope; "
        "the critical finding was remediated and confirmed closed on "
        "retest, and the two medium findings were formally risk-accepted "
        "by the CISO with compensating controls and a scheduled retest, "
        "so all findings are dispositioned."
    ),
    "T11": (
        "VERDICT: Insufficient\n"
        "REASON: The evidence is a SOC 2 Type I report: it opines only on "
        "the design of controls as of a point in time (November 15, 2026) "
        "and expressly does not evaluate operating effectiveness over a "
        "period, so it cannot support an operating-effectiveness claim "
        "for Oct 1 - Dec 31, 2026."
    ),
    "T12": (
        "VERDICT: Insufficient\n"
        "REASON: CHG-5102 was deployed on Mar 9 at 22:40, before approval "
        "was recorded on Mar 10 at 09:00, and CHG-5105 was self-approved "
        "by its own requester, so not every change was independently "
        "approved before deployment."
    ),
}

NAIVE = {
    "T1": (
        "VERDICT: Sufficient\n"
        "REASON: The dashboard screenshot clearly shows MFA enabled for the "
        "organization, which demonstrates the control is operating."
    ),
    "T2": (
        "VERDICT: Sufficient\n"
        "REASON: A clean vulnerability scan report with zero critical or "
        "high findings shows scanning is performed and issues are handled."
    ),
    "T3": (
        "VERDICT: Sufficient\n"
        "REASON: The quarterly access review is signed off as complete for "
        "all users, indicating access is reviewed on schedule."
    ),
    "T4": (
        "VERDICT_CC6.6: Sufficient\n"
        "VERDICT_CC7.2: Sufficient\n"
        "REASON: The report confirms strong AES-256 encryption with managed "
        "keys, a solid security control that supports the claims."
    ),
    "T5": (
        "VERDICT: Sufficient\n"
        "REASON: The change ticket shows an approved status and was "
        "deployed to production, so the change process was followed."
    ),
    "T6": (
        "VERDICT: Sufficient\n"
        "REASON: The vendor holds a clean SOC 2 Type II opinion covering a "
        "full year, which provides strong assurance over the vendor."
    ),
    "T7": (
        "VERDICT: Sufficient\n"
        "REASON: The administrator attests that logs are retained for 90 "
        "days with no gaps, and daily log exports are provided."
    ),
    "T8": (
        "VERDICT: Sufficient\n"
        "REASON: The enforcement report shows MFA required for the "
        "workforce and sampled logins confirm users are challenged."
    ),
    "T9": (
        "VERDICT: Sufficient\n"
        "REASON: Thirty consecutive days of backups completed with a "
        "Success status and no failures, showing a reliable backup "
        "process that protects the production database."
    ),
    "T10": (
        "VERDICT: Sufficient\n"
        "REASON: The penetration test was performed recently by an "
        "outside firm covering production, and the report presents a "
        "strong overall security posture."
    ),
    "T11": (
        "VERDICT: Sufficient\n"
        "REASON: The company holds a SOC 2 report with a clean opinion "
        "from an independent CPA firm covering its logical access "
        "controls, which provides strong assurance over the period."
    ),
    "T12": (
        "VERDICT: Sufficient\n"
        "REASON: Every change in the quarter has a recorded approval and "
        "a successful production deployment, showing the change approval "
        "process was followed."
    ),
}

MOCK_SETS = {
    "all-correct": ALL_CORRECT,
    "naive": NAIVE,
}
