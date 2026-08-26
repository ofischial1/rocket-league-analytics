"""
Phase 3: clean the collected dataset and produce initial exploratory plots.

Run this after collect_dataset.py has finished and dataset.csv exists.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

# --- Load ---
df = pd.read_csv("dataset.csv")
print(f"Loaded {len(df)} rows.\n")

# --- Cleaning ---
critical_cols = ["won", "avg_boost", "shots", "goals"]
before = len(df)
df = df.dropna(subset=critical_cols)
print(f"Dropped {before - len(df)} rows missing critical fields.")

before = len(df)
df = df.drop_duplicates(subset=["replay_id", "team_color"])
print(f"Dropped {before - len(df)} duplicate rows.")

# Report null rates per column so you know what's usable
print("\nNull rate per column:")
print((df.isnull().mean() * 100).round(1).sort_values(ascending=False))

# Make rank_tier ordinal so it plots/sorts in a sensible order
rank_order = [
    "gold-1", "platinum-1", "diamond-1",
    "champion-1", "grand-champion-1", "supersonic-legend",
]
df["rank_tier"] = pd.Categorical(df["rank_tier"], categories=rank_order, ordered=True)

# Sanity check win balance
print("\nWin/loss balance:")
print(df["won"].value_counts())

df.to_csv("dataset_clean.csv", index=False)
print("\nSaved cleaned dataset to dataset_clean.csv\n")

# --- Exploratory plots ---
features = ["avg_boost", "time_zero_boost", "demos_inflicted", "shooting_pct"]

for feature in features:
    plt.figure(figsize=(6, 4))
    sns.boxplot(data=df, x="won", y=feature)
    plt.title(f"{feature} by win/loss")
    plt.xlabel("Won (0 = No, 1 = Yes)")
    plt.tight_layout()
    plt.savefig(f"plot_{feature}_by_win.png")
    plt.close()
    print(f"Saved plot_{feature}_by_win.png")

# Same features, faceted by rank tier
for feature in features:
    plt.figure(figsize=(10, 5))
    sns.boxplot(data=df, x="rank_tier", y=feature, hue="won")
    plt.title(f"{feature} by rank tier and win/loss")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(f"plot_{feature}_by_rank.png")
    plt.close()
    print(f"Saved plot_{feature}_by_rank.png")

# Correlation heatmap
numeric_cols = ["avg_boost", "time_zero_boost", "time_offensive_third",
                 "time_defensive_third", "demos_inflicted", "demos_taken",
                 "shots", "goals", "shooting_pct", "won"]
corr = df[numeric_cols].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0)
plt.title("Feature correlation heatmap")
plt.tight_layout()
plt.savefig("plot_correlation_heatmap.png")
plt.close()
print("Saved plot_correlation_heatmap.png")

print("\nDone. Open the PNG files to review your first round of findings.")
