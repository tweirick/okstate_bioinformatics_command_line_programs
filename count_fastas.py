'''
count_fastas.py
'''
import sys
import argparse
from glob import glob

def getargs(ver='%prog 0.0'):

    parser = argparse.ArgumentParser(description='')    
    parser.add_argument('--file_set', 
                        help='')
    args = parser.parse_args()
    return glob(args.file_set)
    

def countfastas(fasta_file_name):
    '''

    '''
    fasta_number = 0    
    for line in open(fasta_file_name,'r'):
        #Two functions used make end of file and newline the same. 
        #Also to remove whitespace and newlines from data.
        if ">" in line:
            fasta_number+=1
    return fasta_number


#=============================================================================
#                           Start Main Program
#=============================================================================

file_glob = getargs()

for file_name in sorted(file_glob):
    
    print(file_name,countfastas(file_name))
    
    
        
