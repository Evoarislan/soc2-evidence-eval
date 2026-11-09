"""Grader harness runner for the SOC 2 Evidence Judgment Eval.

Usage:
    python run_eval.py --mock all-correct --out results/mock-all-correct.json
    python run_eval.py --mock naive --out results/mock-naive.json
    python run_eval.py --config model.json --out results/model-run.json

Model config JSON (OpenRouter-style chat completions):
    {
      "base_url": "https://openrouter.ai/api/v1",
      "model": "provider/model-name",
      "api_key_env": "OPENROUTER_API_KEY"
    }

Graded runs use temperature 0. The runner writes results.json with, per task:
the parsed verdict, the model's one-line reason, the raw model output, and
latency. No API key is required (or used) in --mock mode.
"""

import argparse
import http.client
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))

SYSTEM_PROMPT = (
    "You are an experienced SOC 2 auditor reviewing evidence for a control. "
    "Judge ONLY whether the evidence provided is sufficient to support the "
    "claim for the stated control and observation period. Check dates, "
    "scope, population coverage, and whether the artifact actually matches "
    "the criterion. Answer in exactly the requested format."
)

# Neutral variant: same role and format discipline, but WITHOUT the
# checklist of what to check. The auditor prompt names the exact
# dimensions the traps test (dates, scope, population, criterion fit),
# which can coach models into passing. Runs are comparable only within
# one variant; results.json records which variant produced them.
NEUTRAL_SYSTEM_PROMPT = (
    "You are an AI assistant reviewing evidence for a SOC 2 control. "
    "Evaluate the evidence provided and answer in exactly the "
    "requested format."
)

SYSTEM_PROMPTS = {
    "auditor": SYSTEM_PROMPT,
    "neutral": NEUTRAL_SYSTEM_PROMPT,
}


def load_tasks(tasks_file):
    with open(tasks_file, "r", encoding="utf-8") as f:
        return json.load(f)


def build_prompt(task, base_dir):
    parts = []
    parts.append("CONTROL CLAIM(S) TO EVALUATE:")
    if task.get("multi_claim"):
        for sub in task["subclaims"]:
            parts.append("- %s" % sub["claim"])
    else:
        parts.append("- %s" % task["claim"])
    parts.append("")
    parts.append("EVIDENCE ARTIFACTS:")
    for rel in task["artifacts"]:
        path = os.path.join(base_dir, rel)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        parts.append("----- FILE: %s -----" % rel)
        parts.append(content.rstrip())
        parts.append("")
    parts.append("Respond in EXACTLY this format:")
    if task.get("multi_claim"):
        for sub in task["subclaims"]:
            parts.append("VERDICT_%s: Sufficient or Insufficient" % sub["control"])
        parts.append("REASON: <one line covering both verdicts>")
    else:
        parts.append("VERDICT: Sufficient or Insufficient")
        parts.append("REASON: <one line>")
    return "\n".join(parts)


def parse_output(task, text):
    """Extract verdict(s) and reason from raw model output."""
    if text is None:
        return ({} if task.get("multi_claim") else None), ""
    reason = ""
    m = re.search(r"REASON:\s*(.+)", text, re.IGNORECASE)
    if m:
        reason = m.group(1).strip()
    if task.get("multi_claim"):
        verdicts = {}
        for sub in task["subclaims"]:
            pat = r"VERDICT_%s:\s*(Sufficient|Insufficient)" % re.escape(sub["control"])
            m = re.search(pat, text, re.IGNORECASE)
            verdicts[sub["control"]] = m.group(1).capitalize() if m else None
        return verdicts, reason
    m = re.search(r"VERDICT:\s*(Sufficient|Insufficient)", text, re.IGNORECASE)
    return (m.group(1).capitalize() if m else None), reason


USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)


