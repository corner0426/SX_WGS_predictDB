#! /usr/bin/env python

import sys

HEADER_FIELDS = ['chr','varID','rsid']
def split_plink_in(file, out_prefix):
	snps_by_chr_files= [out_prefix + '.chr' + str(i) + '.txt' for i in range(1,23)]
	snp_by_chr = [open(f, 'w') for f in snps_by_chr_files]
	
	header = '\t'.join(HEADER_FIELDS)+'\n'
	for f in snp_by_chr:
		f.write(header)
		
	with open(file, 'r') as plink_f:
		for line in plink_f:
			attrs = line.split()
			chr = attrs[0]
			index = int(chr) - 1
			#row_out = '\t'.join([chr, attrs[1], attrs[2]])
			snp_by_chr[index].write(line)
	for f in snp_by_chr:
		f.close()
		
if __name__ == '__main__':
	file = sys.argv[1]
	out_prefix = sys.argv[2]
	split_plink_in(file, out_prefix)