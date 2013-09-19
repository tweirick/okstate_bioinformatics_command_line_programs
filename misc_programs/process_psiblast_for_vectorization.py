from glob import glob 
import sys, argparse
from xml.etree import ElementTree as ET

UNIPROT_FILE_LOCATION = "uniprot_all_proteins_from_euks_w_plastids.xml"
psiblast_file_glob    = ["new_pos_2844.e-9.psiblast"]
START_READING = "Sequences producing significant alignments:"
unique_results = {"NO_HIT":"NOT_HIT"}
inSubcellularLocation = False
tmp2 = False 
find_subcelluar_loc = False

ID_loc_list = {}


for psiblast_file_name in psiblast_file_glob:
    
    query_result_list = []

    name_of_last_query = None
    READ_SEQUENCE_IDS  = False
    query_ID           = ""
    results_ID         = "NO_HIT"
    result_val         = 0.0
    
    for line in open(psiblast_file_name,"r"):
        if line != "\n":
            if "Query= " in line:
                #The start of a data column.
                
                if line.split()[1] != query_ID and query_ID != None:
                    """
                    A new query has been encountered. Save data from 
                    previous query This the data is replaced each iteration 
                    so the data will be from the highest iteration.
                    """ 
                    query_result_list.append([query_ID,results_ID])
                    if not results_ID in unique_results:
                        unique_results.update({results_ID:""})
                        
                #Get the ID of the starting query. 
                query_ID = line.split()[1]

                #Reset Values 
                READ_SEQUENCE_IDS = True
                results_ID        = "NO_HIT"
                e_val             = 0.0
            elif len(line) > 0 and line[0] == ">":
                #Encountered the section of detailed alignments.
                READ_SEQUENCE_IDS = False
            else:
                if READ_SEQUENCE_IDS and line.count("|") >= 2:
                    
                    e_val  = float(line.split()[-1])
                    tmp_ID = line.split("|")[1]   
                    
                    if results_ID == "NO_HIT" and e_val > 0.0:
                        result_val = e_val
                        results_ID = tmp_ID
                        
print("Number of queries    :",len(query_result_list) )
print("Number of unique hits:",len(unique_results) )

                   
#Get related data from Uniprot.

for event,elem in ET.iterparse(UNIPROT_FILE_LOCATION,events=("start","end")):
    
    if elem.tag == "{http://uniprot.org/uniprot}entry" and event == "start":
        accession_number = "NO_ACCESION_NUMBER"
        find_subcelluar_loc = False
        
    if elem.tag == "{http://uniprot.org/uniprot}accession" and event == "end":
        if elem.text in unique_results:
            accession_number    = elem.text
            find_subcelluar_loc = True            

    if find_subcelluar_loc and elem.tag == "{http://uniprot.org/uniprot}subcellularLocation" and event == "start":
        inSubcellularLocation = True
        subcel_loc_test = []
        
    if (inSubcellularLocation and elem.tag == "{http://uniprot.org/uniprot}location" 
    and event == "end"):
        """
        Careful! Plastid will not always be the first tag. 
        """
        subcel_loc_test.append(elem.text.lower())

            
    if find_subcelluar_loc and elem.tag == "{http://uniprot.org/uniprot}subcellularLocation" and event == "end":
        inSubcellularLocation = False
        find_subcelluar_loc   = False
        if "plastid" in subcel_loc_test: #plastid
            unique_results[accession_number] = "plastid"
        else:
            unique_results[accession_number] = subcel_loc_test[0]



for q_el in query_result_list:
    print(query_ID,results_ID,unique_results[results_ID])
    


