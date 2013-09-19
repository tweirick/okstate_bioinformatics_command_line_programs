'''
blastclust_set_run_and_output_fasta_and_log.py
@author: Tyler Weirick
@Created on: 5/16/2012 Update 8/7/2012 
@language:Python 3.2
@tags: uniprot web get xml 
'''
import urllib.parse
import urllib.request
from xml.etree import ElementTree as ET
import time
import io
import sys
import argparse

#=============================================================================
#                       Constants
#=============================================================================
DELIM = "`"
SLEEP_TIME = 8
HTML_GET_XML_HEAD = "http://www.uniprot.org/batch/?query="
HTML_GET_XML_TAIL = "&format=xml"

#?to=ACC&from=P_GI&query=345568165
HTML_MAPPING_HEAD = "http://www.uniprot.org/mapping/"
HTML_MAPPING_TAIL = "&format=tab"

url = 'http://www.uniprot.org/mapping/?'
entry_url = "http://www.uniprot.org/uniprot/"
file_name = "uniprot_test_input.txt"

#http://www.uniprot.org/mapping/?to=ACC&from=P_GI&query=345568165+296168824&format=tab
ncbi_to_unip_dic = { "emb":"EMBL_ID", "ref":"P_REFSEQ_AC", 
                     "gi":"P_GI", "gb":"EMBL_ID", "pir":"PIR", 
                     "dbj":"EMBL_ID","pdb":"PDB_ID"}


#=============================================================================
#                            Functions
#=============================================================================

def getargs(ver='%prog 0.0'):
    '''
    Allow for the input of a file name via command line. 
    '''
    parser = argparse.ArgumentParser(description='Input file name.')    
    parser.add_argument('--file_name', help='')
    return  parser.parse_args().file_name


def parsedatafromflatfile(file_name):
    """
    This is designed to parse a file with the one of the following entries per 
    line.

    NODE_100146_length_238_cov_49.323528    
        gi|156095610|ref|XP_001613840.1|    
        35.29    68    37    2    252    49    5131    5191    3.5    35.4
        
    It returns a mapping dictionary and 
    """
    original_data_dict = {}
    mapping_dict = {}
    out_2D_list = []
    line_cnt = 0
    SPLIT_CHAR = "|"
    for line in open(file_name,"r"):
        line_cnt+=1
        #Split line around spaces
        split_line = line.split()
        conting_name = split_line[0]
        #conting_name =  NODE_100146_length_238_cov_49.323528
        database_ID  = split_line[1] 
        #database_ID = gi|156095610|ref|XP_001613840.1|   
        split_ID_entry = database_ID.split(SPLIT_CHAR)
        #split_ID_entry = [gi,156095610,ref,XP_001613840.1]
        first_DB_name = split_ID_entry[0]
        #first_DB_name = gi
        first_DB_ID   = split_ID_entry[1]
        #first_DB_ID = 156095610
        #For mapping 
        #out_2D_list.append([first_DB_name,first_DB_ID])
        mapping_dict.update( {first_DB_name+" "+first_DB_ID:False} )
        #For reconnecting data.
        original_data_dict.update({first_DB_ID:line})
        
    print("Entries Read   :",line_cnt)
    print("Unique Entries :",len(mapping_dict))
    return mapping_dict,original_data_dict


