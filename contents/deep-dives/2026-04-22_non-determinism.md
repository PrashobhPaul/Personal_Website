---
title: *Non-determinism* is the physics, not the bug
date: 2026-04-22
kicker: First Principles
readingTime: 10 min
tags: [evaluation, testing, llm]
hook: Stop treating LLM variance as a defect to engineer away. Treat it as the operating physics of the system and design test, observability, and governance around that.
---

# Variance is not the enemy

A predictable pattern in early agentic AI work: someone runs the same prompt twice, gets two different outputs, files a bug, and the team spends a week trying to make it deterministic.

It won't be.

LLMs are sampling-based by construction. Even with `temperature=0`, you'll see non-trivial variance from tokenizer changes, hardware non-determinism in floating-point, and provider-side model updates that ship under the same name.

The mistake isn't accepting variance. The mistake is **designing as if variance were a bug to fix** rather than the physics of the system.

## What changes when you accept it

Three things stop being "edge cases" and start being design parameters:

**Testing.** A test that asserts "output equals string X" is a hostile test of an LLM. The right tests assert *properties* (does it cite a source? is it on-topic? is the JSON valid?) over distributions of outputs, with statistical confidence bounds.

**Observability.** Logging the single output isn't enough. You need to capture intent, the resolved prompt, the model+version, and ideally a counterfactual ("what would the same prompt have produced with a different seed?"). This is what separates AI observability from APM.

**Governance.** Human review can't ask "is this output correct?" — it has to ask "is this output acceptable for this class of input under our policy?" That's a different question, and it changes who can answer it.

## The practical reframe

Stop trying to make agents deterministic. Start designing for **bounded non-determinism**: a system where the output set is constrained enough to be useful, but no one pretends the output is single-valued.

The teams that get this build better systems. The teams that don't spend forever chasing reproducibility on a stack that doesn't have it.
