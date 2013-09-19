'''
@author: Tyler Weirick 
@Created on: 6/11/2012 Version 0.0 @change: 7/16/2012 
@language:Python 3.2
@tags: five-fold split splitter fasta
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

#=============================================================================
#                           Functions 
#=============================================================================

def getheadcomments():
    """
    This function will make a string from the text between the first and 
    second ''' encountered. Its purpose is to make maintenance of the comments
    easier by only requiring one change for the main comments. 
    """
    desc_list = []
    start_and_break = "'''"
    read_line_bool = False
    #Get self name and read self line by line. 
    for line in open(__file__,'r'):
        if read_line_bool:
            if not start_and_break in line:
                line_minus_newline = line.replace("\n","")
                space_list = []
                #Add spaces to lines less than 79 chars
                for i in range(len(line_minus_newline),80):
                     space_list.append(" ")
                desc_list.append(line_minus_newline+''.join(space_list)+"\n\r")
            else:
                break    
        if (start_and_break in line) and read_line_bool == False:
            read_line_bool = True
    desc = ''.join(desc_list)
    return desc

def getargs(ver='%prog 0.0'):
    """
    This function handles the command line input for the program.
    In this case we need an input set and an integer to tell us 
    the number of files to split the original file(s) into.
    """
    desc = getheadcomments()
    
    parser = argparse.ArgumentParser(description=desc)    
    parser.add_argument('--file_set', 
                        help='')
    parser.add_argument('--number_of_parts', 
                        help='Input as a integer.')#?
    
    args = parser.parse_args()
    return sorted(glob(args.file_set)),args.number_of_parts
    

def buildfastalist(fasta_file_name):
    '''
    INPUT:
    fasta_file_name(str) - The name of a single fasta file. 
    OUTPUT:
    returns a list of fasta entries with one list element corresponding to 
    one fasta entry.
    '''
    fasta_list      = []
    temp_fasta_name = ""
    temp_fasta_data = []
    
    for line in open(fasta_file_name,'r'):
        #Two functions used make end of file and newline the same. 
        #Also to remove whitespace and newlines from data.
        if line[0] == ">":
            if temp_fasta_name != "":
                fasta_list.append(temp_fasta_name+"".join(temp_fasta_data))
            temp_fasta_name = line
            temp_fasta_data = []
        else:
            temp_fasta_data.append(line)
            
    fasta_list.append(temp_fasta_name+"".join(temp_fasta_data))
    return fasta_list


def splitandoutput(fasta_list,file_name_base,parts):
    """
    INPUT: 
    fasta_list(list) - A list of fasta entries.
    file_name_base(str) - The name of the input file. The output file will be 
                          named with this plus a suffix added in this function. 
    parts(str) or (int) - The number of parts to convert the input file to. 
    OUTPUT: A set of fasta files to hard disk. 
    
    This function will make (parts) number of new fasta files from a fasta 
    file and write them to the hard disk.
    """
    seq_len =  len(fasta_list)
    parts = int(parts)

    sequences_per_part = int( ceil(float(seq_len)/float(parts) ))
    print("file_name:",file_name_base,
          "Number_of_Seqs:",seq_len,"Seqs per part",
          sequences_per_part)
    
    seqs_output = 0
    start       = 0
    stop        = 0
    rollover = seq_len - sequences_per_part*parts
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
        
        out_file = open(tmp_file_name,'w')
        out_file.write(tmp_output_str)
        out_file.close() 

#=============================================================================
#                           Start Main Program
#=============================================================================

file_glob,split_percentage = getargs()

for file_name in file_glob:
        
    fasta_list = buildfastalist(file_name)
    
    splitandoutput(fasta_list,file_name,split_percentage)
    
        
        
        
        
        
        
        
        
        
