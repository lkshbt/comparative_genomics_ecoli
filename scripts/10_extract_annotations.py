from pathlib import Path
import pandas as pd


data_dir = Path("raw_data/ecoli_dataset/ncbi_dataset/data")
output_file = Path("results/protein_annotations.csv")


def parse_attributes(attribute_text):
    attributes = {}

    for item in attribute_text.strip().split(";"):
        if "=" in item:
            key, value = item.split("=", 1)
            attributes[key] = value

    return attributes


rows = []

gff_files = sorted(data_dir.rglob("genomic.gff"))

print(f"Found {len(gff_files)} GFF files\n")

for gff_file in gff_files:

    genome = gff_file.parent.name

    with open(gff_file, "r", encoding="utf-8") as file:

        for line in file:

            if line.startswith("#"):
                continue

            fields = line.rstrip("\n").split("\t")

            if len(fields) != 9:
                continue

            feature_type = fields[2]

            # We only need CDS annotations
            if feature_type != "CDS":
                continue

            attributes = parse_attributes(fields[8])

            protein_id = attributes.get("protein_id")

            if not protein_id:
                continue

            rows.append({
                "protein_key": f"{genome}|{protein_id}",
                "genome": genome,
                "protein_id": protein_id,
                "gene": attributes.get("gene"),
                "locus_tag": attributes.get("locus_tag"),
                "product": attributes.get("product"),
                "go_function": attributes.get("go_function"),
                "ontology_term": attributes.get("Ontology_term")
            })


df = pd.DataFrame(rows)

output_file.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_file, index=False)

print("Annotation extraction complete!")
print(f"Protein annotations: {len(df)}")
print(f"Genomes: {df['genome'].nunique()}")
print(f"Saved to: {output_file}")

print("\nPreview:\n")
print(df.head(10).to_string(index=False))