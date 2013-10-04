

file_name = "specific_positive_set_5202113.3.xml.faa.CDHIT100.faa.DB_uniprot_all_w_eval_and_name.faa.e-40.psiblast7"#"ab_initio_switchgrass_protein_preds.faa.blastp"#"all_switchgrass_transcripts1.fna.blastx"


for line in open(file_name,"r"):
    if line[0] != "#":
        print(line.strip("\n"))
