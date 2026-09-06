import pandas as pd

input_file = "results/functional_analysis.csv"
output_file = "results/functional_summary.csv"

df = pd.read_csv(input_file)

# Remove rows without a functional annotation
df = df.dropna(subset=["go_function"])

# Split multiple GO functions
df["go_function"] = df["go_function"].astype(str)

rows = []

for _, row in df.iterrows():
    functions = row["go_function"].split("|")

    for function in functions:
        function = function.strip()

        if function:
            rows.append({
                "family_type": row["family_type"],
                "go_function": function
            })

summary = pd.DataFrame(rows)

# Count unique families for each function
summary = (
    summary
    .drop_duplicates()
    .groupby(["family_type", "go_function"])
    .size()
    .reset_index(name="family_count")
    .sort_values(
        ["family_type", "family_count"],
        ascending=[True, False]
    )
)

summary.to_csv(output_file, index=False)

print("Functional summary complete!")
print(f"Total functional associations: {len(summary)}")
print(f"Saved to: {output_file}")

print("\nTop functions by family type:")

for category in ["Core", "Accessory", "Singleton"]:
    print(f"\n--- {category} ---")
    print(
        summary[summary["family_type"] == category]
        .head(10)
        .to_string(index=False)
    )