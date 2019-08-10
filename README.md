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



### Genotype dosage file & SNP annotation file

#### PLINK based LD prune

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
'using VCF instead of ped'
```

#### Generate files from VCF file
* The BEAGLE VCF format provides useful information to generate genotype dosage file and snp annotation file. `0|0 homozygote reference, dosage as 0; 0|1 heterozyote, dosage as 1`, see [VCF format](https://faculty.washington.edu/browning/beagle/intro-to-vcf.html).
* The genotype dosage file and SNP annotation file can be generated from the above VCF file. However, the original file is too big to deal with. So, I made the following strategies.
  1. extract LD pruned SNPs with information including `chr and pos` from PLINK fam file - `make_pruned_snps.py`; (Note: using list to extract snp from large file is too slow, change the script that using pandas `make_prunded_snps_pd.py`)
  2. split the VCF file by chr, and excluded pruned out SNPs by the way - `split_vcf_by_chr.py`;
  3. create the genotype dosage and SNP annotation file from the split VCF file (no needs to be combined) - `split_vcf_by_chr.py`
  4. The above three steps were integrated into a calling script - `create_geno_snp_anno.py` 

```shell
#store the make_pruned_snps.py split_vcf_by_chr.py split_vcf_by_chr.py into ~/predictDB/PredictDBPipeline/scripts
#store the create_geno_snp_anno.py into ~/predictDB/PredictDBPipeline/joblogs/SX_WGS_predictDB
cd ~/predictDB/PredictDBPipeline/joblogs/SX_WGS_predictDB
python create_geno_snp_anno.py 
```

