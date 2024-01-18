# Script to extract IDs from txt file
import re
import argparse

# Example run command
# python3 retrive_IDs.py -i path_to_vcf -j 'pop1name','pop2name','pop3name'
# python3 retrive_IDs.py -i vcf_file.vcf -j 'POP1','POP2','POP3'

my_vars = argparse.ArgumentParser(description='Taking a vcf file')

my_vars.add_argument('-i', type=str, metavar='vcf file', required=True, help='give the path to first tsv')
my_vars.add_argument('-j', type=str, metavar='list of population names', required=True, help='List format is pop1,pop2,pop3')

vcf_file = my_vars.parse_args()

# Open main file
with open(vcf_file.i,'r+') as f:

	# Get the positions for the line in the vcf with headers
	vcf_headers_pos = re.search('#CHROM.*',f.read())
	
	# Go back to top of file
	f.seek(0)

	# Get list of vcf headers
	vcf_headers = f.read()[vcf_headers_pos.start():vcf_headers_pos.end()]
	
	# Go through each unique population name
	for pop_name in vcf_file.j.split(','):
		
		# Open a new file using the population name
		new_file = open(f'{pop_name}_population.txt','w+')

		# Look in vcf header line for populations with that name
		for header in vcf_headers.split():
			
			# Write out the IDs into separate text files	
			if header.startswith(pop_name):
				
				new_file.write(f'{header.rstrip()}\n')
				
		new_file.close()

