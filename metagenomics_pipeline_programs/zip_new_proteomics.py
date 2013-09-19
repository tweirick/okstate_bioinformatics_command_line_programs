


fasta_file_name = "tmp_fastas"
comb_file_name = "blast_and_new_proteomics_data_largest_alignment31.csv"

description_dict = {}
species_dict = {}
for line in open(fasta_file_name,"r"):
    if line[0] == ">":
        for name in line.split(">"):
            if name != "":
                description_dict.update({name.split("|")[1]:[name.split("|")[-1].split("[")[0].strip(),name.split("|")[-1].split("[")[-1].split("]")[0].strip()]})
                #species_dict.update({name.split("|")[1]:})
                #print(name.split("|")[-1].split("[")[0].strip())
                #print(name.split("|")[-1].split("[")[-1].split("]")[0].strip())
                
out_list = []
for line in  open(comb_file_name,"r"):
    
   
        fasta_ID = line.split("`")[189]
        
        if len(fasta_ID.split("|")) >1:
            gi = fasta_ID.split("|")[1]
            if gi in description_dict:
                out_list.append(line.strip()+"`"+"`".join(description_dict[gi]))
            else:
                out_list.append(line.strip()+"`"+"`".join(["gi_not_mapped","gi_not_mapped"]))
        else:
            out_list.append(line.strip()+"`"+"`".join([fasta_ID,fasta_ID]))


out_file = open("new_protemoics_data_blast_and_uniprot_wPfam_and_EC.csv","w")
out_file.write("\n".join(out_list))
out_file.close()