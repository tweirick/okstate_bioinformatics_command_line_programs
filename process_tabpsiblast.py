
file_name = "specific_positive_set_5202113.3.xml.faa.CDHIT100.faa.DB_uniprot_all_w_eval_and_name.faa.e-40.psiblast7" #"ab_initio_switchgrass_protein_preds.faa.blastp"
#"laccases_neg_set.e-40.psiblast"
get_name = False


for line in open(file_name,'r'):
    line = line.strip()
    if len(line.strip()) > 0:
        
        if "# Iteration: 1" in line:
            get_name = True
        elif get_name:
            get_name = False
            print(line)
            query_name = line.split("|")[1]
                    
        if line[0] != "#" and not "Search has CONVERGED!" in line: 
            seq_id = line.split()[1].split("[")[0]
            data   = line.split()[1].split("[")[1].strip("]")
              
            if data[0] == "@":
                #no evalue
                prot_name = data.replace("&nbsp;"," ").strip("@name")
                evals    = ["No_eval"]
            else:
                prot_name = data.split("@name")[1].replace("&nbsp;"," ")
                evals     = data.split("@name")[0].split(",")
            
            print(query_name+"\t"+seq_id+"\t"+prot_name+"\t"+"#".join(evals))
            
