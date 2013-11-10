'''
blastclust_set_run_and_output_fasta_and_log.py
@author: Tyler Weirick
@Created on: 6/08/2012 Version 0.0 
@language:Python 3.2
@tags: blastclust fasta 

This program was made to take a blastclust cluster file made from a 
blastclust run of some fastas that have already been run through blastclust.
the program will then make new fasta files with the overlaps removed.
'''

import argparse
from glob import glob

def getargs(ver='%prog 0.0'):

    parser = argparse.ArgumentParser(description='')    
    parser.add_argument('--file_set', help='')
    args = parser.parse_args()
    return glob(args.file_set)


#Get file names. 
file_name_glob = getargs()

#For all files in the set make a set of fastas 
dict_of_fasta_dicts = {}
for file_name in file_name_glob:
    file = open(file_name,'r')
    fasta_name = None
    temp_dict = {}
    while True:
        line = file.readline()
        if len(line) == 0 or line[0] == ">":
            if fasta_name != None:
                sequence = "".join(fasta_data)
                if sequence in temp_dict:
                    print("Redundant entry found.",fasta_name,
                          "and",temp_dict[sequence])
                else:
                    temp_dict.update({sequence:fasta_name})
                
            if len(line) == 0:
                break
            fasta_name = line.strip()#Get new name
            fasta_data = []          #Reset fasta data. 
        else:
            fasta_data.append(line.strip())
    dict_of_fasta_dicts.update({file_name:temp_dict})
    
        
#Now we should have a dictionary of the input fastas 
print(sorted(dict_of_fasta_dicts.keys() ))
overlaps_matrix_list_cols = [ ",".join( ["x"] + sorted(dict_of_fasta_dicts.keys() ) )   ]

for fasta_file_name1 in sorted(dict_of_fasta_dicts.keys()):     
    
    
    file_data1 = set(dict_of_fasta_dicts[fasta_file_name1])
    overlaps_matrix_list_rows = [fasta_file_name1]
    for fasta_file_name2 in sorted(dict_of_fasta_dicts.keys()):
        
        if fasta_file_name1 != fasta_file_name2:
            file_data2 = set(dict_of_fasta_dicts[fasta_file_name2])
            #Find intersection to discover overlaps.
            overlaps = file_data1 & file_data2
            overlaps_matrix_list_rows.append(str(len(overlaps)))
            #Find difference to get a unique fasta file. 
            file_data1 = file_data1 - file_data2
        else:
            overlaps_matrix_list_rows.append("-")

    overlaps_matrix_list_cols.append( ",".join(overlaps_matrix_list_rows) )
    
    #print("\n".join(overlaps_matrix_list_cols))
    
    #output to file.
    out_list = []
    for nonr_seq in file_data1:
        #fasta_name  
        out_list.append(dict_of_fasta_dicts[fasta_file_name1][nonr_seq])
        #fasta_seq 
        out_list.append(nonr_seq)
    
    outfile = open(fasta_file_name1+".nooverlap.faa",'w')
    outfile.write("\n".join(out_list))
    outfile.close()
    
    
print("\n".join(overlaps_matrix_list_cols))    
    
 
