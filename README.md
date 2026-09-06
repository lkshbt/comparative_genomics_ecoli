# Comparative Genomics of Escherichia coli

## Identifying Conserved, Accessory, and Functionally Associated Gene Families

### Project Overview

This project uses comparative genomics to investigate gene-family conservation and functional associations across 11 complete, annotated *Escherichia coli* genomes from NCBI RefSeq.

The analysis combines genome quality control, protein clustering, pangenome-style gene-family classification, functional annotation, phylogenomic reconstruction, and statistical functional enrichment.

The primary objective was to identify gene-family patterns associated with groups of closely related *E. coli* strains.

---

## Research Question

**Which gene families are conserved or variable across *E. coli* strains, and which functional categories are significantly associated with specific strain groups?**

---

## Dataset

- Organism: *Escherichia coli*
- Number of genomes: **11**
- Source: **NCBI RefSeq**
- Assembly level: **Complete**
- Annotation: **NCBI annotated genomes**
- Data types:
  - Genome sequences
  - Protein sequences
  - CDS
  - GFF3 annotations

### Strains analyzed

| Strain | RefSeq Assembly |
|---|---|
| 94-3024 | GCF_000801185.2 |
| BL21 (TaKaRa) | GCF_000833145.1 |
| C41(DE3) | GCF_000830035.1 |
| CI5 | GCF_000971615.1 |
| K-12 HMS174 | GCF_000953515.1 |
| K-12 RV308 | GCF_000952955.1 |
| RM9387 | GCF_000801165.1 |
| SEC470 | GCF_000987875.1 |
| ST2747 | GCF_000599665.1 |
| ST540 | GCF_000597845.1 |
| USML2 | GCF_000833635.2 |

---

## Computational Workflow

```text
NCBI RefSeq genomes
        |
        v
Genome quality control
        |
        v
Protein extraction
        |
        v
MMseqs2 protein clustering
        |
        v
Gene-family classification
        |
        +------------------+
        |                  |
        v                  v
Core families        Accessory/Singleton
        |
        v
Single-copy core families
        |
        v
MAFFT multiple sequence alignment
        |
        v
Concatenated core alignment
        |
        v
IQ-TREE phylogeny
        |
        v
Phylogenetic strain relationships
        |
        v
Functional annotation
        |
        v
Pair-specific gene families
        |
        v
Fisher's exact test
        |
        v
FDR correction
        |
        v
Significant functional associations
