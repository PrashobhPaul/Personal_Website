---
title: ProfitPilot *v3* · NSE analysis pipeline
domain: Capital Markets · ML
status: Live
tech: [Python, FinBERT, CANSLIM, PWA, GitHub Actions]
hook: Backtest-gated picks pipeline with FinBERT sentiment, CANSLIM fundamentals, and a 20+ indicator rules engine. Deployed as a PWA. The lab where I work out how to keep an ML pipeline honest about its own failure modes.
---

# ProfitPilot v3

The third iteration of an NSE-focused analysis stack. Three things make this version different from v1 and v2:

1. **The backtest gate.** No pick ships unless it would have shipped, profitably, in the backtest window. This is non-negotiable and it's eliminated about 70% of the signals the earlier rules engine would have published.
2. **FinBERT for sentiment.** Replaces a much simpler bag-of-words sentiment score. Worth the latency. The earlier version was particularly weak on industry-specific phrasing.
3. **CANSLIM-style fundamentals.** Bolted on next to the technical indicators. Helped filter out signals that were technically clean but fundamentally questionable.

## What this lab is actually for

It's the testbed for "predictable wrongness." The system has known failure modes — it under-fires in low-volatility regimes, it over-fires in earnings season — and those failure modes are stable enough that I can build around them. That's a more useful property than higher average accuracy.

## What it's not

Not an investment platform. Not advice. The repo is open because the patterns are useful, not because the picks should be acted on.
