


file_name = "uniZzip.8-7.2012.txt"
output_dict = {}
for line in open(file_name,'r'):
    
    split_line = line.split("`")
    
    #25-45
    if len(split_line) > 45:
        
        go_terms = split_line[24:45]
        
        
        
        
        for term in go_terms:
            #print(go_terms[0],go_terms[-1])
            #loc,term_name = 
            if term != "No_GO_terms." and term != "No_data": 
                term = "".join(term.split(":")[1:]) 

                if term in output_dict:
                    output_dict[term]+=1
                else:
                    output_dict.update({term:1})
                
        


sort_list = []
for e in output_dict.keys():
    sort_list.append([e,output_dict[e]])
    
    
print_list = []
go_term_total = 0
for e in sorted(sort_list,reverse=True,key=lambda x: x[1]):
    print_list.append(e[0]+"`"+str(e[1]))
    if e[0]!= "No_GO_terms." and e[0]!= "No_data": 
         go_term_total+=e[1]
    
    
print("Number of unique GO terms:",len(output_dict))
print('Number Total GO terms minus "No_GO_terms." and "No_data":',(go_term_total))
print("\n".join(print_list))