---
title: Designing a *9-gate HITL topology* for governed agentic SDLC
date: 2026-05-12
kicker: Featured Deep Dive
featured: true
readingTime: 14 min
tags: [governance, agentic-sdlc, hitl]
hook: When agents write, review, and test code on your behalf, governance can't be a checklist at the end — it has to be a control plane. A walkthrough of the 5-agent + 9-gate reference architecture, file-based handshake contracts, gate composition, and what happens when an agent disagrees with itself.
---

# The shape of governed agentic SDLC

Most agentic SDLC stacks I see in the wild treat governance as the last thing to wire — a review queue bolted onto an otherwise autonomous pipeline. That works until it doesn't, which is usually the day a regulator asks "who approved this commit, and against which policy?"

The pattern that's actually held up across the engagements I've shipped is the opposite: governance as the **control plane**, with agents as managed actors inside it.

## Five agents, nine gates

The 5-agent topology splits the SDLC into roles that mirror what humans do anyway:

- **Feature Builder** — turns intent into a structured feature spec
- **Developer** — writes the code
- **Code Reviewer** — independent review pass against policy + craft
- **Test Engineer** — generates and runs tests, including adversarial ones
- **Documentation Writer** — produces the artifacts a regulator actually reads

Nine gates sit between these agents. Four are HITL — the gates that **must** stop unless a human signs — and five are policy gates that the system can clear on its own when policy says so, but cannot bypass when it doesn't.

## File-based handshake contracts

The single most important architectural decision is how agents pass state. In-memory orchestrators (LangGraph, CrewAI, etc.) make this invisible, which is great for prototyping and bad for audit. File-based handshakes — each agent reads from and writes to known artifact locations, with explicit schemas — give you three things for free:

1. **Replayability** — every state transition is on disk
2. **Auditability** — the trail is the artifact set, not a log
3. **Composability** — humans, other agents, and CI can all be participants

The cost is some throughput. The benefit is that "the gate fired correctly" becomes a file-system question, not a tracing question.

## When the system disagrees with itself

The interesting cases are when the Code Reviewer rejects what the Developer produced. The naive response is to retry the Developer. The better response is to file the disagreement as an artifact and let the next gate decide whether to escalate to a human, retry with a constraint, or accept the disagreement as a known-issue waiver.

This is where rule-based engines still out-discipline LLMs: disagreement routing is a deterministic problem, and treating it that way is what keeps the system honest.

## What this is not

This is not a framework you adopt off the shelf. It's a topology you instrument inside whichever orchestrator your stack already uses. The 9 gates aren't magic numbers — they're the smallest set that covers intent, code, review, test, and documentation with both policy and human checkpoints. In some engagements, the right number has been 7. In others, 11. The shape matters more than the count.
