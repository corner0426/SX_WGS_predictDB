#!/usr/bin/env python

import subprocess
import os
import numpy as np

from model_parameters import *

VCF_IN_DIR = '/data/myl/WGS_Data_for_analysis/'
VCF_OUT_DIR = '../../../original_files/all_split_VCF/'
VCF_FN = 'All_chr_1329_samples_gt_beagle.vcf'
VCF_SPLIT_PREFIX = VCF_FN[:-4]  

DOSAGE_OUT_DIR = '../../../original_files/all_split_dosage/'


print("Extracting chr, ID, RS_ID for LD pruned SNPs from PLINK bim file - done")
#subprocess.call(
#    ['python', '../../scripts/make_pruned_snps_pd.py'])
	
	
print("Splitting a VCF file into multiple files by chromosome")
#subprocess.call(
#    ['python', '../../scripts/split_vcf_by_chr_nofilter.py',
#    VCF_IN_DIR + VCF_FN,
#    VCF_OUT_DIR + VCF_SPLIT_PREFIX
#    ])
	
print('Create genotype dosage file and snp annotation files without filter')
tesk_1 = np.ones(22)
for i in range(1,23):
	vcf_file = VCF_OUT_DIR + VCF_SPLIT_PREFIX + '.chr' + str(i) + '.vcf'
	geno_file = DOSAGE_OUT_DIR + VCF_SPLIT_PREFIX + '.chr' + str(i) + '.'
	gene_anno_file = DOSAGE_OUT_DIR + VCF_SPLIT_PREFIX + '.chr' + str(i) + '.'
	CMD = 'python ../../scripts/make_geno.py {0} {1} {2}'
	cmd = CMD.format(vcf_file, geno_file, gene_anno_file)
	#tesk.append('')
	p = subprocess.Popen(cmd, shell = True)
	tesk_1[i-1] = p.poll()
#Note: no more '&', and Popen will submit cmd 
#print(tesk)

while True:
	#print(tesk_2)
	print('waitting dosage transfor run')
	if sum(tesk_1) == 0:
		print(tesk_1)
		print('filter_dosage.py is over')
		break


	
print('Filter SNPs and samples for genotype file and SNPs for snp annotation file')
tesk_2 = np.ones(22)
for i in range(1,23):
	file_in_frefix = DOSAGE_OUT_DIR + VCF_SPLIT_PREFIX
	file_out_geno_prefix = INTER_DIR + GENOTYPE_DIR + STUDY_NAMES[0]
	file_out_anno_prefix = INTER_DIR + SNP_ANN_DIR + STUDY_NAMES[0]
	chr = i
	CMD = 'python ../../scripts/filter_dosage.py {0} {1} {2} {3}'
	cmd = CMD.format(file_in_frefix, file_out_geno_prefix, file_out_anno_prefix, chr)
	while True:
		if FreeMem > 10:
			subprocess.call(cmd, shell = True)
			#memory consumption, single command once (about 20mim per run)
			#tesk_2[i-1] = p.poll()
			break
		else: 
			print('waitting Memory filter_dosage chr%s' % (i))
#print(sum(tesk_2))


print("Genotype and SNP annotation file Done!")