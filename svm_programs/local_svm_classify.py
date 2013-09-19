#!/opt/python3/bin/python3
#It seems print statements will cause this not to work in the browser.

import sys, os, subprocess
import time
import json
import cgi
from glob import glob
import tempfile
from dipeptide import convertotosvm
#=============================================================================
#                          Constants and Varibles
#=============================================================================
DEBUG            = False 
MODEL_FILE_PATH  = "/var/www/cgi-bin/ligpred/MODEL_DIPEP_COMP/"
MODEL_FILE_REGEX = "*.rbfmodel"
MODEL_FILES      = MODEL_FILE_PATH+MODEL_FILE_REGEX
model_file_list = sorted(glob(MODEL_FILES))
#This directory will need to have it's ownership changed to the web servers
TEMP_DIR         = '/var/www/cgi-bin/ligpred/LIGPRED_TMP/'

file_glob = glob("PradeMeta300PlusFinalMetaMarkAminoAcids.fa.noErrorChars.*of200.fasta")
#file_glob = ["PradeMeta300PlusFinalMetaMarkAminoAcids.fa.noErrorChars.190of200.fasta"]


#=============================================================================
#                             Functions
#=============================================================================

#def classifysequence(contig_name,fasta_sequence):
def getfastanames(fasta_seqs):
    split_fasta_data = fasta_seqs.split("\n")
    fasta_names = []
    for line in split_fasta_data:
        if line == "":
            break
        elif line[0] == ">":
            fasta_names.append(line)
    return fasta_names

#=============================================================================
#                             Main Program
#=============================================================================


title=["Sequence ID"]#

for file_name in file_glob:
    
    prog_result         = {}
    vector_str          = ""
    fasta_data_is_valid =True
    score_matrix = []
    file = open(file_name,"r")
    fasta_seqs = file.read()
    file.close()
    
    fasta_names = getfastanames(fasta_seqs)
    
    
    vector_str = convertotosvm(file_name,'0')
    
    example_file = tempfile.NamedTemporaryFile(mode='w', prefix=TEMP_DIR)  
    example_file.write(vector_str)  
    example_file.flush()

    
    
    for model_file in model_file_list:
        
        title.append(model_file.split(".")[0].split("/")[-1])
        
        score_out_file = tempfile.NamedTemporaryFile(mode='r')#, prefix='')
        
        sub_str = ("/var/www/cgi-bin/ligpred/./svm_classify "+
                   example_file.name+" "+model_file+" "+score_out_file.name)
   
        output = subprocess.getoutput(sub_str)  

        tmp_format_list = score_out_file.read()
        
        tmp_format_list = tmp_format_list.split()
        
        score_out_file.close()#--------------------------------------------------
        score_matrix.append(tmp_format_list)
     
    example_file.close()#--------------------------------------------------
    
    score_matrix = [fasta_names] + score_matrix

    score_matrix = zip(*score_matrix)#     coo
    score_matrix = list( map(lambda x: ':'.join(x),score_matrix) ) 
    
    #Find largest value in column, if largest val is negative then Unknown.
    title.append("Prediction")
    
    for i in range(0,len(score_matrix)):
        
        split_line = score_matrix[i].split(":")
        largest_value = None
        element_pos   = None
    
        j=0
        for val in split_line[1:]:
            float_val = float(val)
            
            if largest_value == None:
                largest_value = float_val
                element_pos   = j
            else:
                if float_val > largest_value:
                    largest_value = float_val
                    element_pos   = j
            j+=1
        if largest_value < 0:
            score_matrix[i] = score_matrix[i]+":"+"UNKOWN"
        else:            
            score_matrix[i] = score_matrix[i]+":"+title[element_pos+1]
    
    score_matrix = [":".join(title)] + score_matrix
    
    out_table_str ="\n".join(score_matrix)
    
    
    print(out_table_str)

