from pathlib import Path
import pandas as pd
from Bio import SeqIO

family_file = Path("results/single_copy_core_families.csv")
cluster_file = Path("results/mmseqs/ecoli_clusters_cluster.tsv")
data_dir = Path("raw_data/ecoli_dataset/ncbi_dataset/data")

output_file = Path("sequences/single_copy_core_proteins.faa")
output_file.parent.mkdir(parents=True, exist_ok=True)

# -----------------------------
# 1. Read single-copy core IDs
# -----------------------------
core_families = set(
    pd.read_csv(family_file)["cluster"].astype(str)
)

# -----------------------------
# 2. Read MMseqs cluster mapping
# -----------------------------
clusters = pd.read_csv(
    cluster_file,
    sep="\t",
    header=None,
    names=["cluster", "protein"]
)

# Keep only single-copy core families
core_members = clusters[
    clusters["cluster"].isin(core_families)
].copy()

# -----------------------------
# 3. Create protein lookup
# -----------------------------
protein_sequences = {}

for protein_file in sorted(data_dir.rglob("protein.faa")):
    genome = protein_file.parent.name

    for record in SeqIO.parse(protein_file, "fasta"):
        key = f"{genome}|{record.id}"
        protein_sequences[key] = record.seq

# -----------------------------
# 4. Extract all core members
# -----------------------------
records = []
missing = 0

for _, row in core_members.iterrows():

    cluster = row["cluster"]
    protein = row["protein"]

    if protein in protein_sequences:
        from Bio.Seq import Seq
        from Bio.SeqRecord import SeqRecord

        record = SeqRecord(
            protein_sequences[protein],
            id=f"{cluster}|{protein}",
            description=""
        )

        records.append(record)

    else:
        missing += 1

# -----------------------------
# 5. Save
# -----------------------------
SeqIO.write(records, output_file, "fasta")

print("Corrected core sequence extraction complete!")
print(f"Core families: {len(core_families)}")
print(f"Core family members found: {len(records)}")
print(f"Expected sequences: {len(core_families) * 11}")
print(f"Missing sequences: {missing}")
print(f"Saved to: {output_file}")