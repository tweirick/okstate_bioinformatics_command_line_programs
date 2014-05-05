
out_dict       = {}
dont_keep_dict = {}

tmp_ec_list = []
existance = ""

#file_glob = ["uniprot_sprot.dat","uniprot_trembl.dat"]
file_glob = ["uniprot_sprot.dat"]

for file_name in file_glob:
    for line in open(file_name,'r'):
        sp_line = line.split()
        if sp_line[0] == "ID":
            if len(tmp_ec_list) > 0:
                if len(tmp_ec_list) == 1:
                   tmp_el = tmp_ec_list[0]
                    
                   if not "-" in tmp_el and not  existance == None and not seq_id == None:
                       
                       if tmp_el in out_dict and existance in out_dict[tmp_el]:
                           out_dict[tmp_el][existance]+=1
                       else: 
                           out_dict.update( {tmp_el:{"1":0 ,"2":0 ,"3":0 ,"4":0 ,"5":0 } } )
                           out_dict[tmp_el][existance]+=1
                           #out_dict.update({tmp_ec:{existance:1}})

                else:
                    for tmp_el in tmp_ec_list:
                        if not "-" in tmp_el and not  existance == None and not seq_id == None:
                            if tmp_el in dont_keep_dict and existance in dont_keep_dict[tmp_el]:
                                dont_keep_dict[tmp_el][existance]+=1
                            else:
                                dont_keep_dict.update( {tmp_el:{"1":0 ,"2":0 ,"3":0 ,"4":0 ,"5":0 } } )
                                dont_keep_dict[tmp_el][existance]+=1
            tmp_ec_list = []

        if sp_line[0] == "ID":
            try:
                seq_id = sp_line[1]
            except: 
                seq_id = None
        if sp_line[0] == "DE" and "EC=" in line:
            tmp_ec_list.append(sp_line[-1].strip(";").strip("EC=")) 
            #print(sp_line[-1].strip(";").strip("EC=")) 
    
        elif sp_line[0] == "PE": 
            try: 
                existance = sp_line[1].strip(":")      
            except:
                 existance = None
                 #print(seq_id,line,sp_line) 

    #PE   1: Evidence at protein level;
    #PE   2: Evidence at transcript level;
    #PE   3: Homology;
    #PE   4: Predicted;
    #PE   5: Uncertain;

print(len(out_dict))
print(len(dont_keep_dict))
good_set =  set(out_dict) - set(dont_keep_dict)   
print(len(good_set))


for set_el in sorted(good_set):
   print(set_el,end="\t")
   for i in {"1":0 ,"2":0 ,"3":0 ,"4":0 ,"5":0 }:
        print(out_dict[set_el][i],end="\t")
   else:
       print(out_dict[set_el][i],end="\n")






