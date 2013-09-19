#http://www.ncbi.nlm.nih.gov/protein/ZP_08948389.1?report=fasta&log$=seqview&format=text
#http://www.ncbi.nlm.nih.gov/protein/ZP_07447395.1?report=fasta&log$=seqview&format=text




from html.parser import HTMLParser
import urllib.request
from glob import glob
import argparse

import datetime

#http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id=YP_001511242.1,YP_001505974.1&rettype=gi
#http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id=
#&rettype=gi
#YP_001511242.1
#file_regex="\\Users\Tyler\Desktop\ligninases\FLOy Stuff\FOLy_UI_FILES\*"
#file_glob = glob.glob(file_regex)


def getargs():
    
    #Gets description from comments at the top of program.
    desc_list = []
    start_and_break = "'''"
    read_line_bool = False
    for line in open(__file__,'r'):
        if read_line_bool:
            if not start_and_break in line:
                line_minus_newline = line.replace("\n","")
                space_list = []
                for i in range(len(line_minus_newline),80):
                     space_list.append(" ")
                     
                desc_list.append(line_minus_newline+''.join(space_list)+"\n")
            else:
                break    
        if (start_and_break in line) and read_line_bool == False:
            read_line_bool = True
    desc = ''.join(desc_list)
    
    parser = argparse.ArgumentParser(description=desc)
    
    #parser.add_argument('integers', metavar='N', type=int, nargs='+',
    #               help='an integer for the accumulator')
    parser.add_argument('--ID_file_names', 
                        #action='store_const',
                        #const=sum, 
                        #default=max,
                        help='')

    args = parser.parse_args()
    #print(args.ID_file_names)
    return glob(args.ID_file_names)


def parseInputTo2DListAndDict(file_name): 
    
    out_2D_list = []
    #out_dict    = {}
    
    for line in open(file_name,'r'):
        out_2D_list.append( line.split() )
        out_dict.update({line[1]:False})
    return sorted(out_2D_list)


def get_ref_seq_or_gi_fasta(ref_or_gi_2D_list,ref_or_gi_found_dict):
    
     search_str = ','.join(list(ref_or_gi_found_dict.keys()))  
     NCBI_EUTILS_BASE = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id="
     NCBI_EUTILS_END  = "&rettype=fasta&retmode=text"
     
     url = NCBI_EUTILS_BASE + search_str + NCBI_EUTILS_END
     print(url)
     response = urllib.request.urlopen(url)
     source = response.read().decode()
     
     #Check for entries not included 
     entry_cnt = 0
     for line in source.split("\n"):
         if "|" in line:
             entry_cnt+=1
             for el in line.split("|"):
                 if el in ref_or_gi_found_dict:
                     ref_or_gi_found_dict[el] = True
     
     #Make not found list 
     not_found_out_list = []
     for e in ref_or_gi_2D_list:
         if e[1] in ref_or_gi_found_dict and not ref_or_gi_found_dict[e[1]]:
             not_found_out_list.append(' '.join(e) )

     return source,not_found_out_list,entry_cnt


def get_pdb(pdb_2D_list,pdb_found_dict):
    #http://www.rcsb.org/pdb/files/fasta.txt?structureIdList=4A2H
    #search_str = ','.join(list(pdb_found_dict.keys()))
    
    not_found_out_list = []
    source_list = []
    entry_cnt = 0 
    PDB_BASE = "http://www.rcsb.org/pdb/files/fasta.txt?structureIdList="
    for e in pdb_2D_list:

        url = PDB_BASE + e[1] 
        print(url)
        response = urllib.request.urlopen(url)
        source = response.read().decode()
        
        if ">" in source:
            source_list.append("".join(source))
            entry_cnt+=1
        else:
            not_found_out_list.append( " ".join(e) )

    return "".join(source_list),not_found_out_list,entry_cnt
        

def build_main_output(file_name):
    #print(file_name)
    main_out_fasta          = []
    main_out_not_found_list = []
    main_entry_cnt          = 0
    last_db_name            = ""
    out_dict                = {}
    query_list = []
    line_cnt= 0
    for line in open(file_name,'r'):
        #print(line.split())
        line_cnt+=1
        db_name,ID = line.split()
        
        #print(db_name)
        if db_name != last_db_name and last_db_name != "":
            #print("Line change")
            
            if last_db_name == "pdb":
                print(last_db_name)
                source,not_found_out_list,entry_cnt = get_pdb(query_list,out_dict)
            elif last_db_name == "embc" or last_db_name == "ref":
                print(last_db_name)
                source,not_found_out_list,entry_cnt = get_ref_seq_or_gi_fasta(query_list,out_dict)
            else:
                print("ERROR:",line)

            if source != []:   
                main_out_fasta.append(source)
            if not_found_out_list != []:
                main_out_not_found_list.append( "\n".join(not_found_out_list) )
            main_entry_cnt+=entry_cnt
            
            #Reset the list for the next round of IDs
            out_dict           = {}
            query_list         = [] 
            source             = ""   
            not_found_out_list = ""
            entry_cnt          = 0
            
        out_dict.update({ID:False})
        query_list.append([db_name,ID])
        last_db_name = db_name         
        
    #Catch the last set of IDs.
    if last_db_name == "pdb":
        source,not_found_out_list,entry_cnt = get_pdb(query_list,out_dict)
    elif last_db_name == "embc" or last_db_name == "ref":
        print(last_db_name)
        source,not_found_out_list,entry_cnt = get_ref_seq_or_gi_fasta(query_list,out_dict)
    else:
        print("ERROR:",line)
    
    if source != []:   
        main_out_fasta.append(source)
    if not_found_out_list != []:
        main_out_not_found_list.append( "\n".join(not_found_out_list) )
    main_entry_cnt+=entry_cnt
    

    return main_out_fasta,main_out_not_found_list,main_entry_cnt,line_cnt
           
file_set = getargs()

DELIM = "`"
log_list = ["File_Name"+DELIM+"Total"+DELIM+"Number_Found"+DELIM+"Number_Not_Found"]
for file_name in file_set:
    
    main_out_fasta,main_out_not_found_list,main_entry_cnt,line_cnt = build_main_output(file_name)
    #print(main_out_fasta)
    #print(main_out_not_found_list)
    #print(main_entry_cnt)
    #print(line_cnt)
    log_list.append(file_name+DELIM+str(line_cnt)+DELIM+str(main_entry_cnt)+DELIM+str(len(main_out_not_found_list)))
    
    output_file = open(file_name+".fasta","w")
    output_file.write("".join(main_out_fasta))
    output_file.close()
    
    output_file = open(file_name+".NF","w")
    output_file.write("\n".join(main_out_not_found_list))
    output_file.close()
    
log_name = str(datetime.datetime.now()).split(".")[0].replace(" ","_")
output_file = open("map_not_found_in_unip"+log_name,"w")
output_file.write("\n".join(log_list))
output_file.close()


