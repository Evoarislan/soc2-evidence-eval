"""Scorer for the SOC 2 Evidence Judgment Eval.

Recomputes scores from a results.json produced by run_eval.py. The only
input you pass is the results file; the answer key (tasks.json) is located
alongside this script unless --tasks overrides it. No model calls are made.

Scoring (per the design brief):
  - Verdict exact-match = full points for the task; wrong verdict = 0.
    No partial credit on verdicts. T4 is scored as two half-verdicts
    (0.5 per claim). Headline score is out of 12.0.
  - Reason-hit rate is reported SEPARATELY and never added to the headline
    score: for each verdict unit, a hit means the model's one-line reason
    contains at least one of that unit's anchor terms (case-insensitive).
    T4 contributes two verdict units, so the denominator is 13.

Usage:
    python score.py results/mock-all-correct.json
    python score.py results/model-run.json --json scores.json
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def reason_hit(reason, anchors):
    text = (reason or "").lower()
    return any(a.lower() in text for a in anchors)


def score(results, spec):
    key = {t["id"]: t for t in spec["tasks"]}
    per_task = []
    total = 0.0
    max_total = 0.0
    hits = 0
    units = 0

    for entry in results["tasks"]:
        task = key[entry["id"]]
        reason = entry.get("reason", "")
        if task.get("multi_claim"):
            max_total += 1.0
            pts = 0.0
            unit_detail = []
            for sub in task["subclaims"]:
                units += 1
                got = (entry.get("verdict") or {}).get(sub["control"])
                ok = got == sub["verdict"]
                if ok:
                    pts += sub.get("points", 0.5)
                hit = reason_hit(reason, sub["anchors"])
                if hit:
                    hits += 1
                unit_detail.append({
                    "control": sub["control"],
                    "expected": sub["verdict"],
                    "got": got,
                    "correct": ok,
                    "reason_hit": hit,
                })
            total += pts
            per_task.append({
                "id": task["id"], "points": pts, "max_points": 1.0,
                "units": unit_detail,
            })
        else:
            max_total += 1.0
            units += 1
            got = entry.get("verdict")
            ok = got == task["verdict"]
            pts = 1.0 if ok else 0.0
            total += pts
            hit = reason_hit(reason, task["anchors"])
            if hit:
                hits += 1
            per_task.append({
                "id": task["id"], "points": pts, "max_points": 1.0,
                "expected": task["verdict"], "got": got,
                "correct": ok, "reason_hit": hit,
            })

    return {
        "model": results.get("model"),
        "score": total,
        "max_score": max_total,
        "score_pct": round(100.0 * total / max_total, 1) if max_total else 0.0,
        "reason_hits": hits,
        "reason_units": units,
        "reason_hit_rate": round(hits / units, 3) if units else 0.0,
        "per_task": per_task,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="Score eval results.json.")
    ap.add_argument("results", help="Path to results.json from run_eval.py.")
    ap.add_argument("--tasks", default=os.path.join(HERE, "tasks.json"),
                    help="Answer key (default: tasks.json alongside this script).")
    ap.add_argument("--json", help="Also write the score report to this JSON path.")
    args = ap.parse_args(argv)

    with open(args.results, "r", encoding="utf-8") as f:
        results = json.load(f)
    with open(args.tasks, "r", encoding="utf-8") as f:
        spec = json.load(f)

    report = score(results, spec)

    print("Model: %s" % report["model"])
    print("Headline score: %.1f / %.1f (%.1f%%)" % (
        report["score"], report["max_score"], report["score_pct"]))
    print("Reason-hit rate: %d/%d = %.3f (diagnostic only)" % (
        report["reason_hits"], report["reason_units"], report["reason_hit_rate"]))
    for row in report["per_task"]:
        if "units" in row:
            detail = "; ".join(
                "%s expected %s got %s %s" % (
                    u["control"], u["expected"], u["got"],
                    "OK" if u["correct"] else "WRONG")
                for u in row["units"])
            print("  %s: %.1f/1.0  (%s)" % (row["id"], row["points"], detail))
        else:
            print("  %s: %.1f/1.0  expected %s got %s %s reason-hit=%s" % (
                row["id"], row["points"], row["expected"], row["got"],
                "OK" if row["correct"] else "WRONG", row["reason_hit"]))

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        print("Wrote %s" % args.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
