import json
import pandas as pd

input_file = "data/ecoli_genomes.jsonl"
output_file = "data/ecoli_metadata.csv"

records = []

with open(input_file, "r") as file:
    for line in file:
        if line.strip():
            records.append(json.loads(line))

rows = []

for record in records:

    assembly_info = record.get("assembly_info", {})
    assembly_stats = record.get("assembly_stats", {})
    organism = record.get("organism", {})
    annotation = record.get("annotation_info", {})
    gene_counts = annotation.get("stats", {}).get("gene_counts", {})

    rows.append({
        "accession": record.get("accession"),
        "organism": organism.get("organism_name"),
        "strain": organism.get("infraspecific_names", {}).get("strain"),
        "assembly_level": assembly_info.get("assembly_level"),
        "assembly_name": assembly_info.get("assembly_name"),
        "genome_size": assembly_stats.get("total_sequence_length"),
        "gc_percent": assembly_stats.get("gc_percent"),
        "contigs": assembly_stats.get("number_of_contigs"),
        "protein_coding_genes": gene_counts.get("protein_coding"),
        "pseudogenes": gene_counts.get("pseudogene")
    })

df = pd.DataFrame(rows)

print("\nE. coli genome metadata:\n")
print(df.to_string(index=False))

df.to_csv(output_file, index=False)

print(f"\nSaved to: {output_file}")
print(f"Total genomes: {len(df)}")