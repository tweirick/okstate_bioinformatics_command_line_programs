'''
Make a matrix of fasta sequences with 
'''
import sys
import argparse
from glob import glob
import tempfile
import sys, os, subprocess

def getargs(ver='%prog 0.0'):
    parser = argparse.ArgumentParser(description='')    
    parser.add_argument('--file_set', help='A set of fasta files.')
    parser.add_argument('--cd_hit', help='a cd-hit file')
    args = parser.parse_args()
    return glob(args.file_set),args.cd_hit


#Read fasta class files 
fasta_file_names,cdhit_file_name = getargs()


fasta_file_dict = {}
out_fasta_dict = {}
for file_name in fasta_file_names:
    out_fasta_dict.update({file_name:[]})
    fasta_data = []
    #temp_dict  = {}
    file       = open(file_name,'r')
    fasta_name = None
    while True:
        line = file.readline()
        if len(line) == 0 or line[0] == ">":
            if fasta_name != None:
                sequence = "".join(fasta_data)        
                id = fasta_name.split("|")[1]    
                fasta_file_dict.update({id:[file_name,fasta_name,sequence]})
            if len(line) == 0:break
            fasta_name = line.strip()#Get new name
            fasta_data = []          #Reset fasta data.
            sequence = ""
        else:
            fasta_data.append(line.strip())
    
 


#Read cd-hit file. 100.00%
cluster_list = []
single_element_clusters = []
round_cluster_contents = []
for line in open(cdhit_file_name,"r"):
    
    if line[0] == ">":
        if len(round_cluster_contents) == 1:
            single_element_clusters.append(round_cluster_contents)

            tmp_ID = round_cluster_contents[0].split("|")[1]
            write_to_file_name = fasta_file_dict[tmp_ID][0]
            out_fasta_dict[write_to_file_name].append(fasta_file_dict[tmp_ID][1])
            out_fasta_dict[write_to_file_name].append(fasta_file_dict[tmp_ID][2])
            del fasta_file_dict[tmp_ID]
        elif len(round_cluster_contents) > 1:
            #print(round_cluster_contents)
            cluster_list.append(round_cluster_contents)
        round_cluster_contents = []
    else:#Is a cluster. 
        ID         = line.split()[2]
        similarity = line.split()[-1]
        if similarity == "100.00%":
            #print(""" WARNING: 100.00% sequence similarity found. This program 
            #was not written to handle this type of data. Thus you could C8T3H7
            #experience unexpected results. Please check the program and 
            #your data. """)
            round_cluster_contents = []
        else:
            round_cluster_contents.append(ID)
            

#Assign non-clustered files to lists.
for cluster in cluster_list:
    smallest_class             = None
    smallest_fasta_name        = None
    name_of_smallest_class     = None
    sequence_of_smallest_class = None
    
    for clustered_sequence in cluster:
        tmp_ID_clustered_sequence     = clustered_sequence.split("|")[1]
        file_name,fasta_name,sequence = fasta_file_dict[tmp_ID_clustered_sequence]
        sequences_in_class            = len(out_fasta_dict[file_name])
        
        if smallest_class == None or sequences_in_class < smallest_class:
            smallest_class             = sequences_in_class
            smallest_fasta_name        = fasta_name
            name_of_smallest_class     = file_name
            sequence_of_smallest_class = sequence
            
    out_fasta_dict[name_of_smallest_class].append(smallest_fasta_name)
    out_fasta_dict[name_of_smallest_class].append(sequence_of_smallest_class)
    


for prot_class in out_fasta_dict:
    file = open(prot_class+".smart_cluster_assignment.faa",'w')
    file.write("\n".join(out_fasta_dict[prot_class]))
    file.close()



