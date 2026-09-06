import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load enrichment results
df = pd.read_csv("results/pair_functional_enrichment.csv")

# Keep only statistically significant categories
sig = df[df["significant_FDR_0.05"] == True].copy()

# Plot
fig, ax = plt.subplots(figsize=(10, 6))

x = np.arange(len(sig))
width = 0.35

pairs = sig["pair"].unique()

for i, pair in enumerate(pairs):
    sub = sig[sig["pair"] == pair]
    positions = [
        j for j, idx in enumerate(sig.index)
        if idx in sub.index
    ]

    ax.bar(
        np.array(positions) + (i - (len(pairs)-1)/2) * width,
        sub["odds_ratio"],
        width,
        label=pair
    )

ax.set_ylabel("Odds ratio")
ax.set_xlabel("Enriched functional category")
ax.set_title(
    "Statistically Significant Functional Enrichment\n"
    "of Pair-Specific Gene Families"
)

ax.set_xticks(x)
ax.set_xticklabels(
    sig["category"],
    rotation=25,
    ha="right"
)

ax.axhline(
    1,
    linestyle="--",
    linewidth=1
)

ax.legend()
plt.tight_layout()

output = "figures/pair_functional_enrichment.png"

plt.savefig(
    output,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Significant categories:")
print(
    sig[
        [
            "pair",
            "category",
            "odds_ratio",
            "FDR"
        ]
    ].to_string(index=False)
)

print("\nSaved:")
print(output)

