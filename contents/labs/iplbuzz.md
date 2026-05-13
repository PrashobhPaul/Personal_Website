---
title: IPLBuzz · *match prediction* engine
domain: Sports Analytics · Rule-Based
status: Live
tech: [React, Stats Engine, NLG, Firebase, Cloudflare Worker]
hook: Production-grade rule-based statistical match prediction system with a multi-voice NLG narrative layer — no LLM in the prediction path by design. Built to study where rule-based engines still out-discipline LLMs.
---

# IPLBuzz

A working answer to the question: "what's the smallest, most disciplined prediction system you can build that beats the LLM-in-the-loop version on the failure modes that matter?"

## What's in the engine

- A statistical model of team-vs-team performance across recent IPL windows
- Player-form weighting with explicit decay
- Conditional adjustments for venue, toss outcome, and pitch type
- A confidence interval reported alongside every prediction

No LLM in the prediction path. That's deliberate. The prediction part is a deterministic problem, and treating it that way means I can reason about its failure modes in a way I cannot with an LLM-in-the-loop equivalent.

## Where the LLM lives

The LLM lives in the **narrative** layer. The same statistical output can be rendered as commentary in three different voices — a stat-heavy analyst voice, a fan voice, a contrarian voice. That's an interesting application for LLMs: stable input, varied stylistic output, with no consequence to getting the style "wrong."

## What this lab is for

It's a study in topology. Where does the LLM belong, and where does it not? IPLBuzz is the version where it belongs *after* the deterministic core, not inside it.
