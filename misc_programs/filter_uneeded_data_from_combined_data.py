



terms_file = "GO_terms_to_delete_from_mascot_data.txt"
removal_GO_terms_list = []
file_name             = "uniZzip.8-7.2012.txt"
keep_file_name        = file_name+".keep"
keep_file_list        = []
remove_file_name      = file_name+".exclude"
remove_file_list      = []

#Make list of terms which warrant removal
"""
If first element not zero then remove 
0       3-deoxy-8-phosphooctulonate synthase activity
0       3-deoxy-7-phosphoheptulonate synthase activity

"""
for line in open(terms_file,'r'):
    
    split_line = line.split("\t")
    if len(split_line) > 1:
        if split_line[0] != "0":
            #print(split_line[1].strip())
            removal_GO_terms_list.append(split_line[1].strip())
    else:
        print("ERROR",[line]) 
    


for line in open(file_name,"r"):

    no_removal_term_found = True 
    #get go terms
    split_line = line.split("`")
    #25-45
    if len(split_line) > 45:
        go_terms = split_line[24:45]
        for term in go_terms:
            cleaned_term = term.split(":")[-1]
            if cleaned_term in removal_GO_terms_list:
                no_removal_term_found = False 
                break 
        
        if no_removal_term_found:
            keep_file_list.append(line)
        else:
            remove_file_list.append(line)
    else:
        print("Aquisition Error.")
        
        
keep_file = open(keep_file_name,'w')
keep_file.write(''.join(keep_file_list))
keep_file.close()

exclude_file = open(remove_file_name,'w')    
exclude_file.write(''.join(remove_file_list))
exclude_file.close()



