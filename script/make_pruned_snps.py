#! /usr/bin/env python

'''
Script to extract chr, ID, RS_ID for LD pruned SNPs from PLINK bim file
'''

SNP_lst=[]
with open('/data1/yaoyh/predictDB/original_files/plink.prune.in', 'r') as f1:
	for line in f1:
		line = line.strip('\n')
		SNP_lst.append(line)

f_out = open('/data1/yaoyh/predictDB/original_files/plink.prune.in.txt', 'w') 		
with open('/data/myl/WGS_Data_for_analysis/chrALL_1329_samples_MAF_0.01_new_beagle.bim') as f2:
	for line in f2:
		l = line.split()
		chr = l[0]
		pos = l[3]
		id = '%s_%s' % (chr, pos)
		rsid = l[1]
		if rsid in SNP_lst:
			f_out.write('%s\t%s\t%s\n' % (chr, id, rsid))