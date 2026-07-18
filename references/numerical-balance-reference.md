# Numerical Balance Reference

Use this reference when a game needs combat, card, hero, economy, progression, probability, difficulty, PvP, or live-balance work. It converts professional research and live-game practice into a repeatable operating loop for the Numerical Balance Agent.

## Role boundary

- **Game Designer** owns the desired player experience, rules, intended counterplay, and what trade-offs are acceptable.
- **System Designer** owns feature scope, the feature specification, data-source map, and acceptance alignment.
- **Numerical Balance Agent** owns quantitative diagnosis, balance targets, simulations, experiment design, evidence quality, and balance recommendations.
- **Data Config Specialist** owns the table/schema/validation implementation of approved tuning values.
- **QA Lead** owns reproducible tests and player-facing regression coverage.
- **Producer** decides scope, timing, and release authorization.

The Numerical Balance Agent recommends and proves; it does not silently replace game direction, monetization policy, or a producer decision.

## Balance operating loop

1. **State the intent.** Write the intended player experience and non-negotiable constraints. For example: "same-skill team matches should feel contestable, each role needs a visible counterplay path, and a normal match should end in the intended time window."
2. **Choose project-specific objectives.** Define fairness, strategy diversity, pace, economy health, progression pace, and difficulty objectives. Do not copy another game's thresholds.
3. **Create the metric dictionary.** For every metric, name its formula, denominator, time window, cohort, data owner, configuration version, minimum practical effect, and known bias.
4. **Build a baseline.** Segment results before judging them. PvP normally needs rank/skill uncertainty, mode, map, team/role, version, party state, first-player/spawn effects, and new-versus-mature content where relevant.
5. **Model and simulate.** Use production combat/rules where practical, deterministic seeds, a scenario matrix, and representative bot/player archetypes. Record seeds and config versions. Simulation screens hypotheses; it does not replace player testing.
6. **Run controlled human tests.** Use blinded or structured battletests across relevant skill bands. Capture both observed outcomes and player-perceived fairness, agency, clarity, and frustration.
7. **Propose the smallest reversible change.** Every proposal contains a causal hypothesis, target cohorts, primary metric, guardrails, expected effect, risks, rollout, stop rule, and rollback.
8. **Stage and monitor.** Use a control group or staged rollout. Report effect size and confidence interval alongside sample size and data quality. A `continue observing` conclusion is valid.
9. **Close the loop.** Publish the decision record, update the baseline, preserve regression scenarios, and document unintended effects for the next version.

## Required scorecards

### Competitive / meta

- Win rate adjusted by relevant skill and match conditions, plus uncertainty.
- Pick rate, ban rate or presence where the mode supports it, and minimum-sample status.
- Matchup matrix, dominated-strategy check, composition/synergy concentration, and counterplay availability.
- Match duration, surrender/quit/rematch rate, first-player/spawn-position split, and player feedback.
- New-content learning curve shown separately from mature-content behavior.

### Economy / progression

- Resource sources (faucets), sinks, stock/holdings, velocity, and inflation/deflation indicators.
- Time and attempts needed to reach the next meaningful goal by player cohort.
- Expected value, variance/tail risk, conversion ratios, and whether rewards bypass intended choices.
- Distributional impact: a change that is harmless at the median may be destructive for new, high-skill, or long-tenure players.

### Difficulty / PvE

- Success/failure distribution, time-to-complete, recovery chance, restart/quit rate, and perceived fairness.
- Clear adjustable knobs, adjustment cooldowns, and a guard against oscillation.
- No hidden dynamic-difficulty manipulation where it would compromise trust or competitive integrity.

## Evidence and statistical rules

- Do not equate statistical significance with practical importance. Report effect size, interval, sample size, cohort coverage, and practical threshold.
- Avoid comparing a live change to a different version, event, map pool, or player population without labeling the confounder.
- In team modes and other interference-heavy systems, randomize and estimate at the room/team level if players influence one another.
- Check sample-ratio mismatch, missing telemetry, bot contamination, version contamination, and multiple-comparison risk before acting on apparent outliers.
- Keep an explicit `observe` state for low-sample or high-uncertainty findings.

## Balance proposal template

```text
Balance question:
Design intent and invariant:
Hypothesis:
Affected mode/cohort/config version:
Baseline and segmentation:
Primary metric and minimum practical effect:
Guardrails:
Simulation/playtest evidence and confidence:
Smallest reversible parameter change:
Expected benefit and known trade-offs:
Experiment/randomization unit, rollout, and observation window:
Stop condition and rollback path:
Recommendation: ship / iterate / observe / roll back
```

## Learning sources

- [Volz, Rudolph, and Naujoks - Demonstrating the Feasibility of Automatic Game Balancing](https://arxiv.org/abs/1603.03795): balance is multi-objective; use simulations and confidence-aware trade-offs rather than a single score.
- [Hernandez et al. - Metagame Autobalancing for Competitive Multiplayer Games](https://arxiv.org/abs/2006.04419): target an intentional strategy/matchup graph, not forced identical global win rates.
- [Microsoft Research - TrueSkill](https://www.microsoft.com/en-us/research/publication/trueskilltm-a-bayesian-skill-rating-system-2/): compare competitive outcomes with skill uncertainty and team context rather than a flat global average.
- [Robin Hunicke - The Case for Dynamic Difficulty Adjustment in Games](https://doi.org/10.1145/1178477.1178573): dynamic difficulty must protect player experience and perceived fairness; directed analysis complements iterative playtesting.
- [Square Enix GDC - Balancing Nightmares: an AI Approach to Balance](https://media.gdcvault.com/gdc2019/presentations/Manabe_Kazuko_Balancing_Nightmares_an.pdf): high-throughput simulations should reuse real game logic, fixed seeds, and automated result capture.
- [Riot Games - Champion Balance Framework](https://www.leagueoflegends.com/en-us/news/dev/dev-champion-balance-framework/): judge live competitive content by multiple skill cohorts and presence, not only average win rate.
- [Riot Games - Balancing New Champions](https://www.leagueoflegends.com/en-us/news/dev/dev-balancing-new-champions/): separate learning curve from mature strength when evaluating new content.
- [Microsoft - Trustworthy Analysis of Online A/B Tests](https://www.microsoft.com/en-us/research/publication/trustworthy-analysis-of-online-a-b-tests-pitfalls-challenges-and-solutions/): align variance estimation with the randomization unit and guard against false conclusions.
- [American Statistical Association - Statement on Statistical Significance and P-Values](https://www.amstat.org/asa/files/pdfs/p-valuestatement.pdf): p-values alone do not measure effect size or decision value.
- [Dan Hart GDC - Balancing Your Game Economy](https://media.gdcvault.com/gdconline11/Dan_Hart_VirtualItemsSummit_BalancingYourGame.pdf): track sources, sinks, stock, and time-to-goal to control economic inflation.

Treat these as methods and evidence sources, not as numbers to copy into a project. Every threshold must be calibrated to the game's mode, audience, version, and player-experience goals.
