from glob import glob

"""
# PSIBLAST 2.2.27+
# Iteration: 1
# Query: sp|O13970|RT04_SCHPO 37S ribosomal protein mrp4, mitochondrial OS=Schizosaccharomyces pombe (strain 972 / ATCC 24843) GN=mrp4 PE=3 SV=2
# Database: uniprot_fixed_data_all_tax_with_plastid.xml.subcell.faa
# Fields: query id, subject id, % identity, alignment length, mismatches, gap opens, q. start, q. end, s. start, s. end, evalue, bit score
# 90 hits found
sp|O13970|RT04_SCHPO    Q4G3A3[plastid,chloroplast]     33.63   226     125     3       48      248     4       229     2e-37    134
sp|O13970|RT04_SCHPO    Q9TM33[plastid,chloroplast]     35.06   231     128     3       47      255     2       232     4e-37    134

"""


def makebinarypsiblastvector( binary_classificaiton,localization_list ): 
    
    if "NO_HIT" in localization_list or "NO_LOCALIZATION" in localization_list:
        return "0 0 1"
    
    for loc in localization_list:
        for cterm in binary_classificaiton: 
            if loc in cterm or loc == cterm:
                return "1 0 0"   
    return "0 1 0"


def makemultipsiblastvector(localization_list):
    multi_classificaiton = { "plastid"    :"0", "chloroplast":"0",
                             "chromoplast":"0", "etioplast"  :"0", 
                             "amyloplast" :"0", 
                             "NOT_PLASTID":"0", "NO_HIT"     :"0",
                             "NO_LOCALIZATION":"0"  }
    
    class_terms  = [ "amyloplast" ,"chloroplast",
                     "chromoplast" ,"etioplast",
                     "plastid" 
                     ]
    
    plastid_relation_found = False
    for e in localization_list:
        for f in class_terms:
            if e in f:
                multi_classificaiton[f] = "1"
                plastid_relation_found = True
    
    if "NO_LOCALIZATION" in localization_list:
        multi_classificaiton["NO_LOCALIZATION"] = "1"
    elif "NO_HIT"  in localization_list:
        multi_classificaiton["NO_HIT"]          = "1"
    elif not plastid_relation_found:
        multi_classificaiton["NOT_PLASTID"]     = "1"
                
    out_list1 = []
    for e in sorted(list(multi_classificaiton)):
        out_list1.append( multi_classificaiton[e] )
        
    return " ".join(out_list1)


def makemultiNclassesPlus1psiblastvector(localization_list):
    multi_classificaiton = { "chloroplast":"0",
                             "chromoplast":"0", 
                             "etioplast"  :"0", 
                             "amyloplast" :"0", 
                             "other":"0",  }
    
    class_terms  = [ "amyloplast" ,"chloroplast",
                     "chromoplast" ,"etioplast",

                     ]
    
    plastid_relation_found = False
    for e in localization_list:
        for f in class_terms:
            if e in f:
                multi_classificaiton[f] = "1"
                plastid_relation_found = True
    
    if "NO_LOCALIZATION" in localization_list:
        multi_classificaiton["other"] = "1"
    elif "NO_HIT"  in localization_list:
        multi_classificaiton["other"]          = "1"
    elif not plastid_relation_found:
        multi_classificaiton["other"]     = "1"
                
    out_list1 = []
    for e in sorted(list(multi_classificaiton)):
        out_list1.append( multi_classificaiton[e] )
        
    return " ".join(out_list1)







binary_classificaiton = ["plastid","chloroplast","chromoplast","etioplast","amyloplast","elaioplast" ]
keep_percent_identity = 100.00
prev_iter_num = 0

#multi_class_plastid_etio.faa
#new_*_2844.*.psiblast7
#multi_class_plastid_chloro.faa.e-6.psiblast7
for file_name in glob("*.psiblast7.1"):
    print(file_name)
    out_list      = []
    multi_outlist = []
    other = []
    for line in open(file_name,"r"):
        line = line.strip()
        if len(line) > 0:
            
            if line[0] == "#": 
                if "Iteration:" in line or "# BLAST processed " in line:
                    
                    if  "# BLAST processed " in line:
                        iteration_num = prev_iter_num
                    else:     
                        iteration_num = int(line.strip("# Iteration: "))
                    
                    if iteration_num <=  prev_iter_num: 
                        #print(iteration_num,prev_iter_num,keep_ID,keep_localization_list)
                        #New line save data
                        #print(iteration_num,keep_percent_identity,keep_localization_list)
                        out_list.append( keep_ID+" "+makebinarypsiblastvector( binary_classificaiton,keep_localization_list ) )

                        multi_outlist.append( keep_ID+" "+makemultipsiblastvector( keep_localization_list ) )                        
                  
                        other.append(keep_ID+" "+makemultiNclassesPlus1psiblastvector(localization_list))
                        keep_percent_identity = 100.00 
                        keep_localization_list = []
                        keep_localization_list = ["NO_HIT"]
                    prev_iter_num = iteration_num
                elif "# 0 hits found" in line and iteration_num == 1:
                    #print(keep_ID,line)
                    keep_localization_list = ["NO_HIT"]
          
                elif "# Query:" in line and  iteration_num == 1:
                    keep_ID   = line.strip("# Query:").split()[0].strip()   
            
            elif not "Search has CONVERGED!" in line:
                
                split_line = line.split() 
                vec_ID = split_line[1]
                localization_list = split_line[1].split("[")[-1].strip("]").split(",")
                
                percent_identity  = float(split_line[2])
                
                if keep_percent_identity == 100.00: 
                    #print("!",localization_list)
                    #print(split_line,localization_list,percent_identity)
                    keep_localization_list = localization_list
                    keep_percent_identity  = percent_identity
                
    outfile = open(file_name+".multipsiblast.vec",'w')
    outfile.write("\n".join(multi_outlist))
    outfile.close()

    outfile = open(file_name+".binpsiblast.vec",'w')
    outfile.write("\n".join(out_list))
    outfile.close()

    outfile = open(file_name+".Nplus1psiblast.vec",'w')
    outfile.write("\n".join(other))
    outfile.close()

                                
multi_classificaiton = {"plastid"    :"0", "chloroplast":"0",
                        "chromoplast":"0", "etioplast"  :"0", 
                        "amyloplast" :"0", "elaioplast" :"0",
                        "NOT_PLASTID":"0", "NO_HIT"     :"0",
                        "NO_LOCALIZATION":"0"  }

print(sorted(list(multi_classificaiton)))




n = { "chloroplast":"0",
                             "chromoplast":"0", 
                             "etioplast"  :"0", 
                             "amyloplast" :"0", 
                             "other":"0",  }
print(sorted(list(n)))