def paresefile872012(file_name):
    """
    This is designed to parse a file with the one of the following entries per 
    line.

    gene_id_1062088.0`
    gene_id_1062088.0`
    gi|26991547|ref|NP_746972.1| extracellular ligand-binding receptor [Pseudomonas putida KT2440] `
    No_entry`
    No_entry`
    NP_746972`
    370.5478294`
    6.0131E-101`
    11-MetGen.htm`
    Cellulose_36_h`
    19804`
    2.4`
    K.VAVLHDK.D`
    0.0055`
    K.KVAVLHDK.D`
    0.46`
    K.KVAVLHDK.D

    It returns a mapping dictionary and 
    """
    FILE_ENTRY_DELIM = '`'
    SPLIT_CHAR = "|"
    NO_DATA_INDICATOR = "No_Blast_Data"
    original_data_dict = {}
    mapping_dict       = {}
    out_2D_list        = []
    line_cnt           = 0
    for line in open(file_name,"r"):
        
        line_cnt+=1
        #Split line around spaces
        split_line = line.split(FILE_ENTRY_DELIM)
        
        blast_title = split_line[3]
        
        if blast_title != NO_DATA_INDICATOR:
            
            #print(line)
            #print(blast_title)
            contig_ID = blast_title#.split()[1]
            #contig_ID = gi|156095610|ref|XP_001613840.1|   
            split_ID_entry = contig_ID.split(SPLIT_CHAR)
            #split_ID_entry = [gi,156095610,ref,XP_001613840.1]
            #print(split_ID_entry)
            first_DB_name = split_ID_entry[0]
            #first_DB_name = gi
            
            first_DB_ID = split_ID_entry[1]
            #first_DB_ID = 156095610
            #For mapping 
            if first_DB_name+" "+first_DB_ID in mapping_dict:
                mapping_dict[first_DB_name+" "+first_DB_ID]+=1
            else:
                mapping_dict.update( {first_DB_name+" "+first_DB_ID:1} )
            #For reconnecting data.
            original_data_dict.update({first_DB_ID:line})
        
    print("Entries Read   :",line_cnt)
    print("Unique Entries :",len(mapping_dict))
    return mapping_dict,original_data_dict






def parsefile92112(file_name):
    """
    This is designed to parse a file with the one of the following entries per 
    line.
    gene_id_397989.0        gi|384216148|ref|YP_005607314.1|        77.05   61      14      0       1       61      92      152     4e-21   89.7
    It returns a mapping dictionary and 
    """
    FILE_ENTRY_DELIM = '`'
    SPLIT_CHAR = "|"
    NO_DATA_INDICATOR = "No_Blast_Data"
    original_data_dict = {}
    mapping_dict       = {}
    out_2D_list        = []
    line_cnt           = 0
    for line in open(file_name,"r"):
        
        line_cnt+=1
        #Split line around spaces
        split_line = line.split()
        gene_id     = split_line[0]
        blast_title = split_line[1]
        contig_ID = blast_title#.split()[1]
        #contig_ID = gi|156095610|ref|XP_001613840.1|   
        split_ID_entry = contig_ID.split(SPLIT_CHAR)
        #split_ID_entry = [gi,156095610,ref,XP_001613840.1]
        #print(split_ID_entry)
        first_DB_name = split_ID_entry[0]
        #first_DB_name = gi
        first_DB_ID = split_ID_entry[1]
        #first_DB_ID = 156095610
        #For mapping 
        if first_DB_name+" "+first_DB_ID in mapping_dict:
            mapping_dict[first_DB_name+" "+first_DB_ID]+=1
        else:
            mapping_dict.update( {first_DB_name+" "+first_DB_ID:1} )
        #For reconnecting data.
        original_data_dict.update({first_DB_ID:line})
        
    
    print("Entries Read   :",line_cnt)
    print("Unique Entries :",len(mapping_dict))
    return mapping_dict,original_data_dict    

    

