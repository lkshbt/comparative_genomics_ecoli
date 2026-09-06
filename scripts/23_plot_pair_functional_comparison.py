import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "results/pair_functional_comparison.csv"
)

plt.figure(figsize=(10, 6))

x = range(len(df))

plt.bar(
    [i - 0.2 for i in x],
    df["RM9387_CI5"],
    width=0.4,
    label="RM9387 + CI5"
)

plt.bar(
    [i + 0.2 for i in x],
    df["C41_BL21"],
    width=0.4,
    label="C41(DE3) + BL21"
)

plt.xticks(
    x,
    df["category"],
    rotation=35,
    ha="right"
)

plt.ylabel("Number of gene families")
plt.xlabel("Functional category")
plt.title(
    "Functional Comparison of Pair-Specific Gene Families"
)

plt.legend()
plt.tight_layout()

plt.savefig(
    "figures/pair_functional_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

print("Saved:")
print("figures/pair_functional_comparison.png")
