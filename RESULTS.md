# micro1 Baseline Results (Nov 5, 2026)

Runner: build/run_eval.py at temperature 0, system prompt = the auditor
prompt in run_eval.py (SYSTEM_PROMPT). Key: John's OpenRouter free key
(transient, not stored). Transport fixes applied Nov 5: requests-library
transport preferred (urllib signature intermittently edge-blocked),
retry-with-backoff on transient statuses, standard browser user-agent.

## Live free-tier results (results/live-*.score.json)

- nvidia/nemotron-3-ultra-550b-a55b:free — **10.0/10.0 verdicts**,
  reason-hit 10/11 (0.909). Every task correct including T4 split, T8, T10.
- nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free — **10.0/10.0
  verdicts**, reason-hit 8/11 (0.727). Right verdicts on T2 and T5
  without anchor-term reasons (verdict-reason divergence worth citing).
- google/gemma-4-31b-it:free and google/gemma-4-26b-a4b-it:free —
  NO RESULT: Google upstream rate-limited the free endpoints (429
  through all retries). Retry later.

## Honest read

The two strongest free models passed every verdict. Candidate causes:
(1) the runner's SYSTEM_PROMPT coaches exactly the checks the traps test
("Check dates, scope, population coverage, and whether the artifact
actually matches the criterion") — a thumb on the scale; (2) both NVIDIA
models are large/reasoning-tuned and genuinely careful at temp 0;
(3) traps are single-defect and findable on a careful full read.

As-is, the package does not yet demonstrate "meaningful frontier
failures" (a scored judging criterion). Levers, in information order:
1. Rerun with a NEUTRAL system prompt (free, isolates the coaching
   effect; defensible because the eval should test the model, not the
   coaching).
2. Harden traps (compound defects, plausible distractor artifacts).
3. Reframe around reason-quality gaps (Nano's 3 right-verdict/wrong-
   reason units) plus the frontier run (Nov 7 decision, paid).

## Neutral-prompt rerun (Nov 5, 2026, ~12:29 PM ET)

Same runner, --prompt-variant neutral (role + format only, no checklist
of what to check). Results (results/neutral-*.score.json):

- nemotron-3-ultra: **10.0/10.0 verdicts, reason-hit 11/11** — BETTER
  reasons than under the auditor prompt (10/11).
- nemotron-3-nano-reasoning: **10.0/10.0 verdicts, reason-hit 8/11** —
  identical to its auditor-prompt run.

Conclusion: the coaching hypothesis is dead. The system prompt was not
the thumb on the scale; both NVIDIA models genuinely pass these tasks
on a careful read. The eval needs harder traps and/or true frontier
models to demonstrate failures.

## v2 results (Nov 5, 2026)

v2 = 12 tasks / 13 units (T11 Type I-for-Type II trap, T12 compound
change trap, distractors added to T2 and T6). Mocks: all-correct
12.0/12.0 (reasons 13/13); naive 2.5/12.0 (20.8%); reject-all cap
9.5/12.0.

- **DeepSeek V4.1 Flash Slow (via Freebuff chat UI, no system prompt,
  Nov 5, 12:35-1:04 PM ET): 12.0/12.0 verdicts, reason-hit 12/13.**
  Caught T11 with textbook Type I reasoning and T12's primary defect
  (CHG-5102 deployed before approval) plus the secondary self-approval
  on CHG-5105 unprompted. Raw answers in
  results/v2-deepseek-freebuff.json. Freebuff daily hours still showed
  21/21 after the session (no per-session meter visible).

Pattern across all live runs: strong reasoning models pass nearly every trap, including the hardened v2 traps. The eval currently discriminates careless acceptance (naive 20.8%) from careful reading, with reason quality as the gradient. The first genuine verdict failure by a strong model arrived in the Nov 8 v2 reruns: Nemotron Nano accepted the T6 carve-out evidence as Sufficient under the auditor prompt (see below).

## Muse Spark 1.3 via Meta API (Nov 5, 2026, eval lane)

Run through the gated credit runner (run_spark_eval.py), standard
tier, temperature 0. Eval lane spend after all Spark runs: $0.3259 of
the $35 cap; credits remaining $149.28.

**Run A (max_tokens 1500, the runner default):**
- Auditor prompt: 9.0/12.0, reasons 10/13. T4 and T10 returned EMPTY
  completions from the API (no content); T8 failed (see below).
- Neutral prompt: 11.0/12.0, reasons 12/13. Only T8 failed.

**T8 artifact fix:** Spark rejected the clean T8 pass under both
prompts because the sampled login events named amara.osei@ and
marcus.webb@, who are NOT in the 41-user roster (Amara Fuentes,
Marcus Marsh). A genuine inconsistency in our artifact; the other
models ignored it. Fixed Nov 5 (sampled events now use roster names;
PROMPTS.md regenerated to match). Spark's T8 objection is recorded
as an over-strict-but-grounded rejection of the pre-fix artifact.

**Run B (max_tokens 4000, post-fix T8):**
- Auditor: **12.0/12.0, reasons 12/13.** Neutral: **12.0/12.0,
  reasons 13/13.** Zero empty completions in 24 calls.

Decomposition of Run A: its failures were (1) a measurement-budget
artifact — a reasoning model at a 1,500-token completion cap
intermittently returns empty content on long prompts (5 empties in
28 calls at 1500; 0 in 24 at 4000), and (2) our own artifact nit.
With an adequate budget, Spark passes v2 completely. The
empty-completion behavior is itself a reportable finding about
running reasoning models through completion-capped pipelines.

## Free-tier quota fact (learned Nov 5)

OpenRouter free tier = 50 free-model requests/day for this account
(X-RateLimit-Limit: 50). The failed Nov 5 batches burned the day's
quota; the last Gemma attempt died on "free-models-per-day" (429),
separate from Google's upstream limit seen earlier. Quota resets
00:00 UTC (7:00 PM ET). Adding 10 credits raises the cap to 1000/day.

## Nemotron v2 reruns (Nov 8, 2026, ~00:00-00:10 AM ET, OpenRouter free tier, key micro1-eval-2)

Full 12-task v2 set, both prompt variants, temperature 0. Gemma pair failed on both variants (Google upstream 429, rate-limited on their side — not the key, not account quota; a morning retry remains optional).

- **Nemotron Ultra 550B: 12.0/12.0 auditor (reason-hit 13/13), 12.0/12.0 neutral (12/13).** First model to sweep v2 with perfect reason-hits under the auditor prompt.
- **Nemotron Nano Reasoning: 11.0/12.0 auditor (reason-hit 10/13), 12.0/12.0 neutral (12/13).** The auditor-prompt miss is T6: Nano accepted the vendor carve-out evidence as Sufficient — the first genuine verdict failure by a strong model on any live run. The v2 T6 hardening (mid-paragraph carve-out + ISO distractor) is what caught it.

## Submission package status (Nov 8, morning)

- Walkthrough video: https://youtu.be/KXrl8se0Djk (4:09), link in build/Q2-DRAFT.md.
- Zip: micro1-submission.zip, rebuilt after the matrix runs.
- Q2 draft complete; final Submit on HackerRank locks the test link permanently — only on John's explicit go, with his acceptance of the Participant Agreement.
