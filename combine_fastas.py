

from glob import glob
file_glob_name = "CDHIT_round4.faa.*of10.CDHIT40.faa"#"CDHIT_round4.faa.*of10.CDHIT40.faa"
#"CDHIT_round1.faa.*of100.CDHIT40.faa"
#"all_ec_numbers_no_laccase_like_16th.faa.*of300.CDHIT40.faa"
first_line = True
search_char = None

file_glob = glob(file_glob_name)

#file_glob = ["specific_negative_set_homology_5202013.2.xml.faa","specific_negative_set_5202013.2.xml.faa"]


for file_name in file_glob:
    for line in open(file_name,"r"):
        print(line.strip("\n"))
        
          
    
    
