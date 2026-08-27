"""
Generates the positioning boxplots that were missing from the
original explore_dataset.py feature list.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

sns.set_style("whitegrid")

df = pd.read_csv("data/dataset_clean.csv")

features = ["time_offensive_third", "time_defensive_third"]

for feature in features:
    # Numeric check first
    r, p = pearsonr(df[feature], df["won"])
    sig = "significant (p < 0.05)" if p < 0.05 else "not significant"
    print(f"{feature}: r = {r:.3f}, p = {p:.4f}  [{sig}]")

    # Plot
    plt.figure(figsize=(6, 4))
    sns.boxplot(data=df, x="won", y=feature)
    plt.title(f"{feature} by win/loss")
    plt.xlabel("Won (0 = No, 1 = Yes)")
    plt.tight_layout()
    plt.savefig(f"plots/plot_{feature}_by_win.png")
    plt.close()
    print(f"  Saved plots/plot_{feature}_by_win.png\n")
