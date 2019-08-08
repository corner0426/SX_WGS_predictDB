#! /usr/bin/env python3

'''
create geneotype dosage file and snp annotation file based on BEAGLE VCF format

Note that the VCF file is splited by chr. Thus, the following two steps was packed into function

I, create snp annotation file based on VCF marker information

II, calculate genotype dosage for all samples, and finally keep RNA seq samples
'''
import os
import sys

## SNP anno file write header
#snp_anno = open(INPUT_DIR + SNP_ANN_DIR + 'sxjc.annot.txt', 'w')
snp_anno_FIELDS = ['Chr', 'Pos', 'VariantID', 'Ref_b37', 'Alt', 'snp_id_originalVCF', 'RSID_dbSNP']
snp_anno_header = '\t'.join(snp_anno_FIELDS) + '\n'

##open VCF file
def make_geno(vcf_file, gene_out_prefix, snp_anno_out_prefix): 
	geno = open(gene_out_prefix + 'dosage.txt', 'w')
	snp_anno = open(snp_anno_out_prefix + 'annot.txt', 'w')
	snp_anno.write(snp_anno_header)

	print ('reading VCF file')
	with open(vcf, 'r') as vcf:
		for line in vcf:
			#if line.startswith('##'): continue
			vcf_field = line.split('\t')
			#write header for genotype file
			if vcf_field[0] == '#CHROM':
				geno_field = ['Id'] + [i for i in vcf_field[9:len(vcf_field)]]
				geno_header = '\t'.join(geno_field)
				geno.write(geno_header)
			
			chr = vcf_field[0].replace('chr', '')
			pos = vcf_field[1]
			ref = vcf_field[3]
			alt = vcf_field[4]
			var_ID = '%s_%s_%s_%s_b37' % (chr, pos, ref, alt)
			snp_anno.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (chr, pos, var_ID, ref, alt, var_ID, rs_id))
			dosage_lst = []
			dosage_lst.append(var_ID)
			dosage_lst = dosage_lst + [str((int(dosage.split('|')[0]) + int(dosage.split('|')[1]))) for dosage in vcf_field[9:len(vcf_field)]]
			dosage_out = '\t'.join(dosage_lst) + '\n'
			geno.write(dosage_out)
		
if __name__ == '__main__':
    vcf_file = sys.argv[1]
    gene_out_prefix = sys.argv[2]
	snp_anno_out_prefix = sys.argv[3]
	
    make_geno(vcf_file, gene_out_prefix, snp_anno_out_prefix)

		
