import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# -----------------------------
# Load enrichment results
# -----------------------------
input_file = "results/pair_functional_enrichment.csv"
output_file = "figures/final_functional_findings.png"

df = pd.read_csv(input_file)

# Keep only statistically significant categories
sig = df[df["significant_FDR_0.05"] == True].copy()

# If no significant results, stop safely
if sig.empty:
    print("No statistically significant categories found.")
    raise SystemExit

# -----------------------------
# Plot
# -----------------------------
plt.figure(figsize=(10, 6))

bars = plt.bar(
    range(len(sig)),
    sig["odds_ratio"]
)

labels = [
    f"{row['pair']}\n{row['category']}"
    for _, row in sig.iterrows()
]

plt.xticks(
    range(len(sig)),
    labels,
    rotation=20,
    ha="right"
)

plt.ylabel("Odds ratio")
plt.xlabel("Enriched functional category")

plt.title(
    "Statistically Significant Functional Associations\n"
    "of Pair-Specific Gene Families"
)

# Reference line: odds ratio = 1
plt.axhline(
    y=1,
    linestyle="--",
    linewidth=1
)

# Add values above bars
for bar, value in zip(bars, sig["odds_ratio"]):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{value:.2f}",
        ha="center",
        va="bottom"
    )

plt.tight_layout()

# -----------------------------
# Save
# -----------------------------
Path("figures").mkdir(exist_ok=True)

plt.savefig(
    output_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Significant findings:")
print(
    sig[
        ["pair", "category", "odds_ratio", "FDR"]
    ].to_string(index=False)
)

print("\nSaved:")
print(output_file)
