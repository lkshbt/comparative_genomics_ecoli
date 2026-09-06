from pathlib import Path
from Bio import SeqIO

data_dir = Path("raw_data/ecoli_dataset/ncbi_dataset/data")
output_file = Path("sequences/all_ecoli_proteins.faa")

protein_files = sorted(data_dir.rglob("protein.faa"))

output_file.parent.mkdir(parents=True, exist_ok=True)

total = 0

with open(output_file, "w") as output:
    for protein_file in protein_files:
        genome = protein_file.parent.name

        for record in SeqIO.parse(protein_file, "fasta"):
            record.id = f"{genome}|{record.id}"
            record.description = ""
            SeqIO.write(record, output, "fasta")
            total += 1

print(f"Protein files: {len(protein_files)}")
print(f"Total proteins: {total}")
print(f"Saved to: {output_file}")