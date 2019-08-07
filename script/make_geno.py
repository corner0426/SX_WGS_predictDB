#! /usr/bin/env python3

'''
create geneotype dosage file and snp annotation file based on BEAGLE VCF format

first, only included SNPs in plink.prune.in file

second, create snp annotation file based on VCF marker information

Third, calculate genotype dosage for all samples, and finally keep RNA seq samples
'''

INPUT_DIR = '../../data/input/'
SNP_ANN_DIR = 'annotations/snp_annotation/'
GENOTYPE_DIR = 'genotypes/'

## SNP anno file write header
snp_anno = open(INPUT_DIR + SNP_ANN_DIR + 'sxjc.annot.txt', 'w')
snp_anno_FIELDS = ['Chr', 'Pos', 'VariantID', 'Ref_b37', 'Alt', 'snp_id_originalVCF', 'RSID_dbSNP']
snp_anno_header = '\t'.join(snp_anno_FIELDS) + '\n'
snp_anno.write(snp_anno_header)

## genotype file 
geno = open(INPUT_DIR + GENOTYPE_DIR + 'sxjc.snps.txt', 'w')


##create list for pruned SNPs
snp_lst = []
print ('reading pruned snps')
with open('../../../original_files/plink.prune.in', 'r') as snp_in:
	for line in snp_in:
		line = line.strip('\n')
		snp_lst.append(line)
print ('The total number of included SNPs : %d' % len(snp_lst))

##open VCF file 
print ('reading VCF file')
with open('/data/myl/WGS_Data_for_analysis/All_chr_1329_samples_gt_beagle.vcf', 'r') as vcf:
	for line in vcf:
		if line.startswith('##'): continue
		vcf_field = line.split('\t')
		if vcf_field[0] == '#CHROM':
			geno_field = ['Id'] + [i for i in vcf_field[9:len(vcf_field)]]
			geno_header = '\t'.join(geno_field)
			geno.write(geno_header)
		rs_id = vcf_field[2]
		if rs_id not in snp_lst: continue
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
		
		
		
