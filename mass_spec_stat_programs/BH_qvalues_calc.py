'''
@author: Tyler Weirick
@date: 2013-08-16
==============================================================================
==============================================================================
'''
from rpy2 import *
import rpy2.robjects as R
import rpy2.rpy_classic as rpy
import argparse

rpy.set_default_mode(rpy.NO_CONVERSION)
rpy.set_default_mode(rpy.BASIC_CONVERSION)

#Get arguments. 
parser = argparse.ArgumentParser()
parser.add_argument('--file_name',
                   help='Input the name of the file to be processed. ')
args = parser.parse_args()
file_name = args.file_name

pvalue_list = []
for line in open(file_name,'r'):
    pvalue_list.append( float(line.strip("\n") ))

pvalue = rpy.r.p_adjust( R.FloatVector( pvalue_list) ,method='BH')

out_list = []
for e in pvalue:
    #print(str(e))
    out_list.append(str(e))

of = open(file_name+".qvals.txt",'w')
of.write("\n".join(out_list))
of.close()
