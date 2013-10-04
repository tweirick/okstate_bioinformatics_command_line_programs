from glob import glob 
#import sys, argparse
from xml.etree import ElementTree as ET
#import xml.etree.cElementTree as etree
import time
unique_terms = {}


import argparse
parser = argparse.ArgumentParser(description='')
parser.add_argument('--file_name', type=str, help='')
args = parser.parse_args()

UNIPROT_FILE_LOCATION = args.file_name  #"uniprot_fixed_data_all_tax_with_plastid.xml"
#UNIPROT_FILE_LOCATION = "P48347.xml"
START_READING         = "Sequences producing significant alignments:"
output_list = []
found_subcelluarLocation = False
found_accession = False

in_isoform = False

for event,elem in ET.iterparse(UNIPROT_FILE_LOCATION,events=("start","end")):

    if elem.tag == "{http://uniprot.org/uniprot}entry" and event == "start":
        accession_number     = "NO_ACCESION_NUMBER"
        find_subcelluar_list = []
        fasta_seq            = "" 
        found_subcelluarLocation = False
        found_accession = False
        
    if not found_accession and elem.tag == "{http://uniprot.org/uniprot}accession" and event == "end":
        assert elem.text != None
        accession_number    = elem.text
        found_accession = True
        
    if elem.tag == "{http://uniprot.org/uniprot}subcellularLocation":
        found_subcelluarLocation = not found_subcelluarLocation

    if elem.tag == "{http://uniprot.org/uniprot}isoform":
        in_isoform = not in_isoform
    
    if (found_subcelluarLocation and 
    elem.tag == "{http://uniprot.org/uniprot}location" and 
    event == "end"):
        loc_term = elem.text.lower().replace(" ","_")
        find_subcelluar_list.append(loc_term)
        if loc_term in unique_terms:
            unique_terms[loc_term]+=1
        else:
           unique_terms.update({loc_term:1})
        

    if elem.tag == "{http://uniprot.org/uniprot}sequence" and event == "end":
        if "length" in elem.attrib: 
            #print(accession_number)
            fasta_seq = elem.text.replace("\n","").replace(" ","")
        #else:
        #    print(elem.attrib)
    if elem.tag == "{http://uniprot.org/uniprot}entry" and event == "end":
        if find_subcelluar_list == []:
            find_subcelluar_list.append("NO_LOCALIZATION")

        output_list.append(">"+accession_number+"["+",".join(find_subcelluar_list)+"]"+""+"\n"+fasta_seq)


#outfile = open(UNIPROT_FILE_LOCATION+".subcell.faa","w")
#outfile.write("\n".join(output_list))
#outfile.close()

for e in unique_terms:
    print(e,unique_terms[e])



#if elem.tag == "{http://uniprot.org/uniprot}sequence" and event == "start":
#    print("start", elem.text,elem,elem.items())
#if elem.tag == "{http://uniprot.org/uniprot}subcellularLocation" and event == "end":
#    found_subcelluarLocation = False
'''
def getelements(filename_or_file):
    context = iter(etree.iterparse(filename_or_file, events=('start', 'end')))
    _, root = next(context) # get root element
    for event, elem in context:
        if elem.tag == "{http://uniprot.org/uniprot}entry" and event == "start":
            accession_number     = "NO_ACCESION_NUMBER"
            find_subcelluar_list = []
            fasta_seq            = "" 
            found_subcelluarLocation = False
          
        if elem.tag == "{http://uniprot.org/uniprot}accession" and event == "end":
            #if elem.text in unique_results:
            accession_number    = elem.text
            find_subcelluar_loc = True            
    
        if elem.tag == "{http://uniprot.org/uniprot}subcellularLocation" and event == "start":
            found_subcelluarLocation = True
    
        if elem.tag == "{http://uniprot.org/uniprot}subcellularLocation" and event == "end":
            found_subcelluarLocation = False
        
        if (found_subcelluarLocation and 
        elem.tag == "{http://uniprot.org/uniprot}location" and 
        event == "end"):
            find_subcelluar_list.append(elem.text.lower())
    
        if elem.tag == "{http://uniprot.org/uniprot}sequence" and event == "end":
            #print(accession_number,elem.tag,event,elem.text)
            fasta_seq = elem.text.replace("\n","").replace(" ","")
    
        if elem.tag == "{http://uniprot.org/uniprot}entry" and event == "end":
            if find_subcelluar_list == []:
                find_subcelluar_list.append("NO_LOCALIZATION")
                #yield elem
            yield accession_number+"["+",".join(find_subcelluar_list)+"]"+""+"\n"+fasta_seq
            root.clear() # preserve memory



for host in getelements(UNIPROT_FILE_LOCATION):
    #for cvss_el in host.iter():
    print(host)

'''


