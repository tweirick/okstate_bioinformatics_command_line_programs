from glob import glob 
#import sys, argparse
from xml.etree import ElementTree as ET
#import xml.etree.cElementTree as etree
import time
unique_terms = {}
#UNIPROT_FILE_LOCATION = "XML_FILES/swiss-prot_all_eukaryotic2.xml"#"swiss-prot_all_eukaryotic.xml"
UNIPROT_FILE_LOCATION = "all_ec_numbers_no_laccase_like"#"all_ec_numbers.xml"
#"XML_FILES/uniprot_sprot.xml"
#"laccases_neg_set.xml"
#"swiss-prot_all_eukaryotic.xml"
#"uniprot_sprot.xml"
#"uniprot_fixed_data_all_tax_with_plastid.xml"
#UNIPROT_FILE_LOCATION = "P48347.xml"

START_READING         = "Sequences producing significant alignments:"
output_list = []
found_subcelluarLocation = False
found_accession = False

in_isoform = False

for event,elem in ET.iterparse(UNIPROT_FILE_LOCATION,events=("start","end")):

    if elem.tag == "{http://uniprot.org/uniprot}entry" and event == "start":
        ecnumber_list = []
        fullName = ""
        accession_number     = "NO_ACCESION_NUMBER"
        find_subcelluar_list = []
        fasta_seq            = "" 
        found_subcelluarLocation = False
        found_accession = False
        elem.clear()
    if not found_accession and elem.tag == "{http://uniprot.org/uniprot}accession" and event == "end":
        assert elem.text != None
        accession_number    = elem.text
        found_accession = True
        elem.clear()        
    if elem.tag == "{http://uniprot.org/uniprot}subcellularLocation":
        found_subcelluarLocation = not found_subcelluarLocation
        elem.clear()
    if elem.tag == "{http://uniprot.org/uniprot}isoform":
        in_isoform = not in_isoform
        elem.clear()
    if (found_subcelluarLocation and 
    elem.tag == "{http://uniprot.org/uniprot}location" and 
    event == "end"):
        loc_term = elem.text.lower().replace(" ","_")
        find_subcelluar_list.append(loc_term)
        #if loc_term in unique_terms:
        #    unique_terms[loc_term]+=1
        #else:
        #   unique_terms.update({loc_term:1})
        elem.clear()

    if elem.tag == "{http://uniprot.org/uniprot}fullName" and event == "end" and fullName == "":
        fullName = elem.text.replace(" ","&nbsp;")
        elem.clear()


    if elem.tag == "{http://uniprot.org/uniprot}ecNumber" and event == "end":
        ecnumber_list.append(elem.text)
        elem.clear()
        

    if elem.tag == "{http://uniprot.org/uniprot}sequence" and event == "end":
        if "length" in elem.attrib: 
            #print(accession_number)
            fasta_seq = elem.text.replace("\n","").replace(" ","")
        #else:
        #    print(elem.attrib)
        elem.clear()
    if elem.tag == "{http://uniprot.org/uniprot}entry" and event == "end":
        if find_subcelluar_list == []:
            find_subcelluar_list.append("NO_LOCALIZATION")
        elem.clear()
        #output_list.append(">"+accession_number+"["+",".join(find_subcelluar_list)+"]"+""+"\n"+fasta_seq)
        #print(">"+accession_number+"["+",".join(find_subcelluar_list)+"]"+""+"\n"+fasta_seq)
        print(">"+accession_number+"["+",".join(ecnumber_list)+"@name"+fullName+"]"+"\n"+fasta_seq)

#outfile = open(UNIPROT_FILE_LOCATION+".subcell.faa","w")
#outfile.write("\n".join(output_list))
#outfile.close()


#for e in unique_terms:
#    print(e,unique_terms[e])






