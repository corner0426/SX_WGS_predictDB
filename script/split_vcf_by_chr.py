#! /usr/bin/env python

import os
import sys

'''
Script to split a VCF file into multiple files by chromosome.

From commandline, first argument is the genotype file, second is the
prefix for the output files.  The suffix 'chrN.vcf' will be added to the
prefix provided, where N is the chromosome number.

In splitting, script will only keep unambiguously stranded SNPs. I.e.,
no INDELs and no SNPs with polymorphisms A->T and vice-versa, or C->G
and vice-versa.

'''

##create dict for pruned SNPs, using chr as keys and index for downstream 
snp_dict = {}
print ('reading pruned snps')
with open('/data1/yaoyh/predictDB/original_files/plink.prune.in_pd.txt', 'r') as snp_in:
	for line in snp_in:
		#line = line.strip('\n')
		l = line.split()
		#snp_lst.append(line)
		snp_dict.setdefault(l[0], []).append(l[1])
#print ('The total number of included SNPs : %d' % len(snp_lst))
for i in snp_dict:
	print ('The number of SNPs for chr{0} is {1}'.format(i,len(snp_dict[i])))

def split_vcf(vcf_file, out_prefix):
	# Make output file names from prefix.
	vcf_by_chr_fns = [out_prefix + '.chr' + str(i) + '.vcf' for i in range(1,23)]
	# Open connection to each output file.
	vcf_by_chr = [open(f, 'w') for f in vcf_by_chr_fns]
	
	with open(vcf_file, 'r') as vcf:
		for line in vcf:
			if line.startswith('##'): continue
			#if line.startswith('#CHROM'):
				#vcf_header = line
				#for f in vcf_by_chr:
					#f.write(line)
			vcf_field = line.split('\t')
			if vcf_field[0] == '#CHROM':
				vcf_header = line
				for f in vcf_by_chr:
					f.write(line)
				continue
			#chr = vcf_field[0].replace('chr', '')
			chr = vcf_field[0][3:]
			snp_id = '%s_%s' % (chr, vcf_field[1])
			#if rs_id not in snp_lst: continue
			index = int(chr) - 1
			if snp_id in snp_dict[chr]:
				vcf_by_chr[index].write(line)
				
	for f in vcf_by_chr:
		f.close()
					
if __name__ == '__main__':
    vcf_file = sys.argv[1]
    out_prefix = sys.argv[2]
    split_vcf(vcf_file, out_prefix)

			