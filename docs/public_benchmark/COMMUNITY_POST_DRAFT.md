# Community Post Draft

I built FairEval, a release-gating system for LLMs.

Instead of only scoring outputs, it compares baseline vs candidate models, detects regressions, and produces a deployment decision (ship or block).

I’ve started packaging a public benchmark around instruction following, along with a regression case library documenting realistic failure modes that should block release.

Current package includes:
- benchmark dataset
- compare + gate workflow
- regression case library
- public benchmark documentation

I’d love feedback on:
- benchmark design
- regression case realism
- evaluation criteria for release decisions
