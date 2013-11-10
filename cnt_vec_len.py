

import argparse
from glob import glob

parser = argparse.ArgumentParser()

parser.add_argument('--file_set',
    help='''The name of a fasta formatted file. ''',
    required=True)
args = parser.parse_args()
file_set         = args.file_set

last_len = None
for file_name in sorted( glob(file_set) ):
    prev_vec_len  = None
    same_len = True 
    for line in open(file_name,'r'):
        vec_len = len(line.split())
        if prev_vec_len == None: prev_vec_len = vec_len
        if vec_len != prev_vec_len: same_len = False
        prev_vec_len = vec_len
    print( file_name+"\t"+str(same_len)+"\t"+str(vec_len) )
    
