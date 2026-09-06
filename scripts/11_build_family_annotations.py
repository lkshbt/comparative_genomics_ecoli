from pathlib import Path
import pandas as pd

cluster_file = Path("results/mmseqs/ecoli_clusters_cluster.tsv")
annotation_file = Path("results/protein_annotations.csv")
output_file = Path("results/family_annotations.csv")

# Read MMseqs2 cluster assignments
clusters = pd.read_csv(
    cluster_file,
    sep="\t",
    header=None,
    names=["cluster", "protein"]
)

# Read NCBI annotations
annotations = pd.read_csv(annotation_file)

# Add genome from protein key
clusters["genome"] = clusters["protein"].str.split("|").str[0]

# Merge cluster information with annotations
merged = clusters.merge(
    annotations,
    left_on="protein",
    right_on="protein_key",
    how="left"
)

# Remove duplicate genome/protein information from the merge
merged = merged[
    [
        "cluster",
        "protein",
        "genome_x",
        "protein_id",
        "gene",
        "locus_tag",
        "product",
        "go_function",
        "ontology_term"
    ]
]

merged = merged.rename(columns={"genome_x": "genome"})

# Save
output_file.parent.mkdir(parents=True, exist_ok=True)
merged.to_csv(output_file, index=False)

print("Family annotation table created!")
print(f"Rows: {len(merged)}")
print(f"Families: {merged['cluster'].nunique()}")
print(f"Genomes: {merged['genome'].nunique()}")
print(f"Saved to: {output_file}")

print("\nPreview:\n")
print(merged.head(10).to_string(index=False))