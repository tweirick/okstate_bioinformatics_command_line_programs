#!/opt/python3/bin/python3.2
'''
identifier_mapper.py
@author: Tyler Weirick
@Created on: 5/3/2012 Version 0.0 
@language:Python 3.2
@tags: uniprot ID map 

'''
import pickle
import argparse
from sys import exit
verbose = False
    
def getargs():
    
    parser = argparse.ArgumentParser(description='Process some integers.')
    
    #parser.add_argument('integers', metavar='N', type=int, nargs='+',
    #               help='an integer for the accumulator')
    parser.add_argument('--map_file_name', 
                        #action='store_const',
                        #const=sum, 
                        #default=max,
                        help='')
    
    parser.add_argument('--exclude_entries_with', 
                        #action='store_const',
                        #const=sum, 
                        default="",
                        help='list entries to exclude separeated by commas')

    parser.add_argument('--pickle_name', 
                        #action='store_const',
                        #const=sum, 
                        default="",
                        help='')
    
    args = parser.parse_args()
    
    return args.map_file_name,args.pickle_name,args.exclude_entries_with
    
    
def buildmappingpickle (map_file_name,entries_to_exclude):
    """
    
    """

    file_name = map_file_name
    unique_db_names = dict()
    overlap_dict = dict()
    
    for line in open(file_name,'r'):
        """
        There should be three values from each split list 
        (1) The uniprot AC ID, 
        (2) The name of the database being mapped to, 
        (3) The ID of the entry in the database being mapped to. 
        """
        
        #The dictionary becomes a bit unmanagable if all data in encluded
        #I am not planning to use all the data now
        exclude_line = False
        
        split_line = line.strip().strip('"').split()
        

        
        if len(split_line) != 3:
            print("Entry \n"+line+" was not split into three parts.")
            exit()
        
        uniprot_AC,db_name,db_id = split_line
        #Make a 2D dictionary, with the name of a non-uniprot database 
        #as the first values the second dictonary as the key 
        #the value of the second dict will be the non-uniprot ID
        #and the key is the uniprot value
        if db_name in unique_db_names:
            #Database name already exists. 
            
            if db_id in unique_db_names[db_name]:
                if(verbose):print("WARNING: "+ db_id +" already exists in dictionary.") 
                overlap_dict[db_name]+=1
            else:
                #New Entry
                unique_db_names[db_name].update( {db_id:uniprot_AC} )
        else:
            #Value outside db name key should be the uniprot db
            overlap_dict.update({db_name:0})
            unique_db_names.update( {db_name:{db_id:uniprot_AC}} )
            
    return unique_db_names,overlap_dict
           
    #Save pickle 
    #Plan to use crontab to update regulary
    #as uniprot_map_pickle_(date)     


#Get arguments from command line.
map_file_name,pickle_name,exclude_entries_with = attribs = getargs()
if(verbose):print(attribs)

#Build dictionary
data_dict,overlap_dict = buildmappingpickle(map_file_name)

#Output dictionary to pickle.
if pickle_name == "":
    pickle_name = map_file_name+'.pkl'
    
output = open(pickle_name, 'wb')  
#Be careful of the pickling Protocol.
pickle.dump(data_dict, output, -1)
output.close()
print("Pickle named '"+pickle_name+"'created successfully.")

print(
"Note: Please check to see if there are overlaps in type of mapping you are"+ 
"doing. Note all of the entries map 1 to 1 with Uniprot ACs and vice versa.")

print("---------------------------------------------------")
print("Categories Created")
print("Database name\tNumber of Entries\tNumber of overlaps")

for e in sorted(data_dict.keys()):
    print(e +"\t"+str(len(data_dict[e].keys()))+"\t"+str(overlap_dict[e]))