def parsefile1132012(file_name):
    """

    """
    FILE_ENTRY_DELIM = '`'
    SPLIT_CHAR = "|"
    NO_DATA_INDICATOR = "No_Blast_Data"
    original_data_dict = {}
    mapping_dict       = {}
    out_2D_list        = []
    line_cnt           = 0
    for line in open(file_name,"r"):
        if "gi|" in line:
            line_cnt+=1
            #Split line around spaces
            split_line = line.split(FILE_ENTRY_DELIM)
            #print()
            #print(line)
            gene_id     = split_line[0]
            blast_title = split_line[1]
            contig_ID = blast_title#.split()[1]
            #contig_ID = gi|156095610|ref|XP_001613840.1|   
            split_ID_entry = contig_ID.split(SPLIT_CHAR)
            #split_ID_entry = [gi,156095610,ref,XP_001613840.1]
            #print(split_ID_entry)
            first_DB_name = split_ID_entry[0]
            #first_DB_name = gi

            first_DB_ID = split_ID_entry[1]
            #first_DB_ID = 156095610
            #For mapping 
            if first_DB_name+" "+first_DB_ID in mapping_dict:
                mapping_dict[first_DB_name+" "+first_DB_ID]+=1
            else:
                mapping_dict.update( {first_DB_name+" "+first_DB_ID:1} )
            #For reconnecting data.
            original_data_dict.update({first_DB_ID:line})
        
    print("Entries Read   :",line_cnt)
    print("Unique Entries :",len(mapping_dict))

    return mapping_dict,original_data_dict   




    

def buildmappingurlsandgetuniprotACs(mapping_dict):
        
    URL_MIDDLE = "?to=ACC&from=P_GI&query="
    JOIN_CHAR = "+"
    map_list = list(mapping_dict.keys())
    return_list = []
    submit_every_x_entries = 100
    entries_searched_dict = dict()
    build_url = {}
    IDs_not_found = []
    number_of_values_not_found = 0
    source_out = []
    ACs_out = {}
    gi_to_ac = {}
    #These should all be GI so no problem there. 
    for i in range(0,len(map_list)):
        
        build_url.update({map_list[i].split()[1]:map_list[i]}) 
        
        if (i % submit_every_x_entries == 0 and i!= 0) or i == len(map_list)-1:
            #Submit URL
            url = (HTML_MAPPING_HEAD+
                   URL_MIDDLE+
                   JOIN_CHAR.join(build_url)+
                   HTML_MAPPING_TAIL)
            #print("URL")
            #print(url)
            time.sleep(SLEEP_TIME)

            response = urllib.request.urlopen(url)
            source = response.read().decode()
            #source_out.append(source)
            #print("print(source)")
            #print(source)
            #Split by line
            for line in source.split("\n"):

                #print(line.split())
                split_line = line.split()
                
                if split_line != []:
                    original_ID,AC = split_line

                    if original_ID != "From":
                        ACs_out.update({AC:original_ID})
                        gi_to_ac.update({original_ID:AC})
                        if original_ID in build_url:
                            #Then this ID was found delete from build list.
                            build_url.pop(original_ID)

            gi_not_found = list(build_url.values())
            
            number_of_values_not_found+=len(gi_not_found)            
            if len(gi_not_found) != 0:
                IDs_not_found.append("\n".join(gi_not_found))     
            build_url = {}
    return ACs_out,IDs_not_found,gi_to_ac

       
