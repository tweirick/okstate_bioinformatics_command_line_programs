'''
@author: Tyler Weirick
@Created on: 8/4/2012 Version 0.0 
@language:Python 3.2
@tags: MASCOT 

Combine rows with the same file of origin or run condition. 
CAUTION: This program works on the assumption that all instances 
of a similar file name or condition will occur together. 
'''

#=============================================================================
#                            Functions
#=============================================================================

def dicttotxtlist(input_dict):
    output_str_list = []
    DELIM = "`"
    for key in sorted(input_dict.keys()):
        output_str_list.append(key+DELIM+DELIM.join(input_dict[key])+"\n")
    
    return "".join(output_str_list)


#=============================================================================
#                               Main Program
#=============================================================================

#11-MetGen.htm   Cellulose_36_h  gene_id_81313.0 5693    7(5)    232     1(1)    0.64    3873    490.9451        1469.8136       1469.809        3.11    0       -26     0.41    1       U       R.VPTADVSVVDLTVR.L      3871

#=============================================================================

#=============================================================================
FILE_NAME        = "PRADE_MASCOT_TOTAL_7-31-2012.dsv"
OUTPUT_FILE_NAME = "PRADE_MASCOT_TOTAL_7-31-2012.dsv.peptide-byfile-comb.dsv"

#
prev_col_name    = ""
temp_dict        = {}
output_list      = []


for line in open(FILE_NAME,'r'):
    
    split_line = line.split()
    if len(split_line) < 18:
        print("ERROR: line is missing data.")
        print(split_line)
        pass
    file_of_origin = split_line[0]
    run_condition  = split_line[1]
    gene_ID        = split_line[2]
    mass           = split_line[3]
    evalue         = split_line[15]
    peptide        = split_line[18]
    

    if file_of_origin != prev_col_name and prev_col_name != "":
        #Append all to ouptput list. 
        output_list.append(dicttotxtlist(temp_dict))
         #Reset temp_dict for next round. 
        temp_dict = {}
    #Set previous entry.    
    prev_col_name = file_of_origin

    if gene_ID in temp_dict:
        temp_dict[gene_ID].append(evalue)
        temp_dict[gene_ID].append(peptide)
    else:
        temp_dict.update( {gene_ID:[file_of_origin,run_condition,mass,evalue,peptide]} )
        
#need to do for last file.
output_list.append(dicttotxtlist(temp_dict))
        

output_file = open(OUTPUT_FILE_NAME,'w')
output_file.write("".join(output_list))
output_file.close()      