def _call_once(url, payload, api_key):
    """One endpoint call. Returns (status, parsed_json_or_text).

    Prefers the `requests` library when installed: some API edge networks
    (Cloudflare-fronted ones) intermittently reject the default
    Python-urllib client/TLS signature with 401/403/404 responses, even
    for authenticated calls with a valid key, while `requests` and curl
    pass. Falls back to urllib with a standard browser user-agent, which
    those edges also accept more reliably than the urllib default.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer %s" % api_key,
        "User-Agent": USER_AGENT,
    }
    try:
        import requests
    except ImportError:
        requests = None
    if requests is not None:
        resp = requests.post(url, headers=headers, json=payload, timeout=180)
        try:
            return resp.status_code, resp.json()
        except ValueError:
            return resp.status_code, resp.text
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        try:
            return e.code, json.loads(body)
        except ValueError:
            return e.code, body


def call_model(config, prompt, system_prompt=SYSTEM_PROMPT):
    """Call the model endpoint, retrying transient transport failures.

    Free-tier endpoints and edge networks intermittently drop chunked
    responses, reset connections, rate-limit (429, including upstream
    provider limits), or return transient 401/403/404/5xx statuses. Those
    are transport failures, not model answers, so they are retried with
    backoff (5 tries max). A 400 means the request itself is malformed
    and is raised immediately. Retries never change the prompt, the
    temperature, or the recorded output.
    """
    api_key = os.environ.get(config.get("api_key_env", "OPENROUTER_API_KEY"), "")
    url = config["base_url"].rstrip("/") + "/chat/completions"
    payload = {
        "model": config["model"],
        "temperature": 0,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    }
    retry_statuses = {401, 403, 404, 408, 429, 500, 502, 503, 504}
    last_exc = None
    for attempt in range(5):
        try:
            status, data = _call_once(url, payload, api_key)
        except Exception as e:  # connection errors, truncated reads, timeouts
            last_exc = e
            status, data = None, None
        if status == 200 and isinstance(data, dict):
            return data["choices"][0]["message"]["content"]
        if status is not None:
            detail = data if isinstance(data, str) else json.dumps(data)[:300]
            if status not in retry_statuses:
                raise RuntimeError(
                    "HTTP %s from endpoint (not retried): %s" % (status, detail)
                )
            last_exc = RuntimeError("HTTP %s: %s" % (status, detail))
        if attempt < 4:
            time.sleep(5 * (2 ** attempt))
    raise RuntimeError("endpoint call failed after 5 attempts: %r" % (last_exc,))


def main(argv=None):
    ap = argparse.ArgumentParser(description="Run the SOC 2 evidence-judgment eval.")
    ap.add_argument("--config", help="Model endpoint config JSON (live mode).")
    ap.add_argument("--mock", choices=["all-correct", "naive"],
                    help="Use scripted model outputs instead of calling an endpoint.")
    ap.add_argument("--tasks", default=os.path.join(HERE, "tasks.json"),
                    help="Path to tasks.json (default: alongside this script).")
    ap.add_argument("--out", required=True, help="Where to write results.json.")
    ap.add_argument("--prompt-variant", choices=["auditor", "neutral"],
                    default="auditor",
                    help="System prompt variant for live runs (default: auditor).")
    args = ap.parse_args(argv)

    if not args.mock and not args.config:
        ap.error("provide --config for a live run or --mock for a scripted run")

    spec = load_tasks(args.tasks)
    base_dir = os.path.dirname(os.path.abspath(args.tasks))

    mock_outputs = None
    model_label = None
    if args.mock:
        sys.path.insert(0, HERE)
        import mock_outputs as mo
        mock_outputs = mo.MOCK_SETS[args.mock]
        model_label = "mock:%s" % args.mock
    else:
        with open(args.config, "r", encoding="utf-8") as f:
            config = json.load(f)
        model_label = config["model"]

    results = {
        "eval": spec.get("eval_name"),
        "model": model_label,
        "temperature": 0,
        "mode": "mock" if args.mock else "live",
        "system_prompt_variant": None if args.mock else args.prompt_variant,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "tasks": [],
    }

    for task in spec["tasks"]:
        prompt = build_prompt(task, base_dir)
        start = time.time()
        if args.mock:
            raw = mock_outputs[task["id"]]
            latency = 0.0
        else:
            raw = call_model(config, prompt,
                             SYSTEM_PROMPTS[args.prompt_variant])
            latency = round(time.time() - start, 3)
        verdict, reason = parse_output(task, raw)
        entry = {
            "id": task["id"],
            "verdict": verdict,
            "reason": reason,
            "raw_output": raw,
            "latency_s": latency,
        }
        results["tasks"].append(entry)
        print("%s -> %s" % (task["id"], verdict))

    out_dir = os.path.dirname(os.path.abspath(args.out))
    os.makedirs(out_dir, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("Wrote %s" % args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
