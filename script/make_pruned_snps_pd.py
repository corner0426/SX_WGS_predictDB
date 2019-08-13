#! /usr/bin/env python

'''
Script to extract chr, ID, RS_ID for LD pruned SNPs from PLINK bim file

The id format for each snp is '1_101', will use as index 
'''
import pandas as pd

#SNP_lst=[]
#with open('/data1/yaoyh/predictDB/original_files/plink.prune.in', 'r') as f1:
#	for line in f1:
#		line = line.strip('\n')
#		SNP_lst.append(line)

#

chr_dict = {}
id_dict = {}
with open('/data/myl/WGS_Data_for_analysis/chrALL_1329_samples_MAF_0.01_new_beagle.bim') as f2:
	for line in f2:
		l = line.split()
		chr = l[0]
		pos = l[3]
		#id = '%s_%s_%s_%s_b37' % (chr, pos, l[4], l[5])
		id = '%s_%s' % (chr, pos)
		rsid = l[1]
		#if rsid in SNP_lst:
		#	f_out.write('%s\t%s\t%s\n' % (chr, id, rsid))
		chr_dict.setdefault(rsid, chr)
		id_dict.setdefault(rsid,id)

SNP_dataframe = pd.DataFrame({'CHR': chr_dict, 'ID_index':id_dict})


f_out = open('/data1/yaoyh/predictDB/original_files/plink.prune.in_pd.txt', 'w')
with open('/data1/yaoyh/predictDB/original_files/plink.prune.in', 'r') as f1:
	for line in f1:
		snp = line.strip('\n')
		if snp in SNP_dataframe.index:
			chr_out = SNP_dataframe['CHR'][snp]
			id_out = SNP_dataframe['ID_index'][snp]
			out_line = '\t'.join([chr_out, id_out, snp]) + '\n'
			f_out.write(out_line)