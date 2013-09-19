'''
@author: Tyler Weirick
@Created on: 8/4/2012 Version 0.0 
@language:Python 3.2
@tags: MASCOT flat-file blast zip

A program make for a specific task to zip two large flat files together. 

gene_id_458581.0        #0
gi|118365042|ref|XP_001015742.1| Zinc carboxypeptidase family protein [Tetrahymena thermophila] 
>gi|89297509|gb|EAR95497.1| Zinc carboxypeptidase family protein [Tetrahymena thermophila SB210] 
XP_001015742        # -3
53.:           # -2 
7.98084E-06         # -1 

AssertionError: gene_id_2128494.0    548    gi|42521743|ref|NP_967123.1|    60 kDa chaperonin [Bdellovibrio bacteriovorus HD100] >gi|59797773|sp|Q6MRI1.1|CH60_BDEBA RecName: Full=60 kDa chaperonin; AltName: Full=GroEL protein; AltName: Full=Protein Cpn60 >gi|39574273|emb|CAE77777.1| 60 KDA chaperonin [Bdellovibrio bacteriovorus HD100]    NP_967123    546    884.7892633    0
[TWeirick@bioinforesearch PRADE]$ python3 /home/TWeirick/PY_PROGRAMS/METAGENOME_PY_PROGS/zip_MASCOT_and_BLAST_flatfiles.py 
Traceback (most recent call last):
  File "/home/TWeirick/PY_PROGRAMS/METAGENOME_PY_PROGS/zip_MASCOT_and_BLAST_flatfiles.py", line 62, in <module>
    assert len(split_seqs) == 1,split_seqs
AssertionError: ['gi|42521743|ref|NP_967123.1| 60 kDa chaperonin [Bdellovibrio bacteriovorus HD100] ', 'gi|59797773|sp|Q6MRI1.1|CH60_BDEBA RecName: Full=60 kDa chaperonin; AltName: Full=GroEL protein; AltName: Full=Protein Cpn60 ', 'gi|39574273|emb|CAE77777.1| 60 KDA chaperonin [Bdellovibrio bacteriovorus HD100]']
vi 
BLAST_FLAT_FILE  = "PradeOutsTotal.blast"
MASCOT_FLAT_FILE = "1-126_pradefinal.dsv.flat.txt"#"PRADE_MASCOT_TOTAL_7-31-2012.dsv.peptide-byfile-comb.dsv"
OUTPUT_FILE_NAME = "1-126_pradefinal_mascot_and_blast_data_zipped_10.31.2012.dsv":
'''

from sys import exit

BLAST_FLAT_FILE  = "/home/TWeirick/PRADE/ghblast_11.3.2012.blast"
MASCOT_FLAT_FILE = "/home/TWeirick/PRADE/prade_final_mascot.csv"
OUTPUT_FILE_NAME = "/home/TWeirick/PRADE/mascot_and_blast_zipped_11.3.2012_3.dsv"
debug            = False 
#First test for no overlapping entries in the blast file. 

blast_geneID_line_data = {}

for line in open(BLAST_FLAT_FILE,'r'):
    
    line_split = line.split()
    if len(line_split) > 1:
        #Protect against empty lines.
        if len(line_split) < 1:
            pass
        
        gene_ID      = line_split[0]
        peptide_len1 = "NA"#line_split[1]
        
        seq_names = " ".join(line_split[1:-3])
    
        split_seqs = seq_names.split(">")
        
        split_pipe1 = split_seqs[0].split("|")
        print(split_pipe1)
        assert len(split_pipe1) >= 5,line
        sequence_ID_1 = "|".join(split_pipe1[0:4])+"|"
    
        
        peptide_len1 = " ".join(line_split[2:-3]).split("]")[0].split("[")[0]
        

        
    
        try:
            seq_name1 = split_pipe1[4].split("[")[0].strip()        
            print(seq_name1)
            seq_species1 = split_pipe1[4].split("[")[1].strip(" ").strip("]")
        except:
            print(line)
            seq_name1    = "No_Seq_Name"
            seq_species1 = "No_Seq_Name"
            
            
        other_stuff = " ".join(split_seqs[1:])
        
        GeneBank_ID  = line_split[-3]
        peptide_len2 = "NA"#line_split[-3]
        bit_score    = line_split[-2]
        e_val        = line_split[-1]
        
        if "]" in " ".join(line_split[2:-3]):
            species = " ".join(line_split[2:-3]).split("]")[0].split("[")[-1]
        else:
            species = "No Species"
        peptide_len2 = species
    
        if gene_ID in blast_geneID_line_data:
            #if gene_ID[0] != "Q":
            if debug:
                print("WARNING: Duplicate found.",gene_ID)
        else:
            #if gene_ID[0] == "g":
            #    print(gene_ID)
            if seq_name1 == "": seq_name1 = "No_Seq_Name"
            if seq_species1 == "":  seq_species1 ="No_Seq_Name"
            
            blast_data = [gene_ID, peptide_len1,sequence_ID_1,
                          seq_name1,seq_species1,other_stuff,GeneBank_ID,
                          peptide_len2,bit_score,e_val]
            joined_blast_data = "`".join(blast_data)
            
            blast_geneID_line_data.update({gene_ID:joined_blast_data})

not_found_dummy_list = []
for e in blast_data:
    not_found_dummy_list.append("No_Blast_Data")

output_list = []
for line in open(MASCOT_FLAT_FILE,'r'):
    
    split_line = line.split("`")
    if split_line[0] in blast_geneID_line_data:
        
        tmp_list = [split_line[0]] + [blast_geneID_line_data[split_line[0]]] + split_line[1:]
        
        output_list.append('`'.join(tmp_list))
    else:
        if debug:
            print(line)
        tmp_list = [split_line[0]]+not_found_dummy_list+split_line[1:]
        
        output_list.append('`'.join(tmp_list))

output_file = open(OUTPUT_FILE_NAME,'w')
output_file.write(''.join(output_list))
output_file.close()




