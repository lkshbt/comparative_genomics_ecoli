from pathlib import Path
from Bio import SeqIO

data_dir = Path("raw_data/ecoli_dataset/ncbi_dataset/data")

protein_files = sorted(data_dir.rglob("protein.faa"))

print(f"Found {len(protein_files)} protein files\n")

for protein_file in protein_files:
    records = list(SeqIO.parse(protein_file, "fasta"))

    lengths = [len(record.seq) for record in records]

    print(f"Genome: {protein_file.parent.name}")
    print(f"  Proteins: {len(records)}")
    print(f"  Average protein length: {sum(lengths)/len(lengths):.1f} aa")
    print(f"  Shortest protein: {min(lengths)} aa")
    print(f"  Longest protein: {max(lengths)} aa")
    print()