import pandas as pd
import matplotlib.pyplot as plt

input_file = "results/strain_functional_categories.csv"
output_file = "figures/strain_functional_heatmap.png"

df = pd.read_csv(input_file)

# Columns to visualize
categories = [
    "Hypothetical",
    "Phage_Mobile",
    "Regulation",
    "DNA_Defense",
    "Surface_Adhesion",
    "Carbohydrate",
    "Transport"
]

matrix = df.set_index("strain")[categories]

# Plot
fig, ax = plt.subplots(figsize=(12, 7))

im = ax.imshow(matrix.values, aspect="auto")

ax.set_xticks(range(len(categories)))
ax.set_xticklabels(
    [
        "Hypothetical",
        "Phage/Mobile",
        "Regulation",
        "DNA Defense",
        "Surface/Adhesion",
        "Carbohydrate",
        "Transport"
    ],
    rotation=45,
    ha="right"
)

ax.set_yticks(range(len(matrix.index)))
ax.set_yticklabels(matrix.index)

# Add values inside cells
for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        ax.text(
            j,
            i,
            str(matrix.iloc[i, j]),
            ha="center",
            va="center"
        )

ax.set_title(
    "Functional Categories of Strain-Specific Gene Families"
)

ax.set_xlabel("Functional category")
ax.set_ylabel("E. coli strain")

plt.tight_layout()

plt.savefig(output_file, dpi=300, bbox_inches="tight")
plt.close()

print("DONE")
print("Saved:", output_file)