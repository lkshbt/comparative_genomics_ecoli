from Bio import Phylo
import matplotlib.pyplot as plt
from pathlib import Path

tree_file = "results/phylogeny/ecoli_final_tree.treefile"
output_file = "figures/ecoli_phylogenetic_tree_strain_names.png"

# Accession -> strain name
strain_names = {
    "GCF_000801185.2": "94-3024",
    "GCF_000833145.1": "BL21_TaKaRa",
    "GCF_000830035.1": "C41_DE3",
    "GCF_000971615.1": "CI5",
    "GCF_000953515.1": "K12_HMS174",
    "GCF_000952955.1": "K12_RV308",
    "GCF_000801165.1": "RM9387",
    "GCF_000987875.1": "SEC470",
    "GCF_000599665.1": "ST2747",
    "GCF_000597845.1": "ST540",
    "GCF_000833635.2": "USML2",
}

tree = Phylo.read(tree_file, "newick")

# Rename terminal taxa
for terminal in tree.get_terminals():
    if terminal.name in strain_names:
        terminal.name = strain_names[terminal.name]

# Draw tree
fig, ax = plt.subplots(figsize=(12, 8))

Phylo.draw(
    tree,
    axes=ax,
    do_show=False
)

ax.set_title(
    "Phylogenetic Tree of 11 Escherichia coli Strains\n"
    "Based on 2,379 Single-Copy Core Protein Families",
    fontsize=14
)

ax.set_xlabel("Branch length")

plt.tight_layout()

Path("figures").mkdir(exist_ok=True)

plt.savefig(
    output_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Renamed phylogenetic tree saved to:")
print(output_file)
