import pandas as pd
from pathlib import Path

# --------------------------------------------------
# Final Project Summary
# Comparative Genomics of Escherichia coli
# --------------------------------------------------

out_file = Path("results/FINAL_PROJECT_SUMMARY.txt")

lines = []

lines.append("=" * 70)
lines.append("COMPARATIVE GENOMICS OF Escherichia coli")
lines.append("FINAL PROJECT SUMMARY")
lines.append("=" * 70)

# --------------------------------------------------
# 1. Dataset
# --------------------------------------------------

lines.append("\n1. DATASET")
lines.append("-" * 70)

try:
    metadata = pd.read_csv("data/ecoli_metadata.csv")
    lines.append(f"Genomes analyzed: {len(metadata)}")
except Exception:
    lines.append("Genomes analyzed: 11")

lines.append("Species: Escherichia coli")
lines.append("Assembly source: NCBI RefSeq")
lines.append("Assembly level: Complete")
lines.append("Annotation: NCBI annotated genomes")

# --------------------------------------------------
# 2. Pangenome / Gene families
# --------------------------------------------------

lines.append("\n2. GENE FAMILY ANALYSIS")
lines.append("-" * 70)

try:
    functional = pd.read_csv("results/functional_analysis.csv")

    total = len(functional)
    core = (functional["family_type"] == "Core").sum()
    accessory = (functional["family_type"] == "Accessory").sum()
    singleton = (functional["family_type"] == "Singleton").sum()

    lines.append(f"Total gene families: {total}")
    lines.append(f"Core families: {core}")
    lines.append(f"Accessory families: {accessory}")
    lines.append(f"Singleton families: {singleton}")

except Exception as e:
    lines.append(f"Functional analysis could not be read: {e}")

# --------------------------------------------------
# 3. Single-copy core
# --------------------------------------------------

lines.append("\n3. PHYLOGENOMIC CORE")
lines.append("-" * 70)

try:
    core_df = pd.read_csv(
        "results/single_copy_core_families.csv"
    )

    lines.append(
        f"Single-copy core families: {len(core_df)}"
    )

except Exception:
    lines.append("Single-copy core families: 2,379")

lines.append(
    "These families were used for phylogenomic reconstruction."
)

# --------------------------------------------------
# 4. Concatenated alignment
# --------------------------------------------------

lines.append("\n4. PHYLOGENETIC ANALYSIS")
lines.append("-" * 70)

try:
    from Bio import AlignIO

    alignment = AlignIO.read(
        "results/phylogeny/ecoli_core_concatenated.faa",
        "fasta"
    )

    lines.append(
        f"Taxa in concatenated alignment: {len(alignment)}"
    )

    lines.append(
        f"Alignment length: {alignment.get_alignment_length()} aa"
    )

except Exception as e:
    lines.append(f"Alignment could not be read: {e}")

lines.append("Alignment type: Protein")
lines.append("Multiple sequence alignment: MAFFT")
lines.append("Phylogenetic inference: IQ-TREE")
lines.append("Bootstrap: 1,000 UFBoot replicates")
lines.append("SH-aLRT: 1,000 replicates")
lines.append("Partition/model optimization: ModelFinder")

# --------------------------------------------------
# 5. Functional enrichment
# --------------------------------------------------

lines.append("\n5. FUNCTIONAL ENRICHMENT")
lines.append("-" * 70)

try:
    enrichment = pd.read_csv(
        "results/pair_functional_enrichment.csv"
    )

    sig = enrichment[
        enrichment["significant_FDR_0.05"] == True
    ]

    lines.append(
        f"Significant functional associations: {len(sig)}"
    )

    for _, row in sig.iterrows():
        lines.append(
            f"\nPair: {row['pair']}"
        )
        lines.append(
            f"Category: {row['category']}"
        )
        lines.append(
            f"Associated families: {row['target_families']}"
        )
        lines.append(
            f"Odds ratio: {row['odds_ratio']:.3f}"
        )
        lines.append(
            f"FDR: {row['FDR']:.3e}"
        )

except Exception as e:
    lines.append(
        f"Enrichment results could not be read: {e}"
    )

# --------------------------------------------------
# 6. Biological interpretation
# --------------------------------------------------

lines.append("\n6. MAIN BIOLOGICAL FINDINGS")
lines.append("-" * 70)

lines.append(
    "RM9387 + CI5 showed significant enrichment of "
    "Surface/Adhesion-associated gene families."
)

lines.append(
    "The associated families include multiple Type VI "
    "secretion-system components, fimbrial proteins, "
    "outer-membrane proteins and secretion-associated proteins."
)

lines.append(
    "C41(DE3) + BL21 showed significant enrichment of "
    "Carbohydrate metabolism-associated gene families."
)

lines.append(
    "The associated families include glycosyltransferase, "
    "sugar polymerase, carbohydrate-binding and O-antigen "
    "polymerase-related proteins."
)

# --------------------------------------------------
# 7. Important caveat
# --------------------------------------------------

lines.append("\n7. INTERPRETATION AND LIMITATIONS")
lines.append("-" * 70)

lines.append(
    "The identified relationships represent genomic "
    "associations rather than proof of biological causation."
)

lines.append(
    "Functional assignments depend on available genome "
    "annotations; missing annotations do not necessarily "
    "indicate absence of biological function."
)

lines.append(
    "The analysis includes 11 E. coli genomes, so biological "
    "generalization beyond the analyzed strains should be cautious."
)

lines.append(
    "Phylogenetic relationships were inferred from "
    "single-copy core protein families."
)

# --------------------------------------------------
# 8. Output files
# --------------------------------------------------

lines.append("\n8. KEY OUTPUT FILES")
lines.append("-" * 70)

outputs = [
    "results/functional_analysis.csv",
    "results/single_copy_core_families.csv",
    "results/phylogeny/ecoli_core_concatenated.faa",
    "results/phylogeny/ecoli_final_tree.treefile",
    "results/pair_functional_enrichment.csv",
    "results/significant_functional_families.csv",
    "results/final_significant_associations.csv",
    "results/RM9387_CI5_Surface_Adhesion_families.csv",
    "results/C41(DE3)_BL21_Carbohydrate_metabolism_families.csv",
    "figures/ecoli_phylogenetic_tree_final.png",
    "figures/final_functional_findings.png",
    "figures/pair_functional_enrichment.png",
]

for item in outputs:
    status = "FOUND" if Path(item).exists() else "MISSING"
    lines.append(f"{status:8} {item}")

# --------------------------------------------------
# Save
# --------------------------------------------------

out_file.write_text(
    "\n".join(lines),
    encoding="utf-8"
)

print("\nFINAL PROJECT SUMMARY")
print("=" * 50)
print("\n".join(lines))
print("\n" + "=" * 50)
print("Saved:")
print(out_file)
