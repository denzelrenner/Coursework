# File to match gene names
import argparse
import re

## Example run command 
# use the overalpped bed file as -i
# python3 filtering_candidates.py -i POP1vsPOP2_5000win.bed -g ../1-2-1_hits_all_gene_descriptions.tsv -o my_homologs.txt

my_vars = argparse.ArgumentParser(description='Taking a bed file')

my_vars.add_argument('-i', type=str, metavar='bed file', required=True, help='give the path to bed file with gene names')
my_vars.add_argument('-g', type=str, metavar='gene list file', required=True, help='give the path to file with the homo/orthologs')
my_vars.add_argument('-o', type=str, metavar='output file', required=True, help='output file name/path')


files = my_vars.parse_args()

# open our bed file and gene list file
with open(f'{files.i}', 'r+') as bed_file, open(f'{files.g}','r+') as gene_list, open(f'{files.o}','w+') as output_file:

    # create variable to store bed file data
    bed_file_data = bed_file.read()

    # extract all gene names from every row of data in the bed file
    raw_data_candidategenes = re.finditer(r'ID=.*;',bed_file_data)

    # create list for just the gene names from the bed file without the unneeded words
    candidate_genes = []

    # go through each match from our regular expression search (every ID='g121212')
    for match_object in raw_data_candidategenes:
        
        # store the match in a variable, filter out the ID = and ;,store gene in list
        potential_gene = bed_file_data[match_object.start():match_object.end()]

        potential_gene = potential_gene.replace(';','').replace('ID=','')

        # extra parsing to sort out gene IDs that have Parent= in them
        if 'Parent' in potential_gene:

            # remove any instance of Parent= and the string before it, leaving only the gene name
            potential_gene = re.sub(string=potential_gene,pattern=r'.*Parent=',repl='')
            
        # only add to the candidate gene list if it is not already there
        if not potential_gene in candidate_genes:

            candidate_genes.append(potential_gene)

    # create variable for gene list data
    gene_list_data = gene_list.read()

    # this list will prevent repeats in the output file by checking if a piece of data has already been written
    duplication_check = ['current_info']

    # go through each candidate gene and find the homologs
    for candidate in candidate_genes:
        
        # find lines in gene list tsv that start with the gene and end in a new line
        orthohomo_logs = re.finditer(rf'{candidate}.*\n', gene_list_data)

        # write out all the matches found in the gene list tsv to get our final set of homo/orthologs
        for ortho in orthohomo_logs:

            if gene_list_data[ortho.start():ortho.end()] != duplication_check[-1]:
                
                # change the value in the list to be what we are writing to the file
                duplication_check[-1] = gene_list_data[ortho.start():ortho.end()]

                output_file.write(f'{gene_list_data[ortho.start():ortho.end()]}')
        




