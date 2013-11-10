'''
@author: Tyler Weirick 
@Created on: 6/11/2012 Version 0.0 @change: 7/16/2012 @change: 2013-10-31 
@language:Python 3.2
This program accepts a file name or regular expression describing a set of 
fasta files and an integer x. The program will output the contents of the 
original files in x parts denoted by the suffix .yofx.fasta where y is the one of 
the x parts. 

>tr|E8SBI1|E8SBI1_MICSL Esterase

'''
import sys
from sys import exit
from math import ceil
import argparse
from glob import glob
version = hash(open(__file__,'r').read())
print("version:"+str(version))
#=============================================================================
#                           Functions 
#=============================================================================

def getargs(ver='%prog 0.0'):
    """
    This function handles the command line input for the program.
    In this case we need an input set and an integer to tell us 
    the number of files to split the original file(s) into.
    """
    
    parser = argparse.ArgumentParser(description=__doc__)    
    parser.add_argument('--file_set',
                        required=True,
                        help='')
    parser.add_argument('--parts', 
                        required=True,
                        help='''
                        Input as a integer, the number of parts to split the 
                        fasta into.''')
    parser.add_argument('--out_path',
                        required=False,
                        default=None,
                        help='''
                        Path to output new files to. Can be left blank if the 
                        desired output location is the same as the input 
                        files.''')
                       
    args = parser.parse_args()
    
    #Get and validate input files. 
    file_set = args.file_set
    sorted_file_glob = sorted(glob(file_set))
    assert sorted_file_glob != [],"No files describe by file_set."

    #Get and validate number of parts. 
    try: 
        parts = int(args.parts)
    except:     
        print("Input for --parts not convertable to integer. EXITING.")
        exit()
 
    #todo: add validation to check existance of output file path. 
    out_path = args.out_path
    if out_path == None: 
        out_path = "/".join(file_set.split("/")[:-1])+"/"
             
    return sorted_file_glob,parts,out_path
    

def buildfastalist(fasta_file_name):
    '''
    INPUT:
    fasta_file_name(str) - The name of a single fasta file. 
    OUTPUT:
    returns a list of fasta entries with one list element corresponding to 
    one fasta entry.
    '''
    fasta_list      = []
    temp_fasta_name = None
    temp_fasta_data = []
    
    fasta_file = open(fasta_file_name,'r')

    while True: 
        line = fasta_file.readline() 
        if line == "" or line[0] == ">":
            if temp_fasta_name != None or line == "":
                fasta_list.append(temp_fasta_name+"".join(temp_fasta_data))
                if line == "":
                    break 
            temp_fasta_name = line
            temp_fasta_data = []
        else:
            temp_fasta_data.append(line)
            
    return fasta_list


def splitandoutput(file_name,parts,out_path):
    """
    INPUT:
    file_name_base(str) - The name of the input file. The output file will be 
                          named with this plus a suffix added in this function. 
    parts(str) or (int) - The number of parts to convert the input file to. 
    OUTPUT: A set of fasta files to hard disk. 
    
    This function will make (parts) number of new fasta files from a fasta 
    file and write them to the hard disk.
    """


    fasta_list = buildfastalist(file_name)    
    seq_len            = len(fasta_list)
    parts              = int(parts)
    sequences_per_part = int( ceil(float(seq_len)/float(parts) ))
    file_name_base     = file_name.split("/")[-1]     

    #Output some info about the split process. 
    print("file_name:",file_name_base,"Number_of_Seqs:",seq_len,
          "Seqs per part",sequences_per_part)
    
    seqs_output = 0
    start       = 0
    stop        = 0
    rollover    = seq_len - sequences_per_part*parts
    FASTA_SUFFIX = ".fasta"
    
    for i in range(1,parts+1):

        tmp_file_name = file_name_base+"."+str(i)+"of"+str(parts)+FASTA_SUFFIX

        if i == parts:
            #This handles the end case, by putting all files left over into
            #the last file. 
            start=stop
            tmp_output_str = "".join(fasta_list[start:])
            stop=seq_len
            print(tmp_file_name,start,stop,len(fasta_list[start:]))         
        else:        
            #All except final.
            stop+=sequences_per_part
            tmp_output_str = "".join(fasta_list[start:stop])
            print(tmp_file_name,start,stop,len(fasta_list[start:stop])) 
            start=stop
        
        out_file = open(out_path+tmp_file_name,'w')
        out_file.write(tmp_output_str)
        out_file.close() 

#=============================================================================
#                           Start Main Program
#=============================================================================

file_glob,n_parts,out_path = getargs()

for file_name in file_glob:        
    splitandoutput(file_name,n_parts,out_path)
    
        
        
        
        
        
        
        
        
        
