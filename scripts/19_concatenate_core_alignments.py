from pathlib import Path
from Bio import AlignIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Align import MultipleSeqAlignment


input_dir = Path("results/alignments")
output_dir = Path("results/phylogeny")
output_dir.mkdir(parents=True, exist_ok=True)

alignment_files = sorted(input_dir.glob("*_aligned.faa"))

if not alignment_files:
    raise FileNotFoundError("No alignment files found.")

print("Alignment files found:", len(alignment_files))


def get_genome_id(record_id):
    """
    Extract genome accession from IDs like:

    GCF_000597845.1|WP_00002541.1|GCF_000597845.1|WP_00002541.1
    """
    parts = record_id.split("|")

    if len(parts) < 3:
        raise ValueError(f"Unexpected sequence ID: {record_id}")

    return parts[2]


# Read first alignment
first = AlignIO.read(alignment_files[0], "fasta")

# Establish a fixed genome order
genomes = [get_genome_id(record.id) for record in first]

print("Genomes:", len(genomes))

if len(set(genomes)) != len(genomes):
    raise ValueError("Duplicate genome IDs found in first alignment.")


# Store concatenated sequences
concatenated = {genome: "" for genome in genomes}

# Store partition coordinates
partitions = []

current_start = 1


for i, file in enumerate(alignment_files, start=1):

    aln = AlignIO.read(file, "fasta")

    # Every family should contain 11 sequences
    if len(aln) != len(genomes):
        raise ValueError(
            f"{file.name}: expected {len(genomes)} sequences, "
            f"found {len(aln)}"
        )

    # Map each sequence to its genome
    records_by_genome = {}

    for record in aln:
        genome = get_genome_id(record.id)

        if genome in records_by_genome:
            raise ValueError(
                f"{file.name}: duplicate genome {genome}"
            )

        records_by_genome[genome] = record

    # Make sure this family contains exactly the same 11 genomes
    if set(records_by_genome.keys()) != set(genomes):
        missing = set(genomes) - set(records_by_genome.keys())
        extra = set(records_by_genome.keys()) - set(genomes)

        raise ValueError(
            f"{file.name}: genome set differs.\n"
            f"Missing: {missing}\n"
            f"Extra: {extra}"
        )

    # Alignment length
    length = aln.get_alignment_length()

    current_end = current_start + length - 1

    family_name = file.stem.replace("_aligned", "")

    partitions.append(
        (family_name, current_start, current_end)
    )

    # Add sequences in the fixed genome order
    for genome in genomes:
        concatenated[genome] += str(
            records_by_genome[genome].seq
        )

    current_start = current_end + 1

    if i % 100 == 0:
        print(f"Processed {i}/{len(alignment_files)} alignments")


# Create concatenated FASTA
records = []

for genome in genomes:
    records.append(
        SeqRecord(
            Seq(concatenated[genome]),
            id=genome,
            description=""
        )
    )


output_alignment = output_dir / "ecoli_core_concatenated.faa"

AlignIO.write(
    MultipleSeqAlignment(records),
    output_alignment,
    "fasta"
)


# Create partition file
partition_file = output_dir / "ecoli_core_partitions.txt"

with open(partition_file, "w") as f:
    for family, start, end in partitions:
        f.write(
            f"LG, {family} = {start}-{end}\n"
        )


# Final summary
total_length = len(records[0].seq)

print()
print("DONE")
print("Families:", len(partitions))
print("Genomes:", len(genomes))
print("Concatenated alignment length:", total_length)
print("Alignment:", output_alignment)
print("Partitions:", partition_file)
