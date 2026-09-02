# Listen to the Web — Security Note
Week 12 · 2 Sep 2026 · Vishnu Anil

## What this product does
Fetches a page written by a stranger, puts it in a prompt,
and reads the result aloud in an Indian language.
Indirect prompt injection is the NORMAL path, on every request.
The output is spoken — a listener has no URL bar and no view-source.

## Defences in place

| Layer | File | What it stops | Measured |
|---|---|---|---|
| URL check | urlcheck.py | localhost, 169.254.169.254, non-http | 5/5 |
| Strip | sanitize.py | zero-width chars hiding payloads | proven |
| Truncate | sanitize.py | oversized pages | LIMIT=5000 |
| Regex | sanitize.py | "ignore previous instructions" | 5/6 |
| Detector | detect2.py | payload buried in real text | 2/3 |
| Output schema | speak1.py | empty, >600 chars, "TOOL" | 3/3 |
| Permissions | perm2.py | tools the caller may not run | 4/4 |
| Rate limit | limit1.py | volume, per user per day | restart-proof |
| Audit log | limit2.py | no record of decisions | 4 rows |
| Monitoring | dash2.py | slowness nobody would notice | 19% slow |

## Known holes — unfixed

1. PARTIAL COMPROMISE. A correct summary that also advertises a
   competitor passes every check above. Demonstrated Wed, spoken aloud.
2. THE AUDIT LOG IS NOT IMMUTABLE. immutable1.py deleted a row with the
   app's own key. 4 rows to 3, no error. Row id 1 is still missing.
3. REGEX FALSE POSITIVES 1 in 10. Cannot ship as a hard block.
4. DETECTOR: n=1 verdicts, one model (gpt-4o-mini), never run twice on
   the same input, never met a sophisticated attack.
5. GEMINI SHIPS IN PRODUCTION AND HAS NEVER BEEN ATTACKED ONCE.
6. NO RLS, NO INDEX on daily_usage or audit_log. All-verbs key.
7. TEST ROWS AND REAL ROWS ARE INDISTINGUISHABLE. dash1.py counted
   ravi's Thursday test rows into today's refusal total.
8. EVERY THRESHOLD IS A CHOSEN CONSTANT, NEVER SWEPT:
   LIMIT=5000, 600 chars, CAPACITY=3, REFILL=1.0, DAILY_LIMIT=3,
   SLOW_MS=1000.
9. NOTHING ABOVE IS WIRED INTO THE PRODUCT. Every file runs standalone
   against hardcoded names. The pipeline is a drawing. Saturday.
10. NO REAL WEBSITE HAS EVER BEEN FETCHED. localhost only.

## Verdict
The product has defences against CONTENT, against VOLUME, and now a
RECORD and a MEASUREMENT. It has no defence against a compromise that
looks correct, and its record can be erased by its own key.
Not shippable to a paying business until items 1, 2 and 9 are closed.