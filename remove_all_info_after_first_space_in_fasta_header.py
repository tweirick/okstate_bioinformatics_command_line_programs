'''
@author: Tyler Weirick
This program remove all data after the first space in a fasta. It is 
important to uses with interproscan as certain characters can cause 
interproscan to fail. (ex: colons :)
'''
from glob import glob

import argparse

parser = argparse.ArgumentParser(
   description=open(__file__).read().split("'''")[1],
   formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('--file_glob',
help='''The name of a fasta formatted file. ''',
required=True)

args = parser.parse_args()
file_glob       = glob(args.file_glob)



for file_name in file_glob: 

    out_list = []
    for line in open(file_name,'r'):
        if line[0] == ">":
            out_list.append(line.split()[0]+"\n")
        else: 
            out_list.append(line)

    of=open(file_name+".fsp.fasta",'w')
    of.write( "".join(out_list) )
    of.close()

