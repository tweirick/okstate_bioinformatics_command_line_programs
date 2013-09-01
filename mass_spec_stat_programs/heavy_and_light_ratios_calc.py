'''
@author: Tyler Weirick 
'''

from rpy2 import *
import rpy2.robjects as R
import rpy2.rpy_classic as rpy
from math import log
rpy.set_default_mode(rpy.NO_CONVERSION)
rpy.set_default_mode(rpy.BASIC_CONVERSION)


import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--file_name',
                   help='Input the name of the file to be processed. ')
parser.add_argument('--start_col_number',
                   help='The number of the colum where replicates start. If none given defaults to 1',
                   default=1)
parser.add_argument('--end_col_number',
                   help='The number of the column where the repicates end. If none give defaults to 10.',
                   default=10)

args = parser.parse_args()
file_name = args.file_name
#The number of the fisrt column -1 of the number of the column in excel.
start_col = int(args.start_col_number)-1
#The number of the last column -1 of the number of the column in excel.
end_col   = int(args.end_col_number)

assert start_col >= 0
assert end_col > start_col
assert (end_col-start_col)%2 == 0

mid_point = (end_col-start_col)/2
out_list  = []

for line in open(file_name,'r'):
    sl = line.split("\t")

    population_heavy = []
    population_light = []
    ratio_lines      = []
    for el_i in range(start_col,mid_point):
        
        l = float( sl[el_i] )
        h = float( sl[el_i+mid_point] )
        population_light.append(l)
        population_heavy.append(h)

    #print(population_heavy,population_light)
    assert len(population_heavy) == len(population_light)
    for hl_i in range(0,len(population_heavy)):
         if  population_light[ hl_i ] != 0.0 and population_heavy[ hl_i ] != 0.0:
             tmp_float = log(  population_heavy[ hl_i ] / population_light[ hl_i ] ,2)
             ratio_lines.append( str(tmp_float)  ) 
         else:
             ratio_lines.append( "0.0" )

    out_list.append( "\t".join(ratio_lines) )

of = open(file_name+".heavylight_ratios.txt",'w')
of.write("\n".join(out_list))
of.close()
