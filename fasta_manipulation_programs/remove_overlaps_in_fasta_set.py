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
    parser.add_argument('--blastclust_cluster_file_name',help='')
    args = parser.parse_args()
    return glob(args.file_set),args.blastclust_cluster_file_name

def make2Dlist(blastclust_clusters_file_name):
    clusters_2D_list = []
    for line in open(blastclust_clusters_file_name,'r'):
        split_line = line.split()        
        if len(split_line) > 1:
            clusters_2D_list.append(split_line)
    return clusters_2D_list

def buildfastadict(input_file_name):
    #Make a dictionary from the fasta file used for input.
    fasta_dict     = {}
    temp_fasta_seq = []
    fasta_name     = ""
    input_fasta_count = 0
    for line in open(input_file_name,'r'):
        if ">" in line:
            input_fasta_count+=1
            if fasta_name != "":
                try:
                    ID = fasta_name.split("|")[1]
                    
                    fasta_dict.update(
                        {ID:fasta_name+''.join(temp_fasta_seq)})
                except:
                    print(fasta_name)
                temp_fasta_seq = []
            fasta_name = line
        else:
            temp_fasta_seq.append(line)
    #Catch last entry
    try:
        ID = fasta_name.split("|")[1]
        fasta_dict.update( {ID:
                            fasta_name+''.join(temp_fasta_seq)
                            } )   
    except:
        print(fasta_name)
    return fasta_dict,input_fasta_count


def inremovedict(dict_el,clusters_2D_list):
    for list_el in clusters_2D_list:
         #print(dict_el,list_el)
         #ID = list_el.split("|")[1]
         if dict_el in list_el[0]:
             print(dict_el,list_el)
             return True
    return False
         
file_glob,blastclust_cluster_file_name = getargs(ver='%prog 0.0')
clusters_2D_list = make2Dlist(blastclust_cluster_file_name)
for file_name in file_glob:
    out_list = []
    fasta_dict,input_fasta_count = buildfastadict(file_name)    
    for dict_el in fasta_dict:
        #print(dict_el)
        if not inremovedict(dict_el,clusters_2D_list):
            out_list.append(fasta_dict[dict_el])
    out_file = open(file_name+".nonr.fasta",'w')
    out_file.write("".join(out_list))
    out_file.close()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    