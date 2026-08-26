# What Actually Predicts Winning in Rocket League? A Data-Driven Look at Ranked Matches

*A statistical analysis of ~[TOTAL REPLAY COUNT] ranked 3v3 matches, pulled via the ballchasing.com API, examining which in-game behaviors actually correlate with winning.*

## Introduction

Rocket League has no shortage of playstyle debates — is boost management more important than positioning? Do aggressive plays like demolitions actually win games, or are they just satisfying highlight-reel moments? Rather than relying on intuition or community folklore, I pulled real match data across multiple rank tiers to test some of these assumptions directly.

This project set out to answer: **which team-level statistics actually correlate with winning, and does that relationship hold consistently across skill levels?**

## Data & Methodology

- **Source**: [ballchasing.com](https://ballchasing.com) API, which hosts community-uploaded Rocket League replay data with full team and player statistics.
- **Scope**: [X] ranked 3v3 standard replays, sampled across six rank tiers (Gold, Platinum, Diamond, Champion, Grand Champion, Supersonic Legend) to check whether patterns generalize across skill levels or are rank-specific.
- **Unit of analysis**: one row per team per match (two rows per replay), including boost usage, field positioning, demolitions, shot volume, and shooting accuracy.
- **Tools**: Python (requests, pandas) for collection and cleaning; matplotlib/seaborn for visualization; scipy for statistical testing.
- Full code and raw data pipeline are available in [the GitHub repo link].

## Findings

### [PLACEHOLDER — Finding 1: e.g., Boost Management]
*Fill in with your boxplot observations: did avg_boost or time_zero_boost differ meaningfully between winners and losers? Was the pattern consistent across rank tiers, or did it change at higher ranks?*

[Insert plot: plot_avg_boost_by_win.png]

### [PLACEHOLDER — Finding 2: e.g., Positioning]
*Fill in with your findings on time_offensive_third / time_defensive_third.*

[Insert plot]

### [PLACEHOLDER — Finding 3: e.g., Shot Volume & Accuracy]
*Fill in — this one likely showed the strongest relationship with winning, worth confirming with your correlation heatmap.*

[Insert plot]

### Demolitions: Testing (and Complicating) the Obvious Hypothesis

My original hypothesis was straightforward: teams that demolish opponents more often should win more often, since demos disrupt rotations and create scoring windows.

The data didn't support this — at least not simply. Across the full dataset, `demos_inflicted` showed no meaningful correlation with winning ([pooled r value], not statistically significant). Breaking the correlation out by rank tier didn't reveal a hidden pattern either; the relationship stayed weak and inconsistent across skill levels.

However, digging one level deeper surfaced a real nuance. When isolating teams with below-median shooting percentage (n=508), a small but statistically significant positive correlation emerged between demos inflicted and winning (r = 0.112, p < 0.05). In other words: for teams that aren't converting shots efficiently, doing more demos is weakly associated with winning more often — suggesting demolitions may act as a secondary path to disruption when a team can't win through clean shot conversion alone.

This effect is modest — demos_inflicted explains only about 1% of the variance in match outcome (r²) within that subgroup — so it should be read as a minor contributing factor, not a primary driver of wins. It's also worth flagging that this result emerged from testing several subgroups, which increases the chance of a false positive (the multiple comparisons problem); I'd treat this as a promising lead rather than a settled fact without further validation on an independent sample.

[Insert plot: plot_demos_corr_by_rank.png and/or plot_demos_shooting_interaction.png]

## Limitations

- **Uploader bias**: ballchasing.com relies on community uploads, which likely skew toward more competitive or engaged players rather than a truly random sample of all ranked matches.
- **Sample size per rank tier**: [X] replays per tier is enough for team-level correlation analysis but limits how confidently rank-specific subgroup findings can be generalized.
- **Multiple comparisons**: several subgroup and per-rank tests were run in this analysis; the demos/shooting-percentage finding in particular should be treated as suggestive rather than confirmed without a larger, independent validation sample.
- **Correlation, not causation**: none of these findings establish that a behavior *causes* winning — e.g., low boost-at-zero time could reflect good boost management, or simply reflect a team that's already winning and playing more conservatively.

## Conclusion & Takeaways

[PLACEHOLDER — pull together your strongest 2-3 findings into concrete, coach-able takeaways. E.g.: "If [strongest finding] holds, teams and coaches optimizing for wins should prioritize X over Y. Demolitions, despite their appeal, are not a reliable primary strategy — but may offer marginal value specifically for teams struggling with shot conversion."]

## What I'd Explore Next

- Incorporate possession and passing metrics if available, to get a fuller picture of playstyle beyond boost/positioning/demos.
- Validate the demos/shooting-percentage subgroup finding on an independent, larger sample.
- Extend the analysis with a logistic regression / random forest model to see which features matter most *jointly*, rather than one at a time.

---
*Full code, raw dataset, and analysis scripts: [GitHub repo link]*