def extractGOterms(xml_object):
    DELIM = "`"
    #Extract GO terms from an XML file. queried_xml_data
    #print("Start Extracting Terms From XML data.")
    entry_return_dict = {}
    read_switch  = False
    go_term_list = []
    taxon_list   = []
    ac_ID        = ""
    ec_number    = ""
    fullname     = "?"
    for event, elem in ET.iterparse(xml_object,events=("start","end")):
        
        if elem.tag == "{http://uniprot.org/uniprot}entry" and event == "end":
            
            if go_term_list == [] or go_term_list == None:
                if go_term_list == None: print(go_term_list,ac_ID,fullname)
                go_term_list = ["No_GO_terms."]
                while len(go_term_list) < 21:
                    go_term_list.append("No_GO_terms.")
            else:
                while len(go_term_list) < 21:
                    go_term_list.append("No_data")
                    
            if taxon_list == []  or taxon_list == None:
                if taxon_list == None: print(go_term_list,ac_ID,fullname)
                taxon_list = ["No_taxonomy_data"]
                while len(taxon_list) < 21:
                    taxon_list.append("No_taxonomy_data")                
            else:
                while len(taxon_list) < 21:
                    taxon_list.append("No_data")
                    
                    
            
            if type(ec_number) != str or ec_number == "":
                 ac_ID = "NO_EC_NUMBER"           
            if type(ac_ID) != str or ac_ID == "":
                 ac_ID = "Error reading ID"
            if type(fullname) != type(str()):
                ac_ID = "Error reading protein name."
            if type(DELIM) != type(str()):
                DELIM = "`"
            if type(taxon_list) != type(list()):
                taxon_list = ["No_taxonomy_data"]
            elif None in taxon_list:
                while None in taxon_list:
                    taxon_list.remove(None)
                    
            if type(go_term_list) != type(list()):
                taxon_list = ["No_taxonomy_data"]
            elif None in go_term_list:
                while None in go_term_list:
                    go_term_list.remove(None)
            
            try:
                entry_return_dict.update({ac_ID:fullname+
                                      DELIM+
                                      ec_number+
                                      DELIM+
                                      DELIM.join(taxon_list)+
                                      DELIM+
                                      DELIM.join(go_term_list) })
            except:
                print("ERROR:===========")
                print(ac_ID)
                print(fullname)
                print(taxon_list)
                print(go_term_list)
                print(DELIM)
                print("+++++++++")
                
                
            read_switch = False
            go_term_list = []
            taxon_list   = []
            fullname     = "?"
            
        if elem.tag == "{http://uniprot.org/uniprot}ecNumber" and event == "end": 
            ec_number = elem.text  
        if elem.tag == "{http://uniprot.org/uniprot}accession" and event == "end":
            ac_ID = elem.text  
        elif elem.tag == "{http://uniprot.org/uniprot}fullName" and event == "end":
            fullname = elem.text
        elif elem.tag == "{http://uniprot.org/uniprot}taxon" and event == "end":
            taxon_list.append(elem.text)
            
        if  "type" in elem.attrib and elem.attrib["type"] == "GO":
            #Turn on when a start tag is seen and off when end tag is seen.
            read_switch = not read_switch
        elif read_switch:
            #If read_switch is true then we know we are in the correct dbReference
            #entry for GO terms.
            if( event == "end" and "type" in elem.attrib and
            elem.attrib["type"] == "term"):
                go_term_list.append(elem.attrib['value'])
    #print(entry_return_dict)
    return entry_return_dict
       


def getdatafromxmlquery(AC_list):
    
    submit_every_x_entries = 100
    JOIN_CHAR = "+"
    build_url = []
    output_parser_data = []
    queried_xml_dict = {}
    
    for i in range(0,len(AC_list)):
        build_url.append(AC_list[i])
        if (i % submit_every_x_entries == 0 and i!= 0) or i == len(AC_list)-1:
            #Submit URL
            #HTML_GET_XML_HEAD = "http://www.uniprot.org/batch/?query="
            #HTML_GET_XML_TAIL = "&format=fasta"
            url = (HTML_GET_XML_HEAD+
                   JOIN_CHAR.join(build_url)+
                   HTML_GET_XML_TAIL)
            #print("URL")
            #print(url)
            build_url = []
            
            try:
                response = urllib.request.urlopen(url)
                response_returned = True
            except:
                print("Request Failed.")
                print(url)
                response_returned = False
                
            if response_returned:
                page = response.read()
                page = str(page,encoding='utf8')
                output = io.StringIO()
                output.write(page)
                output.seek(0)     
                queried_xml_dict.update(extractGOterms(output))
            
            #output_parser_data.append(queried_xml_dict)
            #for e in queried_xml_data:
            #    print(e)
            time.sleep(SLEEP_TIME)
            #build_url.append(AC_list[i])
            #return a list of terms parsed from XML 
        
    return queried_xml_dict
        
#=============================================================================
#                              Main Program
#=============================================================================
#Get arguments from command line.
#Only one type 
file_name = getargs()


