import pandas as pd

input_file = "results/mmseqs/ecoli_clusters_cluster.tsv"
output_file = "results/single_copy_core_families.csv"

# Read MMseqs cluster assignments
df = pd.read_csv(
    input_file,
    sep="\t",
    header=None,
    names=["cluster", "protein"]
)

# Extract genome accession
df["genome"] = df["protein"].str.split("|").str[0]

# Count copies of each family in each genome
copy_counts = (
    df.groupby(["cluster", "genome"])
    .size()
    .unstack(fill_value=0)
)

# Single-copy core = exactly 1 copy in every genome
single_copy_core = copy_counts[
    copy_counts.eq(1).all(axis=1)
]

# Save family IDs
result = pd.DataFrame({
    "cluster": single_copy_core.index
})

result.to_csv(output_file, index=False)

print("Single-copy core extraction complete!")
print(f"Single-copy core families: {len(result)}")
print(f"Saved to: {output_file}")