#!/usr/bin/env python3
"""Run the eval against Muse Spark 1.3 (Meta Model API, standard tier)
through the gated credit runner (~/workspace/survival/meta-credits/
runner.mjs), so every call is estimated, capped, and ledgered under
the 'eval' lane. Usage:

  python3 run_spark_eval.py --variant auditor [--only T1]

Writes results/v2-spark13-<variant>.json in run_eval.py results
format, ready for score.py. Live API calls: requires the runner's
own gates (META_CREDITS_LIVE=YES is set for the child processes).
"""
import argparse
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import run_eval as re_

RUNNER = os.path.expanduser("~/workspace/survival/meta-credits/runner.mjs")
MODEL = "muse-spark-1.3"
CAP_PER_CALL = "0.05"


def call_spark(system_prompt, prompt, max_tokens=None):
    env = dict(os.environ, META_CREDITS_LIVE="YES")
    cmd = ["node", RUNNER, "run", "--lane", "eval", "--model", MODEL,
           "--prompt", prompt, "--system", system_prompt,
           "--temperature", "0", "--cap", CAP_PER_CALL, "--live"]
    if max_tokens:
        cmd += ["--max-tokens", str(max_tokens)]
    out = subprocess.run(cmd, capture_output=True, text=True, env=env,
                         timeout=600)
    if out.returncode != 0:
        raise RuntimeError("runner failed: %s %s" % (out.stdout, out.stderr))
    marker = "--- response ---\n"
    if marker not in out.stdout:
        raise RuntimeError("no response marker in runner output: %s"
                           % out.stdout)
    return out.stdout.split(marker, 1)[1].strip()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", choices=["auditor", "neutral"],
                    required=True)
    ap.add_argument("--only", help="Run a single task id (pilot).")
    ap.add_argument("--max-tokens", default=None,
                    help="Completion budget passed to the runner.")
    ap.add_argument("--tag", default="",
                    help="Suffix for the output filename (e.g. runb).")
    args = ap.parse_args(argv)

    spec = re_.load_tasks(os.path.join(HERE, "tasks.json"))
    base_dir = HERE
    system_prompt = re_.SYSTEM_PROMPTS[args.variant]

    results = {
        "eval": spec.get("eval_name"),
        "model": "meta-api:%s" % MODEL,
        "temperature": 0,
        "mode": "live",
        "system_prompt_variant": args.variant,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "tasks": [],
    }
    for task in spec["tasks"]:
        if args.only and task["id"] != args.only:
            continue
        prompt = re_.build_prompt(task, base_dir)
        start = time.time()
        raw = call_spark(system_prompt, prompt, args.max_tokens)
        latency = round(time.time() - start, 3)
        verdict, reason = re_.parse_output(task, raw)
        results["tasks"].append({
            "id": task["id"], "verdict": verdict, "reason": reason,
            "raw_output": raw, "latency_s": latency,
        })
        print("%s -> %s" % (task["id"], verdict), flush=True)

    suffix = ("-" + args.tag) if args.tag else ""
    out = os.path.join(HERE, "results",
                       "v2-spark13-%s%s.json" % (args.variant, suffix))
    if args.only:
        out = os.path.join(HERE, "results",
                           "v2-spark13-%s-pilot-%s%s.json"
                           % (args.variant, args.only, suffix))
    with open(out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("Wrote %s" % out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
