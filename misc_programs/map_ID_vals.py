#!/opt/python3/bin/python3.2
'''
map_to_uniprot_ac.py
@author: Tyler Weirick
@Created on: 5/3/2012 Version 0.0 
@language:Python 3.2
@tags: uniprot AC ID map 
'''

import sqlite3
import argparse
from time import time
from sys import exit
verbose = False
testing = True
AC_name = "AC"
db_table_name = "map_DB"


def getargs():
    
    parser = argparse.ArgumentParser(description='Process some integers.')
    
    #parser.add_argument('integers', metavar='N', type=int, nargs='+',
    #               help='an integer for the accumulator')
    parser.add_argument('--ID_file_name', 
                        #action='store_const',
                        #const=sum, 
                        #default=max,
                        help='')
    
    parser.add_argument('--translator_file_name', 
                        default="",
                        help='')   

    parser.add_argument('--DB_name', 
                        #action='store_const',
                        #const=sum, 
                        default="",
                        help='')
    
    args = parser.parse_args()
    
    return args.ID_file_name, args.DB_name, args.translator_file_name
    

def build_translation_file(translator_file_name):
    print("Building Translation Dictionary.")
    delim_char = ":"
    trans_dict = dict()
    for line in open(translator_file_name,'r'):
        split_line = line.strip().split(delim_char)
        if len(split_line) == 2: 
            # Key   - The value taken from psi-blast. 
            # Value - The value found in the database. 
            key,value = split_line
            trans_dict.update({key:value})
        else:
            print("ERROR: This line of the traslation file does not split into two strings.")
            print(split_line)        
    print("Translation Dictionary Finished.")    
    return trans_dict

def searchDB(map_file_name,DB_file_name,translator_dict):
    
    print("Opening DB")
    conn = sqlite3.connect(DB_file_name)
    print("DB Open.")
    
    print("Make Cursor Object.")
    #c = conn.cursor()
    
    
    # configure for fast writes 
    c = conn.cursor()
    c.execute('PRAGMA synchronous = 0')
    c.execute('PRAGMA cache_size = 64000')
    c.execute('PRAGMA fullfsync = 0')
    c.execute('PRAGMA journal_mode = OFF')
    c.arraysize = 30000
    print("Make Cursor Object Open.")
    
    
    map_to_val = ""
    
    ac_list = []
    not_found_list = []
    
    
    
    for line in open(map_file_name,'r'):
        split_line = line.strip().split()
        #print(split_line)
        if len(split_line) == 2: 
            if split_line[0] !="sp":
                dn_name,entry_name = split_line
                from_col =  translator_dict[dn_name]
                t = (entry_name,)

                print('select '+AC_name+' from '+db_table_name+' where '+from_col+'='+entry_name)
                
                print("Execute")
                t1 = time()
                c.execute('select '+AC_name+' from '+db_table_name+' where '+from_col+'=? limit 1', t)
                print(time()-t1)
                print("Execute")
                
                print("Fetch")
                t1 = time()
                query = c.fetchone()
                print(time()-t1)
                print("Fetched")
                if query != None:
                    #print(query[0])
                    ac_list.append(query[0]+"\n")
                else:
                    not_found_list.append(line)
        #i+=1
        #if i == 5:
        #    break 
    print("File operations complete.")
    return ac_list,not_found_list
    

ID_file_name,DB_file_name,translator_file_name = getargs()
trans_dict = build_translation_file(translator_file_name)
ac_list,not_found_list = searchDB(ID_file_name,DB_file_name,trans_dict)


print(len(ac_list))
print(len(not_found_list))


out_file = open(ID_file_name+".ac",'w')
out_file.write('\n'.join(ac_list))
out_file.close()


out_file = open(ID_file_name+".not_found",'w')
out_file.write('\n'.join(not_found_list))
out_file.close()

# Have option to print column IDs
# Get ID in column x from ID in column y:
# input is a flat file with DB_name/entry_name
# Translator file. 
# Print as flat file with one entry per line 
"""
Built:create table map_DB (AGD text, Aarhus_Ghent_2DPAGE text, Allergome text, ArachnoServer text, BioCyc text, 
CGD text, CYGD text, CleanEx text, ConoServer text, DIP text, DMDM text, DNASU text, DisProt text, DrugBank text,
ECO2DBASE text, EMBL text, EMBL_CDS text, EchoBASE text, EcoGene text, Ensembl text, EnsemblGenome text,
EnsemblGenome_PRO text, EnsemblGenome_TRS text, Ensembl_PRO text, Ensembl_TRS text, EuPathDB text, FlyBase text, 
GI text, GeneCards text, GeneFarm text, GeneID text, GeneTree text, GenoList text, GenomeReviews text, GermOnline text, 
HGNC text, HOGENOM text, HOVERGEN text, HPA text, HSSP text, H_InvDB text, IPI text, KEGG text, KO text, LegioList text, 
Leproma text, MEROPS text, MGI text, MIM text, MINT text, MaizeGDB text, NCBI_TaxID text, NextBio text, OMA text, 
Orphanet text, OrthoDB text, PATRIC text, PDB text, PeroxiBase text, PharmGKB text, PptaseDB text, ProtClustDB text, 
PseudoCAP text, REBASE text, RGD text, Reactome text, RefSeq text, RefSeq_NT text, SGD text, TAIR text, TCDB text, 
TIGR text, TubercuList text, UCSC text, UniGene text, UniParc text, UniProtKB_ID text, UniRef100 text, UniRef50 text, 
UniRef90 text, VectorBase text, World_2DPAGE text, WormBase text, WormBase_PRO text, WormBase_TRS text, Xenbase text, 
ZFIN text, dictyBase text, eggNOG text, euHCVdb text, neXtProt text)
"""
