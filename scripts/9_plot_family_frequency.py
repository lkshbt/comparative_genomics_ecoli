from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

input_file = Path("results/family_frequency.csv")
output_file = Path("figures/family_frequency_distribution.png")

df = pd.read_csv(input_file)

plt.figure(figsize=(9, 6))

plt.bar(
    df["genomes_present"],
    df["number_of_families"]
)

plt.xlabel("Number of genomes containing protein family")
plt.ylabel("Number of protein families")
plt.title("E. coli Protein Family Frequency Distribution")

plt.xticks(range(1, 12))
plt.tight_layout()

output_file.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(output_file, dpi=300)
plt.show()

print(f"Figure saved to: {output_file}")