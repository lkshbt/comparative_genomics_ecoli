import pandas as pd

# Load enrichment results
enrichment = pd.read_csv(
    "results/pair_functional_enrichment.csv"
)

# Load functional annotations
annotations = pd.read_csv(
    "results/functional_analysis.csv"
)

# Significant results
sig = enrichment[
    enrichment["significant_FDR_0.05"] == True
]

print("Significant enriched categories:\n")
print(
    sig[
        ["pair", "category", "odds_ratio", "FDR"]
    ].to_string(index=False)
)

print("\n" + "=" * 70)

# Define the two significant pair/category combinations
targets = [
    ("RM9387 + CI5", "Surface/Adhesion"),
    ("C41(DE3) + BL21", "Carbohydrate metabolism")
]

for pair, category in targets:

    print("\n" + "=" * 70)
    print(pair, "→", category)
    print("=" * 70)

    # Determine the pair-specific family file
    if pair == "RM9387 + CI5":
        family_file = (
            "results/RM9387_CI5_pair_specific_annotations.csv"
        )
    else:
        family_file = (
            "results/C41_BL21_clade_specific_annotations.csv"
        )

    df = pd.read_csv(family_file)

    products = df["product"].fillna("").astype(str).str.lower()

    if category == "Surface/Adhesion":
        terms = [
            "fimbr",
            "pilus",
            "pili",
            "adhes",
            "outer membrane",
            "secretion",
            "tss",
            "o-antigen"
        ]

    else:
        terms = [
            "sugar",
            "carbohydrate",
            "glycosyl",
            "polymerase",
            "acetyltransferase"
        ]

    mask = products.apply(
        lambda x: any(term in x for term in terms)
    )

    selected = df[mask].copy()

    print(
        "\nMatching families:",
        len(selected)
    )

    print(
        "\nGene / product:\n"
    )

    for _, row in selected.iterrows():

        gene = (
            row["gene"]
            if pd.notna(row["gene"])
            else "-"
        )

        product = (
            row["product"]
            if pd.notna(row["product"])
            else "-"
        )

        print(
            f"{gene:15} | {product}"
        )

    output = (
        "results/"
        + pair.replace(" + ", "_")
        + "_"
        + category.replace("/", "_").replace(" ", "_")
        + "_families.csv"
    )

    selected.to_csv(
        output,
        index=False
    )

    print("\nSaved:", output)
