#!/usr/bin/env python

import subprocess

from model_parameters import *

VCF_IN_DIR = '/data/myl/WGS_Data_for_analysis/'
VCF_OUT_DIR = '../../../original_files/split_VCF/'
VCF_FN = 'All_chr_1329_samples_gt_beagle.vcf'
VCF_SPLIT_PREFIX = VCF_FN[:-4]  


print("Extracting chr, ID, RS_ID for LD pruned SNPs from PLINK bim file...")
subprocess.call(
    ['python', '../../scripts/make_pruned_snps_pd.py'])
	
	
print("Splitting a VCF file into multiple files by chromosome")
subprocess.call(
    ['python', '../../scripts/split_vcf_by_chr.py',
    VCF_IN_DIR + VCF_FN,
    VCF_OUT_DIR + VCF_SPLIT_PREFIX
    ])
	
print('Create geneotype dosage file and snp annotation files')
for i in range(1,23):
	subprocess.call(
		['nohup python', '../../scripts/make_geno.py',
		VCF_OUT_DIR + VCF_SPLIT_PREFIX + '.chr' + str(i) + '.vcf',
		INTER_DIR + SNP_ANN_DIR + STUDY_NAMES + '.chr' + str(i),
		INTER_DIR + SNP_ANN_DIR + STUDY_NAMES + '.chr' + str(i),
		'&'
		])
		
print("Genotype and SNP annotation file Done!")