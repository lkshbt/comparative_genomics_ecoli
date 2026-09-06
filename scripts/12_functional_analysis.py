import pandas as pd

presence_file = "results/gene_presence_absence.csv"
annotation_file = "results/family_annotations.csv"
output_file = "results/functional_analysis.csv"

# Load files
presence = pd.read_csv(presence_file, index_col=0).T
annotations = pd.read_csv(annotation_file)

# Number of genomes containing each family
frequency = presence.sum(axis=1)

# Classify families
def classify(n):
    if n == 11:
        return "Core"
    elif n == 1:
        return "Singleton"
    else:
        return "Accessory"

family_type = frequency.apply(classify)

# Build family-level table
family_summary = pd.DataFrame({
    "genomes_present": frequency,
    "family_type": family_type
})

# Keep one annotation record per protein family
annotations_unique = annotations.drop_duplicates("cluster")

# Add family annotations
family_summary = family_summary.reset_index()
family_summary = family_summary.rename(columns={"index": "cluster"})

family_summary = family_summary.merge(
    annotations_unique[
        ["cluster", "gene", "product", "go_function", "ontology_term"]
    ],
    on="cluster",
    how="left"
)

# Save
family_summary.to_csv(output_file, index=False)

print("Functional analysis complete!")
print(f"Total families: {len(family_summary)}")
print("\nFamily type counts:")
print(family_summary["family_type"].value_counts())
print(f"\nSaved to: {output_file}")

print("\nPreview:")
print(family_summary.head(10).to_string(index=False))