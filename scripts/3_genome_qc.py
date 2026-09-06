from pathlib import Path
from Bio import SeqIO

data_dir = Path("raw_data/ecoli_dataset/ncbi_dataset/data")

genome_files = sorted(
    f for f in data_dir.glob("*/*.fna") if f.name != "cds_from_genomic.fna"
)


print(f"Found {len(genome_files)} genome files\n")

for genome_file in genome_files:

    records = list(SeqIO.parse(genome_file, "fasta"))

    total_length = sum(len(record.seq) for record in records)

    gc_count = sum(
        record.seq.upper().count("G") + record.seq.upper().count("C")
        for record in records
    )

    gc_percent = (gc_count / total_length) * 100

    print(f"Genome: {genome_file.parent.name}")
    print(f"  Contigs: {len(records)}")
    print(f"  Genome size: {total_length:,} bp")
    print(f"  GC content: {gc_percent:.2f}%")
    print()