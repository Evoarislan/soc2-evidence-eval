# SOC 2 Evidence Judgment Eval

**One question, asked twelve ways: does this evidence actually prove this
SOC 2 control operated effectively?**

Auditors make this judgment daily. Frontier language models consistently
get it wrong: they over-accept plausible-looking artifacts and under-check
dates, scope, population coverage, and whether the artifact matches the
criterion at all. This eval measures that failure mode directly, with
synthetic evidence, a defensible answer key, and a grader that cannot be
gamed by blanket skepticism or blanket acceptance.

All evidence is synthetic and fictional (invented company, people,
systems, and dates). No real client or employer data is used anywhere.

## Headline results (v2, 12 tasks / 13 verdict units, temperature 0)

| Model / run | Verdicts | Reason-hit |
|---|---|---|
| Nemotron 3 Ultra 550B (OpenRouter free) | 12.0/12 auditor, 12.0/12 neutral | 13/13, 12/13 |
| Nemotron 3 Nano Reasoning (OpenRouter free) | 11.0/12 auditor, 12.0/12 neutral | 10/13, 12/13 |
| DeepSeek V4.1 Flash (Freebuff) | 12.0/12 | 12/13 |
| Muse Spark 1.3, adequate budget (4,000-token cap) | 12.0/12 both prompts | 12/13, 13/13 |
| Muse Spark 1.3, tight budget (1,500-token cap) | 9.0 / 11.0 of 12 | 10/13, 12/13 |
| Accept-everything baseline | 2.5/12 (20.8%) | 2/13 |
| Reject-everything ceiling | 9.5/12 | n/a |

Two findings worth the read (full detail in [RESULTS.md](RESULTS.md)):

1. **The first genuine verdict failure by a strong model** came from the v2 hardening: Nemotron Nano accepted the T6 vendor evidence as Sufficient, missing the mid-paragraph scope carve-out that excludes exactly the subsystem holding the data.
2. **Evals can measure the harness instead of the model.** At a 1,500-token completion cap, Muse Spark returned empty content on 5 of 28 calls (scored as failures); at 4,000 tokens, 0 of 24. Budget artifacts must be separated from judgment failures before any score is believed.

Video walkthrough (4:09): https://youtu.be/KXrl8se0Djk

## The tasks

Each task ships synthetic evidence artifact(s) plus a control claim. The
model must return a verdict (**Sufficient** / **Insufficient**) and a
one-line reason.

| ID | Control | Scenario | Correct verdict |
|----|---------|----------|-----------------|
| T1 | CC6.1 | SSO screenshot shows MFA "enabled", but the Contractors group is exempt in the per-group policy panel | Insufficient |
| T2 | CC7.2 | Clean vuln-scan report dated before the observation period; no scans inside it; remediation tickets closed in-period are a distractor (activity is not scanning) | Insufficient |
| T3 | CC6.1 | Signed access review vs HR termination list vs IdP export: a terminated user is still active 18 days later | Insufficient |
| T4 | CC6.6 / CC7.2 | One encryption-at-rest config report offered for two different controls | Sufficient for CC6.6, Insufficient for CC7.2 |
| T5 | CC8.1 | Change ticket self-approved by the requester, no test evidence, emergency flag never closed out | Insufficient |
| T6 | CC9.2 | Vendor's clean SOC 2 report carves out the backup subsystem, which is exactly where the data lives; a current ISO 27001 certificate distracts and says nothing about the carve-out | Insufficient |
| T7 | CC7.2 | 30 days of audit-log exports with days 14-16 missing, plus an attestation claiming "no gaps" | Insufficient |
| T8 | CC6.1 | Complete MFA evidence: full population, no exemptions, in-period config, corroborating login events | Sufficient |
| T9 | CC7.4 | 30 days of backup jobs, every one "Success", plus a policy requiring quarterly restore tests; no restore test record anywhere in the set | Insufficient |
| T10 | CC7.1 | Pen test in period on production scope: critical finding remediated and retest-closed; two mediums formally risk-accepted by the CISO with compensating controls | Sufficient |
| T11 | CC6.1 | A pristine SOC 2 Type I report (design suitably designed AS OF one date) offered to support a Type II operating-effectiveness claim covering a full quarter | Insufficient |
| T12 | CC8.1 | CAB approval log + deployment log for six routine changes; one was deployed the night BEFORE its approval timestamp, and one was approved by its own requester - visible only by cross-referencing the two logs | Insufficient |

T8 and T10 are the calibration tasks: two genuine passes with different
evidence shapes. Together they catch graders and strategies that reward
refusing everything, while the trap tasks catch the opposite failure,
so neither blanket skepticism nor blanket acceptance scores well. T4's
split verdict penalizes one-verdict-per-artifact shortcuts.

## How to run it

