import argparse
import os 

##Example run command
# python3 convert_outliersto_bed.py -i path-to_fst_file -obed outputfilename_with_.bed -img image_file_name.png
# python3 convert_outliersto_bed.py -i fst_file.fst -obed my_output.bed -oimg my_output_image.png


my_vars = argparse.ArgumentParser(description='Running an R script through python')

my_vars.add_argument('-i', type=str, metavar='.fst file', required=True, help='path tpfst data from selection scan')
my_vars.add_argument('-obed', type=str, metavar='output bed file', required=True, help='output bed file name/path')
my_vars.add_argument('-oimg', type=str, metavar='output image file,add your own extension', required=True, help='output image file name/path')

files = my_vars.parse_args()

# create R file. This file will always slightly change depending on the argparse input
with open('Master_Script.R','w+') as r_file:

    # gets a list of all the packages the user has installed
    r_file.write("packs<-library()$results[,1]\n\n")

    # installs the packages for them if they dont have it
    r_file.write("if(!'tidyverse' %in% packs){install.packages('tidyverse',repos = 'https://cran.rstudio.com')}\n\n")

    r_file.write("library(tidyverse)\n\n")

    # open the fst window data
    r_file.write(f"data <- read.table('{files.i}',header = T)\n\n")

    # create a function to calculate outliers. function start
    r_file.write("fst_outliers <- function(df,FST_values){\n\n")

    # store the value that represents the 99th percentile
    r_file.write("\tthreshold_value <- quantile(FST_values, probs=0.99, na.rm = T)\n\n")
    
    # create df with only outliers
    r_file.write("\toutliers <- df %>% \n\n\tmutate(outlier = ifelse(FST_values > threshold_value, 'outlier', 'background')) %>% \n\n \tfilter(outlier=='outlier') %>% \n\n \tarrange(desc(BIN_START))\n\n")

    # function end
    r_file.write("\treturn(outliers)\n}\n\n")

    # function for bed format. function start
    r_file.write("convert_to_bed <- function(df){\n\n")

    # get the columns for chromosome, window start and end
    r_file.write("\tbed_format <- df %>%\n\n\tselect(CHROM,BIN_START,BIN_END)\n\n")

    # function end
    r_file.write("\treturn(bed_format)\n}\n\n")

    # get fst outliers
    r_file.write("df_of_outliers <- fst_outliers(data,data$WEIGHTED_FST)\n\n")

    # convert to bed format
    r_file.write("outliers_in_bedformat <- convert_to_bed(df_of_outliers)\n\n")

    # create a file of our outliers in bed format
    r_file.write(fr"write.table(outliers_in_bedformat,sep='\t',file='{files.obed}',row.names = F,col.names = F,quote = F)")

    # plotting fst distribution
    r_file.write("\n\nfst_dsitribution <- ggplot(data=data,aes(x=WEIGHTED_FST)) +\n\n")

    r_file.write("\tgeom_histogram(position = 'dodge',fill='blue',colour='black') +\n\n")

    r_file.write("\tgeom_vline(xintercept=quantile(data$WEIGHTED_FST, probs=0.99, na.rm = T),colour='red',size=1.5) +\n\n")

    r_file.write("\tlabs(x='Fst Values',y='Count') +\n\n")

    r_file.write("\ttheme(legend.position = 'none')\n\n")

    # save the plot
    r_file.write(f"ggsave(filename = '{files.oimg}',plot=fst_dsitribution,width = 10,height = 11,units = 'in')")

# run the R script
os.system('Rscript Master_Script.R')