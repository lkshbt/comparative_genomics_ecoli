import pandas as pd

input_file = "results/family_frequency.csv"
output_file = "results/pangenome_summary.csv"

df = pd.read_csv(input_file)

total_families = df["number_of_families"].sum()

df["percentage"] = (
    df["number_of_families"] / total_families * 100
).round(2)

df.to_csv(output_file, index=False)

print("Pan-genome summary created!")
print(f"Total families: {total_families}")
print(f"Saved to: {output_file}")

print("\nSummary:\n")
print(df.to_string(index=False))