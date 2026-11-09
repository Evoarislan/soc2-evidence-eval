# Grader Self-Test Results

Run: Nov 5, 2026 (originally 8 tasks, extended the same day to 10, then
hardened to 12 as v2.0 - see the CHANGELOG in README.md). Method:
`run_eval.py --mock` feeds scripted model outputs through the exact
same prompt-build, output-parse, and results-write path used for live
runs; `score.py` then grades the resulting results files. Zero external
calls, zero spend.

Commands:

```bash
python run_eval.py --mock all-correct --out results/mock-all-correct.json
python score.py results/mock-all-correct.json --json results/mock-all-correct-scores.json
python run_eval.py --mock naive --out results/mock-naive.json
python score.py results/mock-naive.json --json results/mock-naive-scores.json
```

## Mock set 1: all-correct (expected 12.0/12.0)

Scripted outputs give the keyed verdict on every task, with reasons that
cite the real defect (or, for T8, the corroboration, and for T10, the
finding dispositions).

- **Headline score: 12.0 / 12.0 (100.0%)**
- **Reason-hit rate: 13/13 = 1.000**
- Per task: T1-T12 all correct, including T4's split verdict
  (CC6.6 Sufficient, CC7.2 Insufficient).

## Mock set 2: naive accept-everything (expected: fails T1-T7, T9, T11, T12; passes T8 and T10)

Scripted outputs judge every claim Sufficient with a generic,
surface-level reason: the failure mode the eval is designed to expose.

- **Headline score: 2.5 / 12.0 (20.8%)**
- **Reason-hit rate: 2/13 = 0.154**
- Per task: T1, T2, T3, T5, T6, T7, T9, T11, T12 wrong (0.0 each); T4
  half-correct (0.5: CC6.6 right, CC7.2 wrong); T8 correct (1.0);
  T10 correct verdict (1.0) but reason-hit = miss (see below).

## Known diagnostic caveats (documented, not hidden)

The naive T7 reason quotes the attestation ("no gaps"), which contains
the anchor substring "gap", so that unit registers a reason-hit despite
the wrong verdict. Anchor matching is substring-based and diagnostic
only; it never affects the headline score. This is the expected limit of
a keyword diagnostic and is why the reason-hit rate is reported
separately rather than blended into grading.

The naive T10 result is the mirror-image case, and it is by design: an
accept-everything strategy happens to land on the correct Sufficient
verdict, but its generic reason ("strong overall security posture")
contains none of the unit's anchor terms (risk acceptance, compensating
controls, dispositions, retest), so the unit earns no reason-hit. The
diagnostic exposes a lucky verdict with no understanding of why the
evidence passes, which is exactly the failure the two should-pass tasks
with different shapes (T8, T10) are built to separate from real
judgment.

## Verdict

The grader passes validation on the v2.0 task set: the key-consistent
set achieves a perfect score with a perfect reason-hit rate, and the
naive set fails every trap task - including the new Type I / Type II
trap (T11) and the compound change-management trap (T12) - while
passing only the two calibration tasks (one of them, T10, on the
verdict alone, with reasoning that misses every disposition) and the
one half of T4 where acceptance happens to be right. The harness is
ready for live model runs.
