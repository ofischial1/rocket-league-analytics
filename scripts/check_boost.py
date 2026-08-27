"""
Confirms numerically what the boost boxplots show visually:
does avg_boost or time_zero_boost correlate with winning?
"""

import pandas as pd
from scipy.stats import pearsonr

df = pd.read_csv("data/dataset_clean.csv")
for col in ["shooting_pct", "shots", "goals"]:
    r, p = pearsonr(df[col], df["won"])
    sig = "significant (p < 0.05)" if p < 0.05 else "not significant"
    print(f"{col}: r = {r:.3f}, p = {p:.4f}  [{sig}]")
