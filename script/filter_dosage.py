#!/usr/bin/env python

'''
Script to extarct samples and SNPs from dosage file
'''
import sys
import re
import pandas as pd

##create dict for pruned SNPs, using chr as keys and index for downstream 
snp_dict = {}
print ('reading pruned snps')
with open('/data1/yaoyh/predictDB/original_files/plink.prune.in_pd.txt', 'r') as snp_in:
	for line in snp_in:
		#line = line.strip('\n')
		l = line.split()
		#snp_lst.append(line)
		#snp_index = l[0] #chr_pos
		snp_dict.setdefault(l[0], []).append(l[1])
#print ('The total number of included SNPs : %d' % len(snp_lst))
for i in snp_dict:
	print ('The number of SNPs for chr{0} is {1}'.format(i,len(snp_dict[i])))
	
#Reading sample files
sample_lst = ['Id']
sample_df = pd.read_csv('/data1/yaoyh/predictDB/original_files/sample_id.txt', sep='\t')
samples = sample_df['ID2']
print('The total number of samples included is %d' % (len(samples)))
sample_lst = sample_lst + list(samples)
#sample_lst.append('Id')
print(sample_lst)


def filter_dosage(file_in_frefix, file_out_geno_prefix, file_out_anno_prefix, chr):
	'''
	file_in_frefix = /path_in_split_dosage/All_chr_1329_samples_gt_beagle
	'''
	geno_in_fn = file_in_frefix + '.chr' + str(chr) + '.dosage.txt'
	anno_in_fn = file_in_frefix + '.chr' + str(chr) + '.annot.txt'
	geno_out_fn = file_out_geno_prefix + 'chr' + str(chr) + '.dosage.txt'
	anno_out_fn = file_out_anno_prefix + '.chr' + str(chr) + '.annot.txt'
	
	# genotype file
	print('reading dosage file %s' % (geno_in_fn))
	dosage_frame = pd.read_csv(geno_in_fn, sep = '\t')
	## first extract samples
	print('extracting samples for %s' % (geno_in_fn))
	dosage_filter_sample_frame = dosage_frame.loc[:,sample_lst]
	#print('replacing snp index for vcf id format for chr %s' % (chr))
	#n = 0
	#for i in range(len(dosage_filter_sample_frame['Id'])):
	#	for j in range(len(snp_dict[str(chr)])):
	#		if re.match(snp_dict[str(chr)][j], dosage_filter_sample_frame['Id'][i]):
	#			snp_dict[str(chr)][i] = dosage_filter_sample_frame['Id'][j]
	#			n += 1
	#			print (n)
	#			break
	#print('The number of matched SNPs for chr%s is %d' % (chr, n))		
	## then filter SNPs
	print('filtering SNPs for %s' % (geno_in_fn))
	dosage_filter_snp_frame = dosage_filter_sample_frame.loc[dosage_filter_sample_frame['Id'].isin(snp_dict[str(chr)]),:]
	## write dosage files
	print('Writting genotype file %s' % (geno_out_fn))
	dosage_filter_snp_frame.to_csv(geno_out_fn, index = False, sep = '\t')
	
	# annotation file
	print('filtering annot file %s' % (anno_in_fn))
	annot_frame = pd.read_csv(anno_in_fn, sep = '\t')
	annot_filter_snp_frame = annot_frame.loc[annot_frame['VariantID'].isin(snp_dict[str(chr)]),:]
	
	
if __name__ == '__main__':
	file_in_frefix = sys.argv[1]
	file_out_geno_prefix = sys.argv[2]
	file_out_anno_prefix = sys.argv[3]
	chr = sys.argv[4]
	
	filter_dosage(file_in_frefix, file_out_geno_prefix, file_out_anno_prefix, chr)
	
		