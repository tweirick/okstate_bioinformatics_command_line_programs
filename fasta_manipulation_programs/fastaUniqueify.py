'''
Created on Nov 1, 2011 @author: Tyler Weirick
This program is made to do simple checks on a fasta file to find redundant 
contigs. The program first does a simple string to string equality check. If a
string is found to the contig lower in the file will be deleted and it's name 
will be appended to the end of the higher contigs name.

Next the contigs will be sorted based on decreasing size. 

Finally smaller contigs will be checked against larger contigs to determine if
the smaller contigs are subsets of the larger contigs. In this case the 
smaller contigs will be deleted and as before their names will be appended to
the end of the kept contigs.
'''


def make2Dfastalistfromfile(file_list):
    
    rtn_list = []

    for file in file_list:
        temp_contig_name = "" 
        temp_contig_data = []
        for line in open(file,'r'):
            if line != "":
                if line[0]==">":
                    if temp_contig_name != "":
                        
                        tmp_str = ''.join(temp_contig_data)
                        rtn_list.append( [len(tmp_str),temp_contig_name, tmp_str] )
                                          
                        temp_contig_data = []
                    temp_contig_name = line.replace("\n","")
                else:
                    temp_contig_data.append(line.replace("\n",""))
        tmp_str = ''.join(temp_contig_data)
        rtn_list.append( [len(tmp_str),temp_contig_name, tmp_str] )
    rtn_list.sort()
    return rtn_list
        
        
def removeidenticalandsubsequences(fasta_2D_list):
    
    i = 0
    j = 0
    while i < len(fasta_2D_list):
        
        search_term = fasta_2D_list[i][2]
        j = i+1
        while j < len(fasta_2D_list):
            
            if fasta_2D_list[j][2] == search_term:
                #append name 
                fasta_2D_list[i][1] = fasta_2D_list[i][1] + " IDENTICAL_TO " + fasta_2D_list[j][1]
                del fasta_2D_list[j]
                
            j+=1
        i+=1       

    i = 0
    j = 0
    #Since sequences were sorted small to large reverse
    fasta_2D_list.reverse()
    
    
    while i < len(fasta_2D_list):
        search_term_len = fasta_2D_list[i][0]
        search_term = fasta_2D_list[i][2]
        j = i+1
        while j < len(fasta_2D_list) and search_term_len < (fasta_2D_list[j][0]*1.5):
            if fasta_2D_list[j][2] in search_term:
                
                #append name 
                fasta_2D_list[i][1] = fasta_2D_list[i][1] + " CONTAINS_SUBSEQ " + fasta_2D_list[j][1]
                del fasta_2D_list[j]
                
            j+=1
        i+=1       
    return fasta_2D_list


file_list = ["LO1_uniprot_and_foly.fasta_psi-blast_e1e-40_j3_dnr.3.20.2012.GI.from_psi-blast.faa"]    
fasta_2D_list = make2Dfastalistfromfile(file_list)

fasta_2D_list = removeidenticalandsubsequences(fasta_2D_list)    
#fasta_2D_list = removesubsets(fasta_2D_list)

for e in fasta_2D_list:
    print(e)
        
    
