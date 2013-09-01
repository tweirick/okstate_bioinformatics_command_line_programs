'''
@author: Tyler Weirick 
@date: 2013-23-08
==============================================================================
This program will read columns containing plus or minus signs. If all vals in 
a row are plus signs output a plus sign. 
INPUT: 
A file wiht numerical values in columns in tab delimited format. 
OUTPUT: 
a column of plus or minus signs to a text file. 
============================================================================== 
'''
import argparse
from glob import glob

OUT_CHAR = "-"
SPLIT_CHAR = ","

parser = argparse.ArgumentParser(
   description=open(__file__).read().split("'''")[1],
   formatter_class=argparse.RawDescriptionHelpFormatter)  

parser.add_argument('--file_set',
                   help='File name or regex.')
parser.add_argument('--col_numbers',
                   help='A string on column numbers to check.',
                   default="1,2")

args = parser.parse_args()
file_name_glob = glob(args.file_set)
col_in_txt = args.col_numbers
col_list = set([ int(i)-1 for i in col_in_txt.split(",") ])


for file_name in file_name_glob:
    out_file_list = []
    for line in open(file_name,'r'):
        out_line = []
        sp_line = line.strip().split("\t")   
        pos_bool = True 
        out_line = "+" 
        for i in range(len(sp_line)):
            #if a column is in the column list  
            if i in col_list:
                if sp_line[i] == "-":
                    out_line = "-" 
                elif sp_line[i] != "+":
                    print("error",sp_line[i])
                    exit()
        out_file_list.append(out_line)
    col_txt = "cols-"+col_in_txt.replace(SPLIT_CHAR,OUT_CHAR)+"."

    of = open(file_name+'.pn_to_pn.'+col_txt+'tsv','w')
    of.write( "\n".join(out_file_list) )
    of.close()

