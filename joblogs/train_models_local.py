#!/usr/bin/env python

import subprocess
import time

from model_parameters import *

#CMD = 'qsub -v study={0},expr_RDS={1},geno={2},gene_annot={3},snp_annot={4},' + \
#    'n_k_folds={5},alpha={6},out_dir={7},chrom={8},snpset={9},window={10} ' + \
#    '-N {0}_model_chr{8} -d {11} train_model_by_chr.pbs'

CMD = 'Rscript ./create_model.R {0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} &'
	


gene_annot = INTER_DIR + GENE_ANN_DIR + GENE_ANNOT_INTER2
for i, study in enumerate(STUDY_NAMES):
    expression_RDS = INTER_DIR + EXPRESSION_DIR + EXPR_INTER[i]
    for chr in range(1,23):
        geno = INTER_DIR + GENOTYPE_DIR + GENOTYPE_INTER_PREFIX[i] + \
            '.chr' + str(chr) + '.txt'
        snp_annot = INTER_DIR + SNP_ANN_DIR + SNP_ANN_INTER_PREFIX2 + str(chr) + '.RDS'
        cmd = CMD.format(study,expression_RDS,geno,gene_annot,snp_annot,
            N_K_FOLDS,ALPHA,MODEL_BY_CHR_DIR,str(chr),SNPSET,WINDOW)
	    #cmd = CMD.format(study,expression_RDS,geno,gene_annot,snp_annot,N_K_FOLDS,ALPHA,MODEL_BY_CHR_DIR,str(chr),SNPSET,WINDOW)
        print(cmd)
        with open('/proc/meminfo') as fd:
            for line in fd:
                if line.startswith('MemFree'):
                    free = line.split()[1]
                    break
        FreeMem = int(free)/(1024.0*1024)
        while True:
            if FreeMem > 25:		
                subprocess.call(cmd, shell=True)
                break
        time.sleep(2)
