# What Actually Predicts Winning in Rocket League? A Data-Driven Look at Ranked Matches

*A statistical analysis of ranked 3v3 matches, pulled via the ballchasing.com API, examining which in-game behaviors actually correlate with winning.*

## Introduction

Rocket League has no shortage of playstyle debates — is boost management more important than positioning? Do aggressive plays like demolitions actually win games, or are they just satisfying highlight-reel moments? Rather than relying on intuition or community folklore, I pulled real match data across multiple rank tiers to test some of these assumptions directly.

This project set out to answer: **which team-level statistics actually correlate with winning, and does that relationship hold consistently across skill levels?**

## Data & Methodology

- **Source**: [ballchasing.com](https://ballchasing.com) API, which hosts community-uploaded Rocket League replay data with full team and player statistics.
- **Scope**: Ranked 3v3 standard replays, sampled across six rank tiers (Gold, Platinum, Diamond, Champion, Grand Champion, Supersonic Legend) to check whether patterns generalize across skill levels or are rank-specific.
- **Unit of analysis**: one row per team per match (two rows per replay), including boost usage, field positioning, demolitions, shot volume, and shooting accuracy.
- **Tools**: Python (requests, pandas) for collection and cleaning; matplotlib/seaborn for visualization; scipy for statistical testing.
- Full code and raw data pipeline are available in the [GitHub repo](https://github.com/ofischial1/rocket-league-analytics).

## Findings

To keep the comparisons consistent, every relationship below is reported as a Pearson correlation (r) against whether the team won, along with a p-value indicating whether the result is likely to be real rather than random noise (the conventional threshold is p < 0.05).

### Offensive Output: The Baseline, As Expected

As an internal check on the dataset and methodology, `goals` showed by far the strongest correlation with winning of any metric tested (r = 0.642, p < 0.0001) — unsurprising, since scoring more goals is close to a direct component of winning a match rather than an independent predictor. Shot volume (r = 0.386) and shooting accuracy (r = 0.389) showed similar, moderate positive relationships, confirming that offensive output remains the dominant factor in match outcomes even relative to positioning, boost management, or aggression-based statistics like demolitions. That this "obvious" relationship came through cleanly is a good sign the rest of the pipeline is sound.

[Insert plot: plots/plot_shooting_pct_by_win.png]

### Positioning: The Strongest Non-Obvious Predictor

Positioning showed the clearest relationship with winning of any metric tested that isn't a direct scoring statistic. Time spent in the offensive third correlated positively with winning (r = 0.182, p < 0.0001) — roughly three times the effect size seen for boost management or demolitions. Time in the defensive third showed a smaller, negative relationship (r = -0.083, p = 0.004), consistent with the same underlying pattern: winning teams spend proportionally more of the match applying offensive pressure rather than defending. While still a modest effect in absolute terms, it stands out as the most consistent predictor among the non-scoring stats examined here.

[Insert plot: plots/plot_time_offensive_third_by_win.png]

### Boost Management: Statistically Detectable, Practically Negligible

Boost management showed no practically meaningful relationship with winning. Average boost held was nearly identical between winning and losing teams (r = 0.061); while this reached statistical significance due to the large sample size, an effect this small — well below the threshold typically considered even a "small" effect — has little practical importance. Time spent at zero boost showed no relationship at all (r = -0.010, not significant). This suggests that *how much* boost a team holds on average may simply be too coarse a signal — the *timing* of boost usage (having boost available at the moment it's needed) likely matters more than the raw average, which this analysis doesn't capture.

[Insert plot: plots/plot_avg_boost_by_win.png]

### Demolitions: Testing (and Complicating) the Obvious Hypothesis

My original hypothesis was straightforward: teams that demolish opponents more often should win more often, since demos disrupt rotations and create scoring windows.

The data didn't support this — at least not simply. Across the full dataset, `demos_inflicted` showed no meaningful correlation with winning, and breaking the correlation out by rank tier didn't reveal a hidden pattern either; the relationship stayed weak and inconsistent across skill levels.

However, digging one level deeper surfaced a real nuance. When isolating teams with below-median shooting percentage (n=508), a small but statistically significant positive correlation emerged between demos inflicted and winning (r = 0.112, p < 0.05). In other words: for teams that aren't converting shots efficiently, doing more demos is weakly associated with winning more often — suggesting demolitions may act as a secondary path to disruption when a team can't win through clean shot conversion alone.

This effect is modest — demos_inflicted explains only about 1% of the variance in match outcome (r²) within that subgroup — so it should be read as a minor contributing factor, not a primary driver of wins. It's also worth flagging that this result emerged from testing several subgroups, which increases the chance of a false positive (the multiple comparisons problem); I'd treat this as a promising lead rather than a settled fact without further validation on an independent sample.

[Insert plot: plots/plot_demos_corr_by_rank.png and plots/plot_demos_shooting_interaction.png]

## Limitations

- **Uploader bias**: ballchasing.com relies on community uploads, which likely skew toward more competitive or engaged players rather than a truly random sample of all ranked matches.
- **Multiple comparisons**: several subgroup and per-rank tests were run in this analysis; the demos/shooting-percentage finding in particular should be treated as suggestive rather than confirmed without a larger, independent validation sample.
- **Correlation, not causation**: none of these findings establish that a behavior *causes* winning — e.g., more time in the offensive third could reflect good positioning, or simply reflect a team that's already ahead and playing more aggressively as a result.
- **Statistical vs. practical significance**: several relationships (avg_boost, time_defensive_third) were statistically significant but had small effect sizes — a distinction worth keeping in mind when interpreting any single p-value in isolation.

## Conclusion & Takeaways

Of everything tested, **offensive positioning was the strongest non-obvious predictor of winning**, outperforming boost management and demolitions by a wide margin. Teams and coaches looking to improve win rate through the levers examined here would get more value from emphasizing time spent applying offensive pressure than from boost discipline or aggressive demo-hunting. Demolitions, despite their appeal, are not a reliable primary strategy — but showed a modest, real association with winning specifically for teams struggling to convert shots, suggesting they may function as a secondary tool rather than a core strategy. Boost management, at least measured by simple averages, showed essentially no relationship with outcomes — a metric worth revisiting with more granular, timing-based data rather than being dismissed outright.

## What I'd Explore Next

- Incorporate possession and passing metrics if available, to get a fuller picture of playstyle beyond boost/positioning/demos.
- Validate the demos/shooting-percentage subgroup finding on an independent, larger sample.
- Extend the analysis with a logistic regression or random forest model to see which features matter most *jointly*, rather than one at a time — and to test whether boost timing (rather than average level) shows a relationship the current metrics miss.

---
*Full code, raw dataset, and analysis scripts: [GitHub repo](https://github.com/ofischial1/rocket-league-analytics)*
