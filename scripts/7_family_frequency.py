from pathlib import Path
import pandas as pd

# Input and output
input_file = Path("results/gene_presence_absence.csv")
output_file = Path("results/family_frequency.csv")

# Read presence/absence matrix
df = pd.read_csv(input_file, index_col=0)

# Number of genomes containing each family
frequency = df.sum(axis=0)

# Count how many families occur in 1, 2, ..., 11 genomes
distribution = (
    frequency.value_counts()
    .sort_index()
    .rename_axis("genomes_present")
    .reset_index(name="number_of_families")
)

# Save distribution
distribution.to_csv(output_file, index=False)

print("Family frequency analysis complete!")
print(f"Total families: {len(frequency)}")
print(f"Saved to: {output_file}")

print("\nFamily frequency distribution:\n")
print(distribution.to_string(index=False))