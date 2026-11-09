# micro1 Eval Hackathon — SOC 2 Evidence Judgment Eval: Design Brief

Status: DESIGN ONLY — no code, no registration, no submission yet.
Decided: Nov 4, 2026 — micro1 is the ANCHOR entry for Nov 5–8 (do both, Vultr gated).
Build starts: Nov 5, 2026 (~09:12 ET kickoff). Submission target: Nov 8, 2026 by 10:00 PM ET.
Hard close: Nov 9, 2026, 05:15 GMT = Nov 9, 12:15 AM Toronto.

## Verified facts (checked live Nov 5, 2026, 13:09 UTC)

- Event page: https://www.hackerrank.com/event/micro1-eval-hackathon
- Registration on the page closed Oct 30, 07:00 GMT — BUT late join is still open: the page says
  "You can still participate! See Event Details to find out how." and the FAQ confirms a direct
  challenge link runs until submissions close. Late-join link: https://hr.gs/micro1-eval-hackathon
  (join + short onboarding form).
- Submission: ONE zip file, code only, max 50 MB, PLUS a link to a short video walkthrough
  (≤5 min per the Oct 27 check) and a short description. Do NOT put videos inside the zip.
- Tasks: 5–10 recommended, no maximum; quality over quantity. Each task clear, gradable, meaningful.
- Judging: /100 by micro1 experts — rigor, defensible grading, meaningful frontier failures,
  reproducibility. Results Nov 23, 2026.
- Rules: solo only, one entry; 18+ with 2+ years professional experience; Canada eligible.
  Must accept the micro1 Participant Agreement before submitting. Submissions must be original
  work and must NOT contain confidential employer or client data — ALL evidence in this eval
  is synthetic, built for the task (same discipline as SettleProof's synthetic data).
  IP stays with the builder; micro1 gets a license under the Participant Agreement.
  Prior work allowed if disclosed.
- Models: no credits provided; testing at entrant's cost. FAQ suggests free OpenRouter tier.
  To stand out, show how FRONTIER models perform — clear frontier failures impress most.
  Budget note: Meta credits plan allocated $35 for micro1 eval if picked (balance $149.61,
  hard stop $5). Muse Spark 1.3 via Meta API is one testable model; frontier runs beyond
  the free tier need John's explicit spend call.
- Strong-eval bar (from the event FAQ): targets a real limitation that matters in practice,
  not a trick; tasks clear with a defensible correct answer; grader reliable (no false
  passes/fails); frontier models fail for a meaningful, explained reason; original, reproducible.

## The eval concept (one line)

"Does this evidence actually prove this SOC 2 control operated effectively?" — a judgment
task auditors do daily and frontier models consistently get wrong, because they over-accept
plausible-looking artifacts and under-check dates, scope, population coverage, and
criterion fit. Domain: SOC 2 Type I/II evidence judgment (CC6 logical access, CC7 monitoring,
CC8 change management), John's strongest domain.

## Task set (8 tasks — inside the recommended 5–10)

Every task ships as: synthetic evidence artifact(s) + control claim + question.
Expected output per task: VERDICT (Sufficient / Insufficient) + criterion + one-line reason.
Grader: exact verdict match (binary) + reason-keyword check (partial credit, see below).
No task depends on real client data. All dates, names, systems are fictional.

### T1 — Screenshot vs control (CC6.1): the plausible screenshot
- Artifact: SSO dashboard screenshot showing MFA "enabled" for the org.
- Claim: "MFA is enforced for all workforce users (CC6.1)."
- Trap: screenshot shows the tenant-level toggle ON but the per-group policy list shows the
  "Contractors" group exempted; 3 of 41 sampled users are contractors.
- Correct: INSUFFICIENT — enforcement is not org-wide; exemption unaddressed.
- Frontier failure mode: models accept the toggle screenshot as proof and never read the
  group-policy panel.

### T2 — Out-of-period evidence (CC7.2): the stale log
- Artifact: vulnerability-scan report dated Mar 3, 2026, clean.
- Claim: "Vulnerabilities are scanned weekly and remediated within SLA (CC7.2), observation
  period Apr 1–Jun 30, 2026."
- Trap: the only scan in the period is dated Jul 8 (after period end); the Mar 3 report is
  outside the observation window.
- Correct: INSUFFICIENT — no in-period evidence; timing matters, not just existence.
- Failure mode: models judge the artifact's content and ignore the observation-period boundary.

### T3 — Population coverage (CC6.1): the access review that misses one
- Artifacts: quarterly access-review sign-off (all 38 users "reviewed") + HR termination list
  showing 1 termination (Jun 12) + IdP user list (39 active accounts, incl. the terminated user).
- Claim: "Access is reviewed quarterly and terminated users are removed promptly (CC6.1)."
- Trap: terminated user still active 18 days after termination; review sign-off predates the
  termination and covers a stale population.
- Correct: INSUFFICIENT — orphaned account; review population was incomplete.
- Failure mode: models take the signed review at face value and never reconcile the three lists.

### T4 — Criterion confusion (CC6.6 vs CC7.2): right artifact, wrong control
- Artifact: encryption-at-rest configuration report (AES-256, KMS keys rotated).
- Claim: "Encryption protects data at rest (CC6.6)."
- Second claim in the same task: the SAME artifact offered for "system monitoring detects
  anomalies (CC7.2)."
- Correct: SUFFICIENT for CC6.6; INSUFFICIENT for CC7.2 (a config report is not monitoring).
- Failure mode: models map any security-looking artifact to any security-sounding control.

### T5 — Policy vs practice (CC8.1): the change ticket
- Artifacts: change-management policy (requires peer approval + testing evidence) + change
  ticket CHG-4417 (production deploy, approved by the requester themselves, no test evidence
  attached, "emergency" flag with no post-hoc review).
- Claim: "Changes are approved and tested before production (CC8.1)."
- Correct: INSUFFICIENT — self-approval violates segregation; emergency path used without
  the required retrospective.
- Failure mode: models see "approved" status and stop; they don't check WHO approved or
  whether the emergency exception was closed out.

### T6 — Vendor report scope (CC9.2 / subservice org): the carve-out gap
- Artifact: subservice provider SOC 2 Type II report summary — clean opinion, period
  Oct 1, 2025–Sep 30, 2026, BUT the report carves out the provider's backup subsystem
  ("carved-out subservice organization") and the in-scope system stores backups there.
- Claim: "Vendor monitoring is covered by the vendor's SOC 2 report (CC9.2)."
- Correct: INSUFFICIENT — the carved-out subsystem is exactly where the data lives; reliance
  is unsupported without complementary controls.
- Failure mode: models read "clean opinion" and miss the carve-out paragraph entirely.

### T7 — Log integrity (CC7.2): the gap in the sequence
- Artifact: 30 days of audit-log exports, one per day, except days 14–16 missing; admin
  attestation says "logs retained 90 days, no gaps."
- Claim: "Audit logs are complete and retained (CC7.2)."
- Correct: INSUFFICIENT — 3-day gap unexplained; attestation contradicts the artifacts.
- Failure mode: models trust the attestation over the artifact set and don't count the days.

### T8 — The one that SHOULD pass (calibration): complete evidence
- Artifacts: MFA enforcement report (all 41 users, no exemptions) + IdP config export dated
  inside the period + two sampled login events showing MFA challenge.
- Claim: "MFA is enforced for all workforce users (CC6.1)."
- Correct: SUFFICIENT — population complete, in period, corroborated by sampled events.
- Purpose: catches graders/evals that reward blanket skepticism; a good model should pass this.

## Grader design (rigorous, defensible — this is what judges score)

- Per task: verdict exact-match = 1.0; wrong verdict = 0. No partial credit on verdict.
- Reason check (diagnostic, reported separately, NOT added to the headline score): the model's
  one-line reason must contain at least one of the task's anchor terms (listed per task in
  tasks.json, e.g. T1: "contractor/exempt"; T3: "terminated/orphan"). Reported as reason-hit
  rate so a lucky verdict without the right reason is visible.
