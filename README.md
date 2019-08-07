# SX WGS Model Pipeline

This repository can be used for creating models for predicting gene expression. 

For the original analysis, no covariants were used for adjustment expression.

Genome build is hg19.



## Directory Structure & File preparation

### Build directory tree

```shell
cd ~/predictDB/PredictDBPipeline/joblogs/SX_WGS_predictDB
mkdir -pv \
    ../../data/input/annotations/gene_annotation/ \
    ../../data/input/annotations/snp_annotation/ \
    ../../data/input/expression_phenotypes/ \
    ../../data/input/genotypes/ \
    ../../data/intermediate/annotations/gene_annotation/ \
    ../../data/intermediate/annotations/snp_annotation/ \
    ../../data/intermediate/expression_phenotypes/ \
    ../../data/intermediate/genotypes/ \
    ../../data/intermediate/model_by_chr/ \
    ../../data/output/allBetas/ \
    ../../data/output/allCovariances/ \
    ../../data/output/allLogs/ \
    ../../data/output/allMetaData/ \
    ../../data/output/allResults/ \
    ../../data/output/dbs/ \
```

### gene annotation file

In gtf format, originating from RNA-seq  pipeline. Only `gene` remained. `GRCh38`

```shell
awk '$3 == "gene"' * > \
../../data/input/annotations/gene_annotation/gencode.GRCh38.89.genes.gtf
#58233 lines
```

`needs to be liftover to hg19 after parsing`



### Expression matrix file

Constructed at `Global_PC`, including sample ID transformation and normalization by voom.

Not sure whether genes in this matrix match genes in gtf file.

```R
## sample ID tranfor
gene_count_matrix<- read.table("gene-int-count-matrix.txt",header = T, sep = '\t', row.names = 1)
pheno_file = read.csv('sample_id.txt', sep = '\t')
#gene_count_matrix_t <- t(gene_count_matrix)
#gene_count_matrix_t[,1] <- pheno_file[match(gene_count_matrix_t[,1],pheno_file[,1]),2]
names(gene_count_matrix) <- pheno_file[match(names(gene_count_matrix), pheno_file[,1]),2]

## normalization
library(limma)
#rownames(gene_count_matrix) <- gene_count_matrix[,1]
gene_cpm_matrix <- voom(gene_count_matrix)

write.table(gene_cpm_matrix, sep = '\t', file = 'SX_gene_cpm_matrix.txt')
```

Manually replace quotations and add name for the 1st column



### Genotype dosage file

For SNPs selection, 1% MAF cutoff was applied (Yunlong did). Variants were filtered to remove any SNPs in high LD (R2 > 0.9)

```shell
# extract expression samples
plink --noweb --bfile chrALL_1329_samples_MAF_0.01_new_beagle --keep ~/predictDB/original_files/keep_sample.txt --make-bed --out ~/predictDB/original_files/chrALL_75_samples_MAF_0.01_new_beagle

cd ~/predictDB/original_files
# LD based SNP pruning
plink --noweb --bfile chrALL_75_samples_MAF_0.01_new_beagle --indep-pairwise 50 5 0.9
plink --noweb --bfile chrALL_75_samples_MAF_0.01_new_beagle --extract plink.prune.in --recode --out chrALL_75_samples_MAF_0.01_new_beagle_LD0.9
## 5865689 prune in
## 1510792 prune out

# from ped to dosage

```

