'''
@author: Tyler Weirick 
@Created on: 6/11/2012 Version 0.0 @change:
@language:Python 3.2
@tags: five-fold percentage split splitter fasta
This program accepts a file name or regular expression describing a set of 
fasta files and a float
'''

import sys
import argparse
from glob import glob
from math import ceil
#This is the file of sequences you want to remove from file B or 
#Want to use to combine the sequences in common 


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

    desc = getheadcomments()
    
    print(desc)
    
    parser = argparse.ArgumentParser(description=desc)    
    parser.add_argument('--file_set', 

                        help='')
    parser.add_argument('--split_percentage', 
                        help='Input as a decimal.')
    
    args = parser.parse_args()
    return sorted(glob(args.file_set)),args.split_percentage
    

def buildfastalist(fasta_file_name):
    '''
    This function makes a dictionary object from a fasta file. With the 
    sequence as the key and the name as the value. 
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


def splitandoutput(fasta_list,file_name_base,percent):
    
    percent_float = float(percent)
    other_percent = 1.0 - percent_float
    
    number_to_exclude = int(round(len(fasta_list)*percent_float))
    
    number_to_keep    = abs(len(fasta_list) - number_to_exclude)
    
    #print(file_name_base,number_to_exclude)
    file_a_list = fasta_list[:number_to_exclude]
    file_b_list = fasta_list[number_to_exclude:]
    print(file_name_base+"\t"+str(len(file_a_list))+"\t"+str(len(file_b_list)),)
    #print("Fastas in file a:",len(file_a_list))
    #print("Fastas in file b:",len(file_b_list))
    
    
    for e in file_a_list:
        if len(e) != 0:
            if e[0] != ">":
                print("ERROR: non-standard element")
                print(e)
        else:
            print("empty set found.")
            
    out_file = open(file_name_base+"."+str(percent_float)+".fasta",'w')
    out_file.write("".join(file_a_list))
    out_file.close()
    
    out_file = open(file_name_base+"."+str(round(other_percent,2))+".fasta",'w')
    out_file.write("".join(file_b_list))
    out_file.close()
    
    
    
#=============================================================================
#                           Start Main Program
#=============================================================================

file_glob,split_percentage = getargs()
print("Class\t#_in_File_A\t#_in_File_B")
for file_name in file_glob:
    
    fasta_list = buildfastalist(file_name)
    
    splitandoutput(fasta_list,file_name,split_percentage)
    
    
        