- Anti-gaming: T8 (the sufficient case) penalizes refuse-everything strategies; T4's split
  verdict penalizes single-verdict-per-artifact shortcuts.
- Reproducibility: `run_eval.py` takes a model endpoint + task dir, writes `results.json`
  (per-task verdict, reason, raw output, latency), and `score.py` recomputes from results.json
  alone. Fixed seeds / pinned model versions recorded; temperature 0 for the graded run.
- Harness: OpenRouter free-tier models first (zero cost); one frontier run per task set if
  budget approved; Muse Spark 1.3 via Meta credits as an additional data point (within the
  $35 allocation, hard stop $5 overall).
- Human baseline: John grades all 8 tasks himself first (answer key + reasons) — the key is
  HIS judgment, which is the point of the domain. Disagreements between John's key and the
  grader's anchor terms get resolved in the key, not by loosening the grader.

## Build order (fits Nov 5–8; Vultr runs in parallel, gated Nov 7 noon)

1. (Nov 5) Scaffold repo + write all 8 synthetic artifacts + tasks.json answer key (John's verdicts).
2. (Nov 5–6) Grader + runner + OpenRouter free-tier baseline run; record frontier-failure evidence.
3. (Nov 7) Frontier run if budget approved; package zip; record ≤5-min walkthrough video.
4. (Nov 8) Submit by 10:00 PM ET (Vultr first, 6:00 PM ET, per the gated plan). Registration:
   late-join link https://hr.gs/micro1-eval-hackathon — John's click; Participant Agreement
   acceptance is his step at submission time.

## Open items for John (none block starting the build)

- Confirm the 8 task verdicts as the answer key (his call; he is the domain expert).
- Frontier-model spend: approve any run beyond the OpenRouter free tier / Meta $35 allocation.
- Registration click on the late-join link + Participant Agreement at submission.

## Sources

- Event page (read live Nov 5, 2026): https://www.hackerrank.com/event/micro1-eval-hackathon
- Late-join link from that page: https://hr.gs/micro1-eval-hackathon
- Decisions: Nov 4, 2026 slate — micro1 anchor, Vultr gated, checkpoint Nov 7 noon ET,
  submissions Nov 8 (Vultr 6 PM, micro1 10 PM ET); nothing registered yet, submissions need
  John's explicit yes per event.
- Budget: ~/workspace/survival/meta-entry/CREDITS-PLAN.md ($35 micro1 allocation, $5 hard stop).
