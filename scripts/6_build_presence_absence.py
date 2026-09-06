from pathlib import Path
import pandas as pd

# Input/output files
cluster_file = Path("results/mmseqs/ecoli_clusters_cluster.tsv")
output_file = Path("results/gene_presence_absence.csv")

# Read MMseqs2 cluster assignments
df = pd.read_csv(
    cluster_file,
    sep="\t",
    header=None,
    names=["cluster", "protein"]
)

# Extract genome accession from protein ID
df["genome"] = df["protein"].str.split("|").str[0]

# Count each cluster only once per genome
presence = (
    df.assign(present=1)
      .drop_duplicates(["genome", "cluster"])
      .pivot_table(
          index="genome",
          columns="cluster",
          values="present",
          fill_value=0
      )
)

# Convert to integer 0/1 values
presence = presence.astype(int)

# Save matrix
output_file.parent.mkdir(parents=True, exist_ok=True)
presence.to_csv(output_file)

# Summary
print("Presence/absence matrix created!")
print(f"Genomes: {presence.shape[0]}")
print(f"Clusters: {presence.shape[1]}")
print(f"Saved to: {output_file}")

print("\nMatrix preview:\n")
print(presence.iloc[:, :10])