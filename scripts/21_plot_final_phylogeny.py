from Bio import Phylo
import matplotlib.pyplot as plt
from pathlib import Path

tree_file = "results/phylogeny/ecoli_final_tree.treefile"
output_file = "figures/ecoli_phylogenetic_tree_final.png"

strain_names = {
    "GCF_000801185.2": "94-3024",
    "GCF_000833145.1": "BL21 (TaKaRa)",
    "GCF_000830035.1": "C41(DE3)",
    "GCF_000971615.1": "CI5",
    "GCF_000953515.1": "K-12 HMS174",
    "GCF_000952955.1": "K-12 RV308",
    "GCF_000801165.1": "RM9387",
    "GCF_000987875.1": "SEC470",
    "GCF_000599665.1": "ST2747",
    "GCF_000597845.1": "ST540",
    "GCF_000833635.2": "USML2",
}

tree = Phylo.read(tree_file, "newick")

for terminal in tree.get_terminals():
    if terminal.name in strain_names:
        terminal.name = strain_names[terminal.name]

fig, ax = plt.subplots(figsize=(13, 9))

Phylo.draw(
    tree,
    axes=ax,
    do_show=False,
    label_func=lambda clade: clade.name
)

ax.set_title(
    "Maximum-Likelihood Phylogeny of Escherichia coli Strains",
    fontsize=16,
    fontweight="bold",
    pad=20
)

ax.text(
    0.5,
    1.01,
    "2,379 single-copy core protein families | 1,000 UFBoot + 1,000 SH-aLRT",
    transform=ax.transAxes,
    ha="center",
    fontsize=11
)

ax.set_xlabel(
    "Amino-acid substitutions per site",
    fontsize=11
)

ax.set_ylabel("Strains", fontsize=11)

ax.tick_params(axis="both", labelsize=9)

plt.tight_layout()

Path("figures").mkdir(exist_ok=True)

plt.savefig(
    output_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Final phylogenetic figure saved to:")
print(output_file)