Python 3, standard library only. No API key is needed for the mock runs.

```bash
# 1. Validate the grader with scripted outputs (zero external calls)
python run_eval.py --mock all-correct --out results/mock-all-correct.json
python run_eval.py --mock naive       --out results/mock-naive.json
python score.py results/mock-all-correct.json
python score.py results/mock-naive.json

# 2. Run a real model (OpenRouter-style chat completions endpoint)
#    model.json: {"base_url": "...", "model": "...", "api_key_env": "OPENROUTER_API_KEY"}
python run_eval.py --config model.json --out results/model-run.json
python score.py results/model-run.json
```

Graded runs use temperature 0. `run_eval.py` writes `results.json` with,
per task: parsed verdict, the model's one-line reason, the raw model
output, and latency. `score.py` recomputes all scores from that results
file alone (the answer key in `tasks.json` is the only other input), so
any run can be re-graded without re-calling a model.

## Grading (defensible by construction)

- **Verdict: exact match = full points, wrong = 0.** No partial credit.
  T4 is scored as two half-verdicts (0.5 per claim). Headline score is
  out of 12.0.
- **Reason-hit rate (diagnostic, reported separately, never added to the
  score):** for each verdict unit, does the model's one-line reason
  contain at least one of that unit's anchor terms (the defect, or for
  T8 and T10 the corroboration / dispositions, an auditor would cite)?
  This makes a lucky verdict with the wrong reasoning visible instead
  of hiding it. Anchor matching is case-insensitive substring matching;
  it is a diagnostic signal, not a semantic judgment.
- The answer key and anchor terms live in `tasks.json`, written from the
  domain expert's judgment, with a key reason recorded per task.

Self-test (see `SELF-TEST.md`): the scripted all-correct set scores
**12.0/12.0** with reason-hit rate **13/13**; the scripted
naive-accept-everything set scores **2.5/12.0** (right verdicts only on
T8, T10, and half of T4; its T10 verdict is right by luck and its reason
names none of the dispositions, so that unit earns no reason-hit).

## How this maps to the judging criteria

- **Rigor:** every task isolates one named failure mode (period
  boundaries, population reconciliation, criterion fit, scope carve-outs,
  segregation of duties, artifact-vs-attestation conflicts, report-type
  confusion (Type I design opinion vs Type II operating effectiveness),
  and defects visible only by cross-referencing two logs), each with a
  recorded key reason.
- **Defensible grading:** binary exact-match verdicts against a fixed
  key; no rubric drift, no LLM judge. The reason-hit diagnostic is kept
  out of the headline score precisely so it cannot inflate results.
  The key also contains two Sufficient verdicts with different evidence
  shapes (T8: complete control evidence; T10: a pen test whose open
  findings are all formally dispositioned), which strengthens the
  anti-gaming story from both directions: blanket acceptance scores
  2.5/12.0, and blanket rejection caps at 9.5/12.0 because it fails
  both genuine passes and halves T4 the wrong way.
- **Meaningful frontier failures:** the tasks target limitations that
  matter in real audit work, not tricks: models demonstrably accept
  screenshots, attestations, and clean opinions at face value.
- **Reproducibility:** temperature 0, pinned task set and key in
  `tasks.json`, raw outputs and latencies preserved in `results.json`,
  and a zero-cost mock mode that validates the full pipeline end to end.
  Total size is well under the 50 MB submission limit (text only).

## Changelog

- **v2.0 (Nov 5, 2026) - hardened.** v1 (10 tasks) was passed
  10.0/10.0 on verdicts by two strong free models (Nemotron Ultra
  550B and Nemotron Nano Reasoning) under BOTH the auditor and the
  neutral system prompt, so the task set was hardened: T11 adds the
  Type I / Type II report-type trap, T12 adds a compound
  change-management trap whose two defects require cross-referencing
  an approval log against a deployment log, and T2 / T6 gained
  plausible distractor artifacts (in-period remediation activity;
  an unrelated ISO 27001 certificate) while the T6 carve-out sentence
  was moved into the middle of a longer scope paragraph. 12 tasks,
  13 verdict units.
- **v1.0 (Nov 5, 2026).** Initial set: 10 tasks, 11 verdict units
  (grew from an 8-task draft the same day).

## Layout

```
README.md          this file
PROMPTS.md         the exact per-task user prompts (for chat-UI runs)
Q2-DRAFT.md        draft text for the submission's subjective question
SELF-TEST.md       grader validation results (mock modes)
tasks.json         task definitions, answer key, anchor terms
run_eval.py        runner (live endpoint or --mock)
score.py           grader: results.json in, scores out
mock_outputs.py    scripted outputs for the two mock sets
tasks/T1..T12/     synthetic evidence artifacts per task
results/           run outputs and score reports
```
