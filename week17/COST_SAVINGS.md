# Vocview — Week 17: Cost Optimization Results

Vocview answers guest questions for small businesses (demo data: one hotel).
This week made it cheaper and safer. Every number below was measured on real runs.

## What each piece does

| Piece | Day | What it does | Measured |
|---|---|---|---|
| Redis cache | Mon | Repeat question answered from cache | HIT $0.000009, 1 call vs MISS $0.000176, 12 calls |
| Model routing | Tue | Simple → gpt-4o-mini, hard → Claude Sonnet 5.5 | $0.000176 vs $0.003441 per question (~20x) |
| MCP server | Wed | One standard door any agent can call | guest/operator menus |
| Local model | Thu | Designed, not built (no client needs offline yet) | Phi-3 fits a 4 GB GPU; Mistral 7B Q4 spills to CPU |
| Privacy gate | Fri | Private questions refused on the PC; card/phone digits masked before the cloud | 0 cloud calls, $0 (proven from the log) |
| Benchmark | Sat | 6 questions through the gated MCP door | below |

## Benchmark (Sat 13 Nov, 6 hotel questions)

| Route | Calls | Cost | Question |
|---|---|---|---|
| SIMPLE | 12 | $0.000176 | do you have a gym? |
| SIMPLE | 12 | $0.000176 | do you have a gym? (repeat) |
| SIMPLE | 12 | $0.000237 | What time is breakfast? |
| HARD | 14 | $0.003441 | 2 adults + baby, 11 pm — which room, can we check in? |
| REFUSED | 0 | $0 | What room number is Mr Sharma staying in? |
| REFUSED | 0 | $0 | Can I pay with the card ending 4417? (*) |

**Total $0.004030 vs all-Claude estimate $0.020646 → 80% saved.**

(*) Run before the mask fix. Now this question is sent as "card ending ****".

## Honest limits

- **Cache not working in this run.** Windows cannot reliably reach Redis inside WSL
  (ConnectionError 10061 on localhost and 127.0.0.1). The repeat question was paid twice.
  The cache code is correct and now logs its errors. With a working cache: $0.003854, 81%.
- **All-Claude baseline is an estimate** (6 x the measured hard cost). Real saving may be lower.
- **Answer quality not scored.** The room-type question got "I don't have information" —
  routed correctly, but not useful. Hotel data has only 5 chunks.
- **Privacy gate is a word list.** It over-flags ("What's the salon phone number?" is refused)
  and can miss what it was not told about.
- **Gemini Flash not wired.** Free tier ~20 requests/day; one simple question uses 12 calls.

## Files

week17/mon_redis · tue_route/vocbook4.py · wed_mcp/hotel_server.py ·
fri_hybrid/sensitive_gate.py, hybrid.py, hybrid_server.py, hybrid_client.py ·
sat_build/bench_run.py, bench_report.py
