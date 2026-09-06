from pathlib import Path
import subprocess

input_dir = Path("sequences/core_families")
output_dir = Path("results/alignments")

fasta_files = sorted(input_dir.glob("*.faa"))

print(f"Found {len(fasta_files)} family FASTA files")

for i, fasta in enumerate(fasta_files, start=1):

    output = output_dir / f"{fasta.stem}_aligned.faa"

    if output.exists():
        print(f"[{i}/{len(fasta_files)}] Already done: {fasta.name}")
        continue

    print(f"[{i}/{len(fasta_files)}] Aligning: {fasta.name}")

    with open(output, "w") as outfile:
        subprocess.run(
            [
                "mafft",
                "--auto",
                "--anysymbol", 
                "--thread",
                "4",
                str(fasta)
            ],
            stdout=outfile,
            check=True
        )

print("\nAll alignments completed!")

