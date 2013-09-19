'''
search_input_files_blastclust.py
This program takes a blastclust input and a set of fasta files.
It will print out all of the conections between files for each cluster. 
'''
import sys
import argparse
from glob import glob

def getargs(ver='%prog 0.0'):

    parser = argparse.ArgumentParser(description='')
        
    parser.add_argument('--file_set', 
                        help='')
    
    parser.add_argument('--blastclust_clusters_file_name', 
                        help='')
    
    args = parser.parse_args()
    return glob(args.file_set),args.blastclust_clusters_file_name
    

def countfastas(fasta_file_name,search_string):
    '''

    '''
    fasta_number = 0    
    for line in open(fasta_file_name,'r'):
        #Two functions used make end of file and newline the same. 
        #Also to remove whitespace and newlines from data.
        if search_string in line:
            print(search_string,"found in",fasta_file_name)
            
    return fasta_number


#=============================================================================
#                           Start Main Program
#=============================================================================

file_glob,blastclust_clusters_file_name = getargs()

#Get clusters
out_list = []
out_dict = {}
clusters_2D_list = []

for line in open(blastclust_clusters_file_name,'r'):
    split_line = line.split()
    if len(split_line) > 1:
        clusters_2D_list.append(split_line)

for el in clusters_2D_list:
    
    file_name_list = []
    
    for file_name in sorted(file_glob):
        
        #line will be fasta entry name or 
        for line in open(file_name,'r'):
            #An entry found in a cluster. 
            for el_1 in el:
                if el_1 in line:
                    if not file_name in file_name_list:
                        file_name_list.append(file_name)
                        
    sorted_output_str = " ".join(sorted(file_name_list))
    #print(len(file_name_list)," ".join(file_name_list),"from",len(el),"contigs")
    
    
    
    
    if sorted_output_str in out_list:
        out_dict[sorted_output_str]+=1
    else:
        out_list.append(sorted_output_str)
        out_dict.update({sorted_output_str:1})
        #print(sorted_output_str)    

#print(len(out_list))
for e in out_list:
    print(e,out_dict[e])    
    

        
        
        
        
        
        
        
        
        
        