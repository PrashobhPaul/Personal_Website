---
title: Pachaka Lokam · *meal planner*
domain: Household · Pantry-Aware
status: Live
tech: [PWA, TWA / Bubblewrap, GitHub Pages, Play Store]
hook: Kerala-style household meal planning PWA with pantry-aware suggestions, weekly templates with smart substitution, and maid/milk delivery tracking. Shipped to the Play Store via TWA. Real users, real edge cases.
---

# Pachaka Lokam

A meal-planning PWA built for Kerala-style household constraints. Three things that made it useful enough that family members use it without prompting:

1. **Pantry-aware suggestions.** Suggests meals based on what you actually have, not generic recipe lists.
2. **Weekly templates with substitution.** A repeating weekly plan, but smart about substituting individual items based on availability and recent meal history.
3. **Delivery tracking.** Maid attendance, milk delivery, ad-hoc deliveries — the boring household telemetry that keeps weeks running.

## Why this is a lab

It's a study in shipping useful software with no backend. Pure PWA. No server. State stays in the browser, exported / imported as JSON if needed. The constraint is liberating — it forces every feature to be possible within the bounds of "what one device can do well."

Shipped to the Play Store as a TWA via Bubblewrap. Domain: pachakalokam.prashobhpaul.com.
