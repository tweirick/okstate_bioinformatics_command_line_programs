'''
@author: Tyler Weirick 
@date: 2013-23-08
==============================================================================
This program will read values in a tab delimited file and output a new file
with columns containing plus or minus signs. 
INPUT: 
- A file or regex for a set of files. 
- A string or integers delimited with commas ex: 2,3,4 
  corresponding to column numbers in the tab delimited file. 
- A number as a float, all values less than or equal to this value will be 
  set to a plus sign, all others will be set to a negative sign. 

OUTPUT: 
- A tab delimited file names as the input file name with the suffix, 
.plusneg.tsv . The columns  with the column checked in order.
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
                   help='A string of integers delimited by a "'+SPLIT_CHAR+'"',
                   default="1")
parser.add_argument('--max_val',
                   help='Values less than or equal than this value will recide plus signs.',
                   default=False)
parser.add_argument('--min_val',
                   help='Values greater than or equal to this value will receive a plus',
                   default=False)
parser.add_argument('--between_or_outside',
                   help='This determines if the program will check inside or outside. The given value(s) True or False',
                   default=True,
                   type=bool)

args = parser.parse_args()
file_name_glob = glob(args.file_set)
col_in_txt = args.col_numbers
col_list = set([ int(i)-1 for i in col_in_txt.split(SPLIT_CHAR) ])

between_or_outside = (args.between_or_outside == "True")
min_val = args.min_val
max_val = args.max_val

if min_val:
    min_val = float(min_val)    
 
if max_val: 
    max_val = float(max_val) 
        



for file_name in file_name_glob:
    out_file_list = []
    for line in open(file_name,'r'):
        out_line = []
        sp_line = line.split("\t")     
        for i in range(len(sp_line)):
            #if a column is in the column list  
            if i in col_list:
               val = float(sp_line[i])
               print(max_val,min_val,between_or_outside)
               if min_val and max_val:
                   if between_or_outside: 
                       if val <= max_val and val >= min_val: 
                           out_line.append("+")   
                       else: 
                           out_line.append("-")
                   else:                         
                       if val >= max_val or val <= min_val:  
                           out_line.append("+")
                       else: 
                           out_line.append("-")                            
               elif min_val and not max_val:                 
                   if min_val <= val:
                       out_line.append("+")
                   else:
                       out_line.append("-")
               elif not min_val and max_val:
                   if max_val >= val:
                       out_line.append("+")
                   else:
                       out_line.append("-")
               else: 
                   print("ERROR:")
               
        out_file_list.append("\t".join(out_line))
  
    col_txt = "cols-"+col_in_txt.replace(SPLIT_CHAR,OUT_CHAR)+"."
    val_txt = 'maxval-'+str(max_val)+"."

    of = open(file_name+'.plusneg'+col_txt+val_txt+'tsv','w')
    of.write( "\n".join(out_file_list) )
    of.close()