#file_name = "FARESBlastOUT_test_set"    
#Get a dictionary with the Database IDs as the key and the conting names as the key.
mapping_dict,out_dict = paresefile872012(file_name)
#mapping_dict,out_dict = parsefile1132012(file_name)



#print("Entries mapped:",len(mapping_dict))
sort_list = []
non_gi_found = False
for e in mapping_dict:
    #print(mapping_dict[e],e[2:])
    sort_list.append([mapping_dict[e],e[2:].strip()])
    if e[:2] != "gi":
        print(e)
        non_gi_found = True

#fsum = 0
#for e in sorted(sort_list):
#    print(e[1],e[0])
#    fsum+=e[0]
#print("Sum:",fsum)        
#exit()

if non_gi_found:
    print("Oops this was written to only handle GIs, you will need to update the program to run other IDs. Exiting.")
    exit()
else:
    print("All entries conform to requirements.")

#Get a list of all mapped AC numbers and not found numbers    
AC_dict,IDs_not_found,gi_to_ac = buildmappingurlsandgetuniprotACs(mapping_dict)
AC_list = list(AC_dict.keys())

print("Entires mapped to Uniprot ACs:",len(AC_list))
print("Entries not mapped           :",len(IDs_not_found))

try:
    error_file = open(file_name+".mapping-errors","w")
    error_file.write("\n".join(IDs_not_found))
    error_file.close()
except:
    print("Error printing mapping errors.")
    
uniprot_info_dict = getdatafromxmlquery(AC_list)
print("Uniprot data entries returned:",len(uniprot_info_dict))

error_list = []
for uni_key in uniprot_info_dict.keys():
     if uni_key in AC_dict:
          print(AC_dict[uni_key]+"`"+uni_key+"`"+uniprot_info_dict[uni_key])
     else:
         error_list.append(uni_key+"`"+uniprot_info_dict[uni_key])
         

out_error_file_2 = open("errornus_uniprot_outout.txt",'w')
out_error_file_2.write( "\n".join(error_list) )
out_error_file_2.close()
         

split_around_char = "|"
ac_col       = ""
uniprot_cols = ""
output_lines_list = []
for line in open(file_name,"r"):
    if "gi|" in line:
        #Split line around spaces
        split_line = line.split("`")
        conting_name = split_line[0]
        database_ID  = split_line[3]#Needs to containg gi number
        split_ID_entry = database_ID.split(split_around_char)
        first_DB_name = split_ID_entry[0]
        print(split_ID_entry)
        first_DB_ID   = split_ID_entry[1]
            
        if first_DB_ID in gi_to_ac:
            ac_col = gi_to_ac[first_DB_ID]
            if ac_col in  uniprot_info_dict:
                uniprot_cols = uniprot_info_dict[ac_col]
            else:
                uniprot_cols = "Not Downloaded"
                build_cols = []
                while len(build_cols) < 21:
                    build_cols.append(uniprot_cols)
                uniprot_cols = DELIM.join(build_cols)
                
        else:
            ac_col = "Not Mapped"
            #build_cols = []
            #while len(build_cols) < 21:
            #    build_cols.append(ac_col)
            #ac_col = DELIM.join(build_cols) 
            uniprot_cols = "Not Mapped"
            build_cols = []
            while len(build_cols) < 21+21:
                build_cols.append(uniprot_cols)
            uniprot_cols = DELIM.join(build_cols)
    else:
        ac_col = "Not Mapped"
        #build_cols = []
        #while len(build_cols) < 21:
        #    build_cols.append(ac_col)
        #ac_col = DELIM.join(build_cols) 
        uniprot_cols = "Not Mapped"
        build_cols = []
        while len(build_cols) < 21+21:
            build_cols.append(uniprot_cols)
        uniprot_cols = DELIM.join(build_cols)
        
    output_lines_list.append(ac_col+DELIM+line.strip()+DELIM+uniprot_cols)


out_file_name = file_name+".unip"
out_file = open(out_file_name,'w')
out_file.write("\n".join(output_lines_list))
out_file.close()
    

