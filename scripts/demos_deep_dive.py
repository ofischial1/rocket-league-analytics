"""
Step 1: dig deeper into the demos-vs-winning hypothesis before
concluding there's no relationship.

Checks (demos_inflicted only -- demos_taken is just the mirror
image of the opponent's demos_inflicted in a two-team match, so
it doesn't add independent information):
  1. Correlation of demos_inflicted with winning, pooled.
  2. Same correlation broken out by rank tier, to check whether
     a real effect is being averaged away in the pooled data.
  3. A simple interaction check: does demos_inflicted matter more
     when shooting_pct is also high (i.e. does the team capitalize
     on the advantage a demo creates)?
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

sns.set_style("whitegrid")

df = pd.read_csv("dataset_clean.csv")
print(f"Loaded {len(df)} cleaned rows.\n")

rank_order = [
    "gold-1", "platinum-1", "diamond-1",
    "champion-1", "grand-champion-1", "supersonic-legend",
]
df["rank_tier"] = pd.Categorical(df["rank_tier"], categories=rank_order, ordered=True)

# --- Check 1: demos_inflicted, pooled across all ranks ---
print("=== Pooled correlation with winning ===")
r, p = pearsonr(df["demos_inflicted"], df["won"])
sig = "significant (p < 0.05)" if p < 0.05 else "not significant"
print(f"  demos_inflicted: r = {r:.3f}, p = {p:.4f}  [{sig}]")

# --- Check 2: same, but broken out by rank tier ---
print("\n=== Correlation with winning, by rank tier ===")


def corr_with_p(group):
    r, p = pearsonr(group["demos_inflicted"], group["won"])
    return pd.Series({"corr_inflicted": r, "p_value": p, "n": len(group)})


by_rank = df.groupby("rank_tier", observed=True)[["demos_inflicted", "won"]] \
            .apply(corr_with_p)
by_rank["significant"] = by_rank["p_value"] < 0.05
print(by_rank)

# Plot it so the pattern (or lack of one) is easy to see at a glance
plt.figure(figsize=(9, 5))
by_rank_plot = by_rank[["corr_inflicted"]].reset_index()
sns.barplot(data=by_rank_plot, x="rank_tier", y="corr_inflicted")
plt.axhline(0, color="black", linewidth=0.8)
plt.title("Demos inflicted vs. winning correlation, by rank tier")
plt.ylabel("correlation")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("plot_demos_corr_by_rank.png")
plt.close()
print("\nSaved plot_demos_corr_by_rank.png")

# --- Check 3: does demos_inflicted only help when shooting_pct is also high? ---
# Split into high/low shooting_pct groups (above/below median) and compare
# the demos-vs-winning relationship within each group.
median_shooting = df["shooting_pct"].median()
df["shooting_group"] = df["shooting_pct"].apply(
    lambda x: "high_shooting" if x >= median_shooting else "low_shooting"
)

print("\n=== Demos_inflicted vs winning, split by shooting_pct group ===")
for group in ["low_shooting", "high_shooting"]:
    subset = df[df["shooting_group"] == group]
    r, p = pearsonr(subset["demos_inflicted"], subset["won"])
    sig = "significant" if p < 0.05 else "not significant"
    print(f"  {group} (n={len(subset)}): r = {r:.3f}, p = {p:.4f}  [{sig}]")

plt.figure(figsize=(6, 4))
sns.boxplot(data=df, x="shooting_group", y="demos_inflicted", hue="won")
plt.title("Demos inflicted by shooting group and win/loss")
plt.tight_layout()
plt.savefig("plot_demos_shooting_interaction.png")
plt.close()
print("Saved plot_demos_shooting_interaction.png")

print("\nDone. Review the printed correlations, p-values, and the two PNGs.")
print("Remember: statistical significance (low p-value) and practical")
print("significance (large |r|) are different things. With this sample")
print("size, small correlations can come back 'significant' but still be")
print("negligible in magnitude (|r| < 0.10) -- report both, not just p < 0.05.")
