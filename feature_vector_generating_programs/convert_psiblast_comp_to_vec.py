from glob import glob 

file_glob = glob("new_neg_2844.*.psiblast.comp")
correct_pred_term = "plastid"
POS_OR_NEG_FILE = False
NO_HIT_STR = "NO_HIT"
NO_SUBCELL_STR = "NO_LOC"

output_type = "SVM_LIGHT" #SPACED_VALS.

for file_name in file_glob:
    out_str = []
    for line in open(file_name,"r"): 
        sub_loc = " ".join(line.split()[2:])
        name = line.split()[0]
        if   POS_OR_NEG_FILE     and correct_pred_term == sub_loc:
            if output_type == "SVM_LIGHT":     out_str.append(name+" 1:1 2:0 3:0")
            elif output_type == "SPACED_VALS": out_str.append(name+" 1 0 0")
        elif not POS_OR_NEG_FILE and correct_pred_term == sub_loc:
            if output_type == "SVM_LIGHT":     out_str.append(name+" 1:0 2:1 3:0")
            elif output_type == "SPACED_VALS": out_str.append(name+" 0 1 0")
        elif POS_OR_NEG_FILE     and correct_pred_term != sub_loc:
            if output_type == "SVM_LIGHT":     out_str.append(name+" 1:0 2:1 3:0") 
            elif output_type == "SPACED_VALS": out_str.append(name+" 0 1 0")         
        elif not POS_OR_NEG_FILE and correct_pred_term != sub_loc:
            if output_type == "SVM_LIGHT":     out_str.append(name+" 1:1 2:0 3:0")
            elif output_type == "SPACED_VALS": out_str.append(name+" 1 0 0")
        elif NO_HIT_STR == sub_loc or NO_SUBCELL_STR == sub_loc:
            if output_type == "SVM_LIGHT":out_str.append(name+" 1:0 2:0 3:1")
            elif output_type == "SPACED_VALS":out_str.append(name+" 0 0 1")
            
    out_file = open(file_name+".psitri.vec","w")
    out_file.write("\n".join(out_str))
    out_file.close()