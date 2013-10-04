'''
@author: Tyler Weirick  
@date: 2013-7-9

This program is meant to be a quick script to gereate a table of E.C. numbers 
found by blasting against Swiss-Prot negative sets made by removing all 
query sequences from the database and then blasting the queries against the 
that database. This will read the tab delimited files generated 

'''


from glob import glob


def getclassname(name):

     if "/" in name: 
         name = name.split("/")[-1]
     #print("/")
     if "_" in name: 
         name = name.split("_")[0]
     return name

g_name = "/scratch/tweiric/LigPred_0.3/data/2013-6-21_PSIBLAST_with_2013-6-14_ids_on_2013-6-18_Sns/*_proteinlevel.faa.on.*_SwissProtnegativeset.faa.psiblastout.uniqueids.SwissProt.tab"
"""
g_name = "/scratch/tweiric/LigPred_0.3/data/2013-6-21_PSIBLAST_with_2013-6-14_ids_on_2013-6-18_Sns/*_transcriptlevel.faa.on.*_SwissProtnegativeset.faa.psiblastout.uniqueids.SwissProt.tab"

g_name = "/scratch/tweiric/LigPred_0.3/data/2013-6-21_PSIBLAST_with_2013-6-14_ids_on_2013-6-18_Sns/*_homologylevel.faa.on.*_SwissProtnegativeset.faa.psiblastout.uniqueids.SwissProt.tab"

g_name = "/scratch/tweiric/LigPred_0.3/data/2013-6-21_PSIBLAST_with_2013-6-14_ids_on_2013-6-18_Sns/*_predictedlevel.faa.on.*_SwissProtnegativeset.faa.psiblastout.uniqueids.SwissProt.tab"
"""

file_glob = sorted(glob(g_name))

max_len = 0
#Main data structure for output. 
table_dict = {}

for file_name in file_glob: 
    ec_dict = {}
    #The count of rows wikll be printed with the table to give us an idea 
    #about the amount proteins with more than one ec number. 
    row_cnt = 0    
    for line in open(file_name,"r"):
        strp_line = line.strip()
        #There was a run when running these that the program would 
        #sometimes print extra lines. So exclude blank lines. 
        if strp_line != "":
            row_cnt+=1
            #The ec numbers are located in columns 7:12
            sp_line = strp_line.split("\t")[6:12]
            for ec_num in sp_line:
                if ec_num in ec_dict: 
                    ec_dict[ec_num]+=1
                else: 
                    ec_dict.update({ec_num:1})      
                     
    if len(ec_dict) > max_len: 
        max_len = len(ec_dict)
    
    table_dict.update({ file_name: ec_dict })

    
print("Enzyme Class"+"\t"+"EC numbers in Negative Set")
for col_el in file_glob:       
    print( getclassname(col_el)+"\t"+str(len(table_dict[col_el])) )
    
for col_el in file_glob:
    for ec_cnt in table_dict[col_el]:
        print(getclassname(col_el)+"\t"+ec_cnt+"\t"+str(table_dict[col_el][ec_cnt]))












