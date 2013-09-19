#!/opt/python3/bin/python3.2
'''
map_to_uniprot_ac.py
@author: Tyler Weirick
@Created on: 5/3/2012 Version 0.0 
@language:Python 3.2
@tags: uniprot AC ID map 

This program converts a list of mixed IDs into Uniprot AC IDs. Using 
pre-built Python pickles generated from the Uniprot mapping data.
'''

import pickle 
import argparse
from time import time
from glob import glob
testing = True
import datetime





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

    parser.add_argument('--pickle_base_name', 
                        #action='store_const',
                        #const=sum, 
                        default="",
                        help='')
    
    args = parser.parse_args()
    
    return glob(args.ID_file_names),args.pickle_base_name


def parseInputTo2DList(file_name,file_type=0): 
    
    out_2D_list = []
    for line in open(file_name,'r'):
        out_2D_list.append( line.split() )
        #if e == 'tpg':
        #    line.split('\t')
        #    #if testing:print( line.split('\t') )
    return sorted(out_2D_list)


def search_2D_list_in_dict(dict_pickle_names,entry_2D_list): 
    
    ncbi_to_unip_dic = {"ref":"RefSeq", 
                        "gi":"GI", 
                        "gb":"EMBL", 
                        "tpg":"EMBL",
                        "emb":"EMBL", 
                        "tpe":"EMBL",
                        "dbj":"EMBL", # 484
                        "pdb":"PDB",
                        "embc":"EMBL-CDS"}
    """
    Special Cases
    sp -> remove period and all after period.
    tpe    CBF88500.1  tpe Textseq-id -- Third Party Annot/Seq EMBL
    sp     P31023.2  
    tpg    DAA04521.1  tpg Textseq-id -- Third Party Annot/Seq Genbank
    """
    not_found_list = []
    accession_list = []
    use_dict   = ""
    last_dict  = ""
    #Get DB
    
    for e in entry_2D_list:
        
        #print(e)
        use_dict = e[0]
        ID       = e[1]
        
        if use_dict == 'sp':
            #This is actually a uniprot(swissprot) entry add directly, clip after period.
            use_dict = "emb"
            accession_list.append( ID.split(".")[0] )
        else:
            if use_dict == "" or use_dict != last_dict:
                
                dict_name = dict_pickle_names + ncbi_to_unip_dic[use_dict] + ".pkl"
                
                try:
                     print("Begin loading pickle.")
                     t1 = time()
                     dict_pickle_bin = open(dict_name,"rb")
                     pickle_data = pickle.load(dict_pickle_bin)
                     print("Pickle loaded.")
                     print(time()-t1)
                     
                except:
                    
                     print("Name not found.")
                     print(dict_name)
                     exit()
                 
            last_dict = use_dict
              
            if ID in pickle_data:
                #print(use_dict)
                 accession_list.append( str(pickle_data[ID]) )
            else:
                #for e in pickle_data:
                #    print(use_dict+"->"+e)
                #    break
                not_found_list.append( use_dict+" "+ID )
            
    return accession_list,not_found_list
    

  
file_glob,dict_pickle_names = getargs() 

log_list = ["File_Name\t#_Mapped\t#_Not_Mapped"]
for file_name in file_glob:
    
    print(file_name)
    t_main = time()
    #file_name = "LO1_uniprot_and_foly.fasta_psi-blast_e1e-40_j3_dnr.3.20.2012.IDs"
    #dict_pickle_names = "idmapping.dat"    
    entry_2D_list = parseInputTo2DList(file_name) 
    accession_list,not_found_list = search_2D_list_in_dict(dict_pickle_names,entry_2D_list)
    print("Total time")
    print(time() - t_main)
    
    split_file_name = file_name.split("\n")
    if len(split_file_name) > 1: 
        real_file_name = split_file_name[-1]
    else:
        real_file_name = file_name
    
    log_list.append(real_file_name+"\t"+str(len(accession_list))+"\t"+str(len(not_found_list)))
    
    out_file = open(file_name+".ac",'w')
    out_file.write( '\n'.join(accession_list) )
    out_file.close()
    
    out_file = open(file_name+".nf",'w')
    out_file.write( '\n'.join(not_found_list) )
    out_file.close()


log_name = str(datetime.datetime.now()).split(".")[0].replace(" ","_")
out_file = open(log_name+".ac-nf.log",'w')
out_file.write( '\n'.join(log_list) )
out_file.close()
    
    
    
    
    
    
    