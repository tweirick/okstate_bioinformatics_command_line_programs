'''
fasta_intersection_or_complement.py
@Created on: 4/2/2012
@author: Tyler Weirick
@language:Python 3.2
@tags: fasta difference intersection set Relative Complement Symmetric Difference
                        
Does various set operations, will print the output to screen. 
I = intersection i.e. The things that are only in both.
R = Relative Complement of B i.e. the things that are in A that are not in B.
S = Symmetric Difference - the things that  unique to each.
U = Union - Everything that is in A and everything that is in B.
TODO - Need to add error checking. 
'''
import sys
from optparse import OptionParser
import argparse
#This is the file of sequences you want to remove from file B or 
#Want to use to combine the sequences in common 

def getargs(ver='%prog 0.0'):
    """Gets file names for input and output 
    will use the first name and append out on the end of the file
    if no out-file name is given"""
    
    parser = argparse.ArgumentParser(description=__doc__,
                                      formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("--fasta_a_name", 
                      required=True,
                      help = "The name of the fasta file a.")

    parser.add_argument("--fasta_b_name", 
                      required=True,
                      help = "The name of the fasta file b.")
    
    parser.add_argument("--set_operation", 
                      default="U",
                      help = "The operation to preform.")
    
    args = parser.parse_args() 
    fasta_a_name  = args.fasta_a_name
    fasta_b_name  = args.fasta_b_name
    set_operation = args.set_operation

    return fasta_a_name,fasta_b_name,set_operation



def buildfastaset(fasta_file_name):
    '''
    This function makes a dictionary object from a fasta file. With the 
    sequence as the key and the name as the value. 
    '''
    fasta_set = set()
    
    fasta_name = ""
    fasta_data_list = []
    fasta_dict = dict()
    
    for line in open(fasta_file_name,'r'):
        
        #Two functions used make end of file and newline the same. 
        #Also to remove whitespace and newlines from data.
        line = line.strip()
        
        #print(''.join(fasta_data_list))
        #print(fasta_name)
        #print(fasta_dict)
        
        if len(line) == 0:
           #This is the end of the file, or a newline
           if fasta_name != "" and fasta_data_list != []:
               #Then a \n character was not encountered before end of file.
               fasta_dict.update({''.join(fasta_data_list):fasta_name})
               fasta_name,fasta_data_list = "",[]
        elif line[0] == ">":
            #This is the start of a fasta
            if fasta_name != "" and fasta_data_list != []:
                # Then not new fasta 

                fasta_dict.update({ ''.join(fasta_data_list) : fasta_name })
                fasta_name,fasta_data_list = "",[]
            fasta_name = line.strip()
            #fasta_data_list.append()
        else:
            #Must be fasta data
            fasta_data_list.append(line)
            
    
    if fasta_name != '' and fasta_data_list != []:
        fasta_dict.update({''.join(fasta_data_list):fasta_name})
        fasta_name,fasta_data_list = "",[]
    return fasta_dict

def dosetoperation(fasta_dict_A,fasta_dict_B,set_operation):
    """
    
    """
    
    fasta_set_a = set(fasta_dict_a.keys())    
    fasta_set_b = set(fasta_dict_b.keys())
    
    out_dict = dict()
    out_set = []
    
    if set_operation == "I":
        #I = intersection
      out_set = fasta_set_a.intersection(fasta_set_b)
    elif set_operation == "R":
        #R = Relative Complement of B
        #fasta_set_a.difference_update(fasta_set_b)
        out_set = fasta_set_a.difference(fasta_set_b)
    elif set_operation == "S":
        #S = Symmetric Difference
        out_set = fasta_set_a.symmetric_difference(fasta_set_b)
    elif set_operation == "U":
        # U = Union
        out_set = fasta_set_a | fasta_set_b
    else:
        print("Set Operation selector char not found.")
        
    return out_set
        
        
def add_names_to_output_set(fasta_dict_a,fasta_dict_b,output_set):
    """
    return set data as fasta file by adding name and converting to text.
    """
    out_fasta_list = []
    fasta_contig_name = ""
    
    for fasta_data in output_set:
        if fasta_data in fasta_dict_a:
            fasta_contig_name = fasta_dict_a[fasta_data]
            out_fasta_list.append("\n"+fasta_contig_name+"\n")        
            out_fasta_list.append(fasta_data)            
        elif  fasta_data in fasta_dict_b:
            fasta_contig_name = fasta_dict_b[fasta_data]
            out_fasta_list.append("\n"+fasta_contig_name+"\n")        
            out_fasta_list.append(fasta_data)

    return ''.join(out_fasta_list).strip()+"\n"



#=============================================================================
#                           Start Main Program
#=============================================================================
#fasta_a_file_name = "/home/tyler/fasta_a.faa"
#fasta_b_file_name = "/home/tyler/fasta_b.faa"
#set_operation = 'S'
fasta_a_file_name,fasta_b_file_name,set_operation = getargs(ver='%prog 0.2')
fasta_dict_a = buildfastaset(fasta_a_file_name)
fasta_dict_b = buildfastaset(fasta_b_file_name)
#print("Dicts created")
#print("Set a")
#print(fasta_dict_a)
#print("Set b")
#print(fasta_dict_b)
output_set = dosetoperation(fasta_dict_a,fasta_dict_b,set_operation)
#print(len(output_set))
out_txt = add_names_to_output_set(fasta_dict_a,fasta_dict_b,output_set)
print(out_txt)







        
        
        
        
