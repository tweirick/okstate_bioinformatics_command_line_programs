
file_name = "/scratch/tweiric/LigPred_0.3/data/2013-6-21_PSIBLAST_with_2013-6-14_ids_on_2013-6-18_Sns/4CL_predictedlevel.faa.on.4CL_SwissProtnegativeset.faa.psiblastout"#"specific_positive_set_5202113.3.xml.faa.CDHIT100.faa.DB_uniprot_all_w_eval_and_name.faa.e-40.psiblast7" #"ab_initio_switchgrass_protein_preds.faa.blastp"
#"laccases_neg_set.e-40.psiblast"
get_name = False


query_dict   = {}
results_dict = {}

max_score = 0
min_score = 1000000

for line in open(file_name,'r'):
    line = line.strip()
    if len(line.strip()) > 0:
        
        if "# Iteration: 1" in line:
            #The start of a new entry. 
            #The next line will contain the name of the query. 
            get_name = True
        elif get_name:
            #Get the name of the query. 
            get_name = False
            #print(line)
            #This is meant for uniprot. It may need to be changed for other input. 
            query_name = line.split("|")[1]
                    

        if line[0] != "#" and not "Search has CONVERGED!" in line:
 
            split_line = line.split()
            query_id = split_line[0].split("|")[1]
            results_id = split_line[1].split("|")[1]
            score = float(split_line[-1])
            
            if score > max_score:
                max_score = score
            if score < min_score:
                min_score = score
              
            if query_id in query_dict:
                query_dict[query_id].update( {results_id:float(score)} )
            else:
                query_dict.update( {query_id:{results_id:float(score)} } )

            if not results_id in results_dict:    
                #results_dict[results_id].update( {query_id:float(score)} )            
                #else:             
                #results_dict[results_id].update( {results_id:{query_id:float(score)}} )
                #print(results_id)
                results_dict.update( {results_id:""} )  


'''
for result_id in results_dict: 
    for query_id in query_dict:
        if result_id in query_dict[query_id]:
            print(query_dict[query_id][result_id],end=",")
        else:
            print(-1,end=",")
    print()
'''
x = """
<head>
<style>
tr{"border-bottom: none; border-top: none; border-right: none; border-left: none; border-spacing: 0px; margin: 0px 0px 0px 0px; padding: 0px 0px 0px 0px;"}
td {border-bottom: none; border-top: none; border-right: none; border-left: none; border-spacing: 0px; margin: 0px 0px 0px 0px; padding: 0px 0px 0px 0px;}
div {border-bottom: none; border-top: none; border-right: none; border-left: none; border-spacing: 0px; margin: 0px 0px 0px 0px; padding: 0px 0px 0px 0px; margin: 0px 0px 0px 0px; width: 5px; height: 5px;
}
</style>
</head>"""

print(x)
print('<html><table border="">')
for result_id in results_dict:
    print("<tr>")
    for query_id in query_dict:
        if result_id in query_dict[query_id]:

            normal_score = 360*(query_dict[query_id][result_id] - min_score)/(max_score - min_score)
            
            print('<td><div style="width: 5px; height: 5px; background-color:hsl('+str(int(normal_score))+',65%,75%);"> </div></td>')
            
        else:
            print('<td><div style="width: 5px; height: 5px; background-color:hsl(0,65%,100%);"> </div></td>')
    print("</tr>")
print("</table></html>")





