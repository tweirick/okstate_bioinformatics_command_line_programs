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
    parser.add_argument('--file_set', 
                        help='')
    args = parser.parse_args()
    return glob(args.file_set)


fasta_class_dict_list = []
for file_name in getargs():
    fasta_data = []
    temp_dict = {}
    file = open(file_name,'r')
    fasta_name = None
    while True:
        line = file.readline()
        if len(line) == 0 or line[0] == ">":
            
            if fasta_name != None:
                sequence = "".join(fasta_data)
                
                if sequence in temp_dict:
                    print("Redundant entry found.",fasta_name,
                    "and",temp_dict[sequence])
                else:
                    temp_dict.update({fasta_name:sequence})
                    #print(fasta_name.split("|")[1])
                    fasta_class_dict_list.append([file_name+"-"+fasta_name.split("|")[1],
                                                  file_name,
                                                  ">"+fasta_name.split("|")[1],
                                                  sequence])
            if len(line) == 0:break
            fasta_name = line.strip()#Get new name
            fasta_data = []          #Reset fasta data.
            sequence = ""
        else:
            fasta_data.append(line.strip())
    #fasta_class_dict_list.append([file_name,temp_dict])
    



cols = ["x"]
row_list = []
first_line = True
for fasta1 in sorted(fasta_class_dict_list):
    
    row_list = [fasta1[0]]
    for fasta2 in sorted(fasta_class_dict_list):
        
        #Make x column list.
        if first_line:
            cols.append(fasta2[0])

        #Make Temp File.
        temp_file = tempfile.NamedTemporaryFile(mode='w')
        temp_file.write(fasta1[2]+"\n"+fasta1[-1]+"\n"+fasta2[2]+"\n"+fasta2[-1])
        temp_file.flush()
        
        #Run CD-HIT
        out_file = tempfile.NamedTemporaryFile(mode='r')
        sub_str = "/home/tyler/cd-hit-v4.6.1-2012-08-27/cd-hit -i "+temp_file.name+" -o "+out_file.name+" -d 0 -c 0.40 -n 2"
        output = subprocess.getoutput(sub_str)  
        
        #Get Results should be one similarity per file. 
        similarity = "0.0"
        for line in open(out_file.name+".clstr","r"):
             if line[0] != ">" and len(line.split()) == 5:
                 similarity = line.split()[-1].strip("%")
        #Append similarity found to list.
        row_list.append(similarity)
        
        output = subprocess.getoutput("rm "+out_file.name+".clstr")
        temp_file.close()
        out_file.close()
        
    if first_line:
       print(",".join(cols)) 
       first_line = False

    print(",".join(row_list))
    
#print("\n".join(out_list))
            
            
            
            
            
            
            
            
            
        
