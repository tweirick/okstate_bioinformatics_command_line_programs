'''
@author: Tyler Weirick 
@date: 2013-23-08
==============================================================================
This program will average columns together. 
INPUT: 
- A text file with tab separated values 
- a string of integers separated by commas corresponding to columns to be 
  averaged
OUTPUT: 
A file with one averaged value per line. with the suffix .avg.txt
============================================================================== 
'''

import argparse
from glob import glob

parser = argparse.ArgumentParser(
   description=open(__file__).read().split("'''")[1],
   formatter_class=argparse.RawDescriptionHelpFormatter)  

parser.add_argument('--file_name',
                   help='File name or regex.')
parser.add_argument('--col_numbers',
                   help='A string on column numbers to check.',
                   default=1)

args = parser.parse_args()
file_name_glob = glob(args.file_set)
col_list = set([ int(i)-1 for i in args.col_numbers.split(",") ])
max_val = float(args.max_val)

for file_name in file_name_glob:
    out_file_list = []
    for line in open(file_name,'r'):
        out_line = []
        sp_line = line.split("\t")     
        numbs_in_avg = 0.0
        line_total = 0.0
        for i in range(len(sp_line)):
            #if a column is in the column list  
            if i in col_list:
                try:
                    num_val = float(sp_line[i])
                except:            
                    num_val = 0.0
                if num_val != 0:
                    numbs_in_avg+=1.0
                line_total+=num_val
        out_file_list.append( str(line_total/numbs_in_avg)  )
    of = open(file_name+'.avg.txt','w')
    of.write( "\n".join(out_file_list) )
    of.close()

