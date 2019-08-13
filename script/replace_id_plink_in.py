#! /usr/bin/env python
import sys
import re
import pandas as pd

'''
script to replace snp id from plink bim to vcf format in plink prune in file
'''

def replace_id_plink_in(plink_in_file, dosage_file, plink_out_file):
	print('reading dosage file %s' % (dosage_file))
	dosage_frame = pd.read_csv(dosage_file, sep = '\t')
	
	print('reading plink in file %s' % (plink_in_file))
	plink_frame = pd.read_csv(plink_in_file, sep = '\t')
	
	n = 0
	plink_out = open(plink_out_file, 'w')
	for i in range(dosage_frame.shape[0]):
		for j in range(plink_frame.shape[0]):
			if re.match(plink_frame['varID'][j][:-8], dosage_frame['Id'][i]):
				out_row = '\t'.join([dosage_frame['Id'][i], plink_frame['rsid'][j]]) + '\n'
				plink_out.write(out_row)
				plink_frame.drop(j, inplace = True)
				n += 1
				print(n)
				
if __name__ == '__main__':
	plink_in_file = sys.argv[1]
	dosage_file = sys.argv[2]
	plink_out_file = sys.argv[3]
	replace_id_plink_in(plink_in_file, dosage_file, plink_out_file)	
		
	