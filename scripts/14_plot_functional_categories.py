import pandas as pd
import matplotlib.pyplot as plt

input_file = "results/functional_summary.csv"
output_file = "figures/functional_categories.png"

df = pd.read_csv(input_file)

# Keep the most frequent functions overall
top_functions = (
    df.groupby("go_function")["family_count"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .index
)

plot_df = df[df["go_function"].isin(top_functions)]

# Pivot for plotting
plot_df = plot_df.pivot_table(
    index="go_function",
    columns="family_type",
    values="family_count",
    fill_value=0
)

# Ensure consistent category order
for category in ["Core", "Accessory", "Singleton"]:
    if category not in plot_df.columns:
        plot_df[category] = 0

plot_df = plot_df[["Core", "Accessory", "Singleton"]]

# Plot
ax = plot_df.plot(kind="bar", figsize=(12, 7))

ax.set_title("Top Functional Categories in E. coli Pangenome")
ax.set_xlabel("GO Function / Functional Annotation")
ax.set_ylabel("Number of Protein Families")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

plt.savefig(output_file, dpi=300)
plt.close()

print("Functional category plot created!")
print(f"Saved to: {output_file}")