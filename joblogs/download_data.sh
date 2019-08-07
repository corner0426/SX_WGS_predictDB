#!/usr/bin/env bash

# Download zipped tar file of input data.
#curl -O https://s3.amazonaws.com/imlab-open/Data/PredictDB/predictdb_example.tar.gz

#tar -zxvf predictdb_example.tar.gz

# Build directory tree
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


# Reduce gencode annotation to genes only
#awk '$3 == "gene"' /data1/biocloud/genome/human_ensemble_chr/Homo_sapiens.GRCh38.89_chr_version.gtf \
#    > /data1/yaoyh/predictDB/original_files/gencode.GRCh38.89.genes.gtf


#SNP annotation file


#Gene expression file 
cp /data1/nkm/mayunlong-all-project/project-xiyan/20181227-lncRNA-analyst/result/3.Expression/gene/gene-int-count-matrix.txt \
    /data1/yaoyh/predictDB/original_files/SX_count.txt
sed -i 's/-/_/g' /data1/yaoyh/predictDB/original_files/SX_count.txt
cat <<EOF> count_normalize.R
#/bin/R
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

EOF

chmod 755 count_normalize.R
Rscript ./count_normalize.R






