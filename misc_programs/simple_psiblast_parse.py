'''
PSI-BLAST_to_GI.py
@author: Tyler Weirick
@Created on: 3/23/2012 Version 0.0 
@language:Python 3.2
@tags: PSI-blast psi blast 
==============================================================================

==============================================================================

'''

from glob import glob 
import sys
import argparse
import re


def getheadcomments():
    """
    This function will make a string from the text between the first and 
    second ''' encountered. Its purpose is to make maintenance of the comments
    easier by only requiring one change for the main comments. 
    """
    desc_list = []
    start_and_break = "'''"
    read_line_bool = False
    #Get self name and read self line by line. 
    for line in open(__file__,'r'):
        if read_line_bool:
            if not start_and_break in line:
                line_minus_newline = line.replace("\n","")
                space_list = []
                #Add spaces to lines less than 79 chars
                for i in range(len(line_minus_newline),80):
                     space_list.append(" ")
                desc_list.append(line_minus_newline+''.join(space_list)+"\n\r")
            else:
                break    
        if (start_and_break in line) and read_line_bool == False:
            read_line_bool = True
    desc = ''.join(desc_list)
    return desc

def getargs(ver='%prog 0.0'):
    #Get a set of file names 
    parser = argparse.ArgumentParser(description=getheadcomments())    
    parser.add_argument('--file_set',help='')
    args = parser.parse_args()
    sorted_file_glob = sorted(glob(args.file_set)) 
    return sorted_file_glob



file_glob = getargs()
#print(file_glob)
QUERY = "Query="
DELIM = ","

START_READING = "Sequences producing significant alignments:"

for file_name in file_glob:

    file_queries_list    = []
    set_of_unique_queires = []
    name_of_last_query    = None
    READ_SEQUENCE_IDS     = False
    
    query_cnt             = 0
    query_ID              = ""
    query_to_save         = ""
    for line in open(file_name,"r"):

        if line != "\n":
            if QUERY in line:

                #This indicates the start of a query or round of a query.
                #ex:Query= sp|P35510|PAL1_ARATH Phenylalanine ammonia-lyase 1 OS=Arabidopsis
                if line != name_of_last_query and name_of_last_query != None:
                    #Start of a new query, save data from last query. 
                    print("\n".join(query_results))
                    #file_queries_list.append("\n".join(query_results)) 
                
                #Required for previous if statement. 
                name_of_last_query = line
                try:
                    query_name = line.split("|")[1]
                except:
                    print(line)
                    query_name = line.strip()
                #Reset query_results for new query of new iteration of current query. 
                query_results      = []
                READ_SEQUENCE_IDS = True    
            elif len(line) > 0 and line[0] == ">":
                READ_SEQUENCE_IDS = False
            else:
                if READ_SEQUENCE_IDS and line.count("|") >= 2:

                    query_ID  = line.split("|")[1]
                    bit_score = line.split()[-2]
                    evalue    = line.split()[-1]
                    query_results.append(DELIM.join([query_ID,query_name,file_name,bit_score,evalue]))
                    
    #Get Last Round, as there is no new query to cause the save of data. 
    #file_queries_list.append("\n".join(query_results))
    print("\n".join(query_results))
    #print("".join(file_queries_dict))
    






