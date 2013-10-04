
names_file = "specific_on_hints.txt" #"preds_IDs_from_98.fa.txt"#"noble_top_hits.txt"#"z1.txt"
fasta_file = "switchgrass_hints_pred_augustus.faa.pruneBJXZ.fasta.greaterthan61chars.faa"

name_list = []
for name_line in open(names_file,"r"):
    name_list.append(name_line.strip())


print_line = False
for fasta_line in open(fasta_file,"r"):
    if fasta_line[0] == ">":
         if fasta_line.strip() in name_list or fasta_line.strip(">").split()[0] in name_list:
             print_line = True
             print(fasta_line.strip())
         else:
             print_line = False
    elif print_line:
        print(fasta_line.strip())

        


 

