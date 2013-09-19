from glob import glob
import sys, argparse
from xml.etree import ElementTree as ET

UNIPROT_FILE_LOCATION = "uniprot_all_proteins_from_euks_w_plastids1.xml"
psiblast_file_glob    = ["new_pos_2844.e-9.psiblast"]
START_READING = "Sequences producing significant alignments:"
unique_results = {"NO_HIT":"NOT_HIT"}
inSubcellularLocation = False
tmp2 = False
find_subcelluar_loc = False

ID_loc_list = {}
i = 0
for event,elem in ET.iterparse(UNIPROT_FILE_LOCATION,events=("start","end")):

    if elem.tag == "{http://uniprot.org/uniprot}entry" and event == "start":
        i+=1
        accession_number = "NO_ACCESION_NUMBER"
        find_subcelluar_loc = True

    if elem.tag == "{http://uniprot.org/uniprot}accession" and event == "end":
        #if elem.text in unique_results:
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
            #unique_results[accession_number] = "plastid"
            print(accession_number,"plastid")
        elif subcel_loc_test == []:
            print(accession_number,"NO_SUBCELL_LOCATION")            
        else:
            print(accession_number,subcel_loc_test[0])
            #unique_results[accession_number] = subcel_loc_test[0]


