'''
@author: Tyler Weirick
@date: 2013-08-16
==============================================================================
This program will calculate the Storey FDR for a given column of values from 
a file containing one value per line of a tab delimited file. It requires 
the rpy2 library as well as the qvalue library for R from bioconductor. 
INPUT:
- A file or regex describing a set of files which contain p-values. 
- A string of comman separated integers corresponding to column numbers in 
  the tab delimited file. 
OUTPUT: 
- Storey FDR values. 
==============================================================================
'''
import argparse
parser = argparse.ArgumentParser(
description=open(__file__).read().split("'''")[1],
formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('--file_set',
                   help='A file name or regex. ',
                   required=True)

parser.add_argument('--col_numbers',
                   help='A string of column numbers to check. Counting starts from one.',
                   default="1")

from rpy2 import *
import rpy2.robjects as R
import rpy2.rpy_classic as rpy
from glob import glob
rpy.set_default_mode(rpy.NO_CONVERSION)
rpy.set_default_mode(rpy.BASIC_CONVERSION)
R.r.library('qvalue')

OUT_CHAR = "-"
SPLIT_CHAR = ","

#Pass args.
args = parser.parse_args()
file_name_glob = glob(args.file_set)
col_in_txt = args.col_numbers
col_set = set([ int(i)-1 for i in col_in_txt.split(SPLIT_CHAR) ])

for file_name in file_name_glob:

    #Story FDR requires an entire set of values for calculation.  
    #Therefore each cold needs to be in a list. Will keep track of this 
    #with a 2D list instanciate with the correct number of empty lists to 
    #keep from checking during parsing. 
    #pvalue_list = [ [] ] * len(col_set)
    pval_list_dict = {}
    for line in open(file_name,'r'):
        sp_line = line.split("\t")
        for i in range( len(sp_line) ):        
            if i in col_set:  
                if str(i) in pval_list_dict:
                    pval_list_dict[str(i)].append( float(sp_line[i]) )
                else:
                    pval_list_dict.update( {str(i): [float(sp_line[i]) ]})
                
                #pvalue_list[i].append( float(sp_line[i]) )
                
    #Calculate Storey FDR values.     
    #The R function returns a number of values regarding the stat cals 
    #but we only need to values. They are located in the third element.
    storey_col_list = []
    for pval_col in sorted(pval_list_dict.keys()):
        #print(pval_col)
        #print(    R.r.qvalue( R.FloatVector(  pval_list_dict[ pval_col]  ) )[2]     ) 
        storey_col_list.append( R.r.qvalue( R.FloatVector(  pval_list_dict[ pval_col]  ) )[2] )
  
    out_str_list = [] 
    for x in range( len(storey_col_list[0]) ):
        line_list = []    
        for y in range( len(storey_col_list) ): 
            line_list.append( str( storey_col_list[y][x]) )  
        out_str_list.append("\t".join(line_list))
    
    #Output a text file with one p-value per line. 
    of = open(file_name+".storey.txt",'w')
    of.write("\n".join(out_str_list))
    of.close()

