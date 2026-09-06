from pathlib import Path
from Bio import SeqIO

input_file = Path("sequences/single_copy_core_proteins.faa")
output_dir = Path("sequences/core_families")

output_dir.mkdir(parents=True, exist_ok=True)

family_counts = {}

for record in SeqIO.parse(input_file, "fasta"):
    # Header format:
    # cluster|genome|protein
    family = "|".join(record.id.split("|")[:2])
    output_file = output_dir / f"{family}.faa"

    with open(output_file, "a") as handle:
        SeqIO.write(record, handle, "fasta")

    family_counts[family] = family_counts.get(family, 0) + 1

print("Family splitting complete!")
print(f"Families created: {len(family_counts)}")
print(f"Total sequences: {sum(family_counts.values())}")

print("\nSequence count distribution:")
from collections import Counter

distribution = Counter(family_counts.values())

for count, families in sorted(distribution.items()):
    print(f"{count} sequences/family: {families} families")