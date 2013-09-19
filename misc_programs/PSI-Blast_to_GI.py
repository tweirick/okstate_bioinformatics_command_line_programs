'''
PSI-Blast_to_GI.py
@author: Tyler Weirick
@Created on: 3/23/2012 Version 0.1 update 5.5.2012 
@language:Python 3.2
@tags: PSI-blast psi blast 
==============================================================================
This program takes a PSI-Blast file or set of blast files specified by a  
regular expression and outputs the ID numbers found at the highest iteration 
available. The output format is a tab delimited text file with one entry per 
line. Each entry is composed of the database name followed by the ID from the
corresponding database.
In addition to the data file output a log file will also be output to a file
containing a the number of entries in the output as well as unique set of the 
databases from which entries were taken.  
==============================================================================
'''

import glob 
import sys
from optparse import OptionParser
import re

global_db_dict = {}


def getargs(ver='%prog 0.2'):
    """
    This function handles command line input for the program via the optparse 
    library
    """
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
    
    troubleShoot = False
    parser = OptionParser(version=ver,description=desc)
    
    #@todo: OptionParser is depreciated in Python 3.2. 
    #Need to move to the new style of parser. 
    parser.add_option("-i", "--psi_blast_set", 
                      dest="psi_blast_set", 
                      default="False",
                      help = "A file name or regular expression"+ 
                             "for psi-blast output.")

    parser.add_option("-l", "--level", 
                      dest="level", 
                      default="1",
                      help = "Take entries at level l, doesn't actually work yet.")
    """
    parser.add_option("-o", "--out_directory_path", 
                      dest="out_directory_path", 
                      default="",
                      help = "If not used will create files in working "+ 
                      "directory, if used will create files in specified"+ 
                      "directory")
    """
    (options, args) = parser.parse_args()
    if(troubleShoot):print(options);print(args)
            
    file_list = glob.glob(options.psi_blast_set) 
    level = options.level
     
    #print(file_list) 
    #print(out_directory_path) 
    return file_list,level


def outputdict(input_dict,max_to_output=500):
    list_for_sorting = []
    for key in input_dict.keys():
        list_for_sorting.append([input_dict[key],key])
    

    i=0
    for e in sorted(list_for_sorting, reverse=True):
        if i <= max_to_output:       
            print(e[1])
        else:
            break
        i+=1
        
def output_ref_name_pairs(input_dict,file_name,top_levels_found):
    global global_db_dict
    unique_db_names = dict()
    ID_cnt = 0
    print_list = []
    DELIM = "`"
    #Make text for IDs file.
    for e in input_dict:
        input_list = input_dict[e]
        unique_db_names.update({str(input_list[-1]):""})
        
        if str(input_list[-1]) in global_db_dict:
            global_db_dict[str(input_list[-1])]+=1
        else:
            global_db_dict.update({str(input_list[-1]):1})
        
        print_list.append(str(input_list[-1])+'\t'+str(e)+"\n")
        ID_cnt+=1
        
    out_file = open(file_name+".IDs",'w')
    out_file.write(''.join(print_list))
    out_file.close()
    
    #Make text for log file.
    print_list = []
    #Print Stats of IDS
    #print_list.append("The information below related to "+file_name+"\n")
    split_file_name = file_name.split("/")
    if len(split_file_name) > 1:
        #Get only the file name if a directory is given.
        real_file_name = split_file_name[-1]+DELIM
    else:
        real_file_name = file_name
    
    print_list.append(real_file_name+DELIM)    
    print_list.append("Sequences psi-blasted"+DELIM+str(top_levels_found)+DELIM)
    print_list.append("Number of IDs found"+DELIM+str(ID_cnt)+DELIM)
    #print_list.append("Unique IDs found:\n")
    #Add the number of entries from each database. 
    for e in sorted(unique_db_names):
        print_list.append(e+DELIM+str(global_db_dict[e])+DELIM )   
         
    print_list.append("\n")
    global_db_dict = {}
    out_file = open(file_name+".IDs.log",'w')
    out_file.write(''.join(print_list))
    out_file.close()  

            
    
def makedictfrompsiblast(file_list,level):
    
    #For collecting the query name. 
    QUERY_INDICATOR = "Query="
    QUERY_END_INDICATOR = " letters)"
    test_cnt = 0
    #For determining if all the data for the psi-blast for an input is over. 
    ENTRY_END = "Matrix:"
    
    ROUND_INDICATOR = "Results from round " 

    #For instances where a list of files is given via regex.
    for file_name in file_list:
        
        log_file_list = []        
        
        read_entries = False
        read_query   = False
    
        #One an entry is complete the highest round will be added to this 
        output_dict = dict()
        
        #Store a rounds number and a dict of the round entries. 
        greatest_round_number = 0
        
        #Stores a round from a psi-blast entry is a larger round number is found 
        #it will be replaced by this round. 
        temp_dict  = dict()
        query_name = []
        top_levels_found = 0
        for line in open(file_name,'r'):
            
            if QUERY_INDICATOR in line:
                #This will be used for the log file. So the results can be 
                #traced to a certain name.
                read_query = True 
                top_levels_found+=1
                #
            elif QUERY_END_INDICATOR in line:
                read_query = False  
                query_name.append('\n')
                log_file_list.append(''.join(query_name)) 
                query_name = []
                test_cnt+=1

            elif ROUND_INDICATOR in line:
                #Reset the temp_dict if a larger round number is encountered. 
                round_number = line.split(ROUND_INDICATOR)[1]
                if int(round_number) > int(greatest_round_number):
                    temp_dict = dict()
            elif ENTRY_END in line:
                #If true the psi-blast for the given input entry should be finished. 
                #add what data has been parsed to the output
                output_dict.update(temp_dict)
            
            #Read Data =======================================
            if read_query:
                query_name.append(line.strip()+' ')
            else:
                if (line.count("|") >=2 and line[0]!='>' and 
                line[0] != ' ' and 'Query= ' not in line): 
                
                        entry  = line.split('|')[1] #+'\n'
                        ref    = line.split('|')[0]
                        score  = line.strip().split(" ")[-4] #three spaces
                        evalue = line.strip().split(" ")[-1] #three spaces
                        #To solve some processing problems later.           
                        
                        embl_ids =  ["gb","tpg","emb","tpe","dbj"]               
                        if (ref in embl_ids  and "." in entry):
                            #print("Found embc posing as emb.")
                            ref = "embc"
                        
                        if entry.strip() != '':
                            if entry in  temp_dict:
                                temp_list = temp_dict[entry]
                                temp_list[0]+=1
                                temp_list[1] = score
                                temp_list[2] = evalue
                                temp_list[3] = ref
                                temp_dict[entry] = temp_list
                            else:
                                temp_dict.update({entry:[1,score,evalue,ref]})
        
        output_ref_name_pairs(output_dict,file_name,top_levels_found)
        #print(test_cnt)


file_list,level = getargs()
makedictfrompsiblast(file_list,level)



#convertPSItooneGIperline(file_list,out_directory_path)

#for e in global_db_dict:
#    print( e +"\t"+str(global_db_dict[e]) )


