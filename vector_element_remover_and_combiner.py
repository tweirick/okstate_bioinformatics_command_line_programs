"""
@author: Tyler Weirick  
@date: 2013-08-21
==============================================================================
Input: 
- A text file containing a line with vector desc ids 
- a regex of vector desc value format vector files
Output: 
- a file containing a composite pruned vector. The vector elements will be 
arranged in alphabetical order. The output format will be output in 
description:value format. file extenstion will be CompositePruned.vec
==============================================================================
  n_terminusI:0.00000 n_terminusK:0.00000 n_terminusL:0.00626 n_terminusM:0.00209 n_terminusN:0.00000 
  n_terminusP:0.00000 n_terminusQ:0.00000 n_terminusR:0.00835 n_terminusS:0.00418 n_terminusT:0.00209 
  n_terminusV:0.00209 n_terminusW:0.00000 n_terminusY:0.00000 a_charged_residudes_DREKH:0.25470 
  a_molecular_weight:0.67416 b_hydrophillic_and_neutral_NQSTY:0.23591 b_numb_of_aas_in_prot_seq:0.53607 
  c_basic_polar_or_positivly_charged_HKR:0.12735 d_acidic_or_negativly_charged_DE:0.12735 
"""
import argparse 
from glob import glob

DELIM = "\t"
DEBUG = False 
#=============================================================================
#                               Functions
#=============================================================================
def getargs():
    """
    Returns a value containing a file name as a string or None and a list of 
    file names as a string.  
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--els_to_keep_file',
                       help='''A file containing the names of the elements to 
                       keep,If not given, all elements will be kept.
                       EX: VD n_terminusF o_contains_sulfer_CM
                       ''',default=None)

    parser.add_argument('--vec_file_glob',
                       help='''A single .EL_DESC_VAL.vec file or regex 
                       describing multiple EL_DESC_VAL.vec files''')

    parser.add_argument('--out_file_name',
                       help='''The base name for the vector file output. 
                       Also a .log version will be printed containing the 
                       vectors used in the new vector.''')

    parser.add_argument('--omit_seqs_not_in_all_classes',
                       default=False,
                       help='''
                       If set to True will remove sequences that do not occur in each class. 
                       ''')


    args = parser.parse_args()
    return args.els_to_keep_file,glob(args.vec_file_glob),args.out_file_name,args.omit_seqs_not_in_all_classes

#=============================================================================
#                             Main Program
#=============================================================================

vecs_to_keep,file_name_glob,out_file_name,omit_seq = getargs()

#print(vecs_to_keep,file_name_glob,out_file_name)
if DEBUG: 
    for f_name in file_name_glob:
        print(f_name)
        

#Get the vectors to keep if a description file has been given.
if vecs_to_keep != None:
    in_file = open(vecs_to_keep,'r')
    in_txt = in_file.read()
    in_file.close()
    #Vectors to keep descrition file should only contain one line.
    assert len(in_txt.strip().split("\n")) == 1,in_txt.strip().split("\n")
    vecs_to_keep_list = in_txt.strip().split()
    vecs_to_keep = set(vecs_to_keep_list)
    #Check for overlaps, while this will not nessisarily cause errors. It 
    #could indicate an error. 
    assert len(vecs_to_keep) == len(vecs_to_keep_list)

    if DEBUG: 
        print("Keeping",len(vecs_to_keep),"Elements")

 
#All files should be on the same dataset i.e. the same number of lines  
out_vec_collection = []
first_file         = True
number_of_vecs     = 0

#This will only keep track of the ids in the given files. 
#It will contain a dictionary as its value with dicts 
#output will be generated from these. 
out_vec_id_dict = {}
set_of_vecs_read = set()
last_seq_ids = set()
#Each file in this will contain some type of vector. 
seq_ids_not_in_all_files = set()
for file_name in file_name_glob:
    line_cnt = 0

    tmp_seq_ids = set()

    for line in open(file_name,'r'): 
        
        sp_line = line.strip().split()
        if len(sp_line) >=2:
            seq_id  = sp_line[0]
            vector  = sp_line[1:] 
            tmp_seq_ids.add(seq_id)
            if not seq_id in out_vec_id_dict:
                out_vec_id_dict.update( {seq_id:dict()} )
            
            for el in vector:
                el_id  = "".join(el.split(":")[:-1])
                el_val = el.split(":")[-1]
                assert type(float(el_val)) == float
                if vecs_to_keep == None or el_id in vecs_to_keep:
                    #assert not el_id in out_vec_id_dict[seq_id], file_name+"\n"+line+"\n"+el_id+"\n"+
                    set_of_vecs_read.add(el_id)
                    out_vec_id_dict[seq_id].update( { el_id  : el_val }  )        
            line_cnt+=1 
    if DEBUG: 
        print(len(out_vec_id_dict),seq_id,out_vec_id_dict[seq_id]) 
    
    """
    Had a problem with not quite perfectly overlapping data sets. 
    This is a quick fix, but maybe it could come in handy later. 
    Will make a set of all seq ids that do not overlap. 
    Use this to remove them from the final dict. 
    """
    if omit_seq:
        if last_seq_ids == set():
             last_seq_ids = tmp_seq_ids

        sym_dif =  tmp_seq_ids ^ last_seq_ids 
        for sd_el in sym_dif:
            set_of_vecs_read.add( sd_el  )
        
        last_seq_ids = tmp_seq_ids


output_list = []

#Need to perserve order, so sort. If no vecs to keep given, keep all input vecs. 
if vecs_to_keep == None:
    sorted_el_list = sorted( list(set_of_vecs_read) )
else:
    sorted_el_list = sorted( vecs_to_keep )


for seq_id in out_vec_id_dict:

    if not seq_id in set_of_vecs_read:   
        #Add the name of the sequence 
        out_list_tmp = [seq_id]
        #Add the vector elements, if no entry exists for a given element. Add zero.
        for el_to_keep in sorted_el_list:
            if el_to_keep in out_vec_id_dict[seq_id]:
                out_list_tmp.append( el_to_keep+":"+out_vec_id_dict[seq_id][el_to_keep] )
            else:
                out_list_tmp.append( el_to_keep+":"+"0.0000") 
        output_list.append( DELIM.join(out_list_tmp) )

print(out_file_name)
print("Number of files in:"+str(len(file_name_glob)))
print("Final vec lenght: "+str(len(sorted_el_list)))

out_txt = "\n".join(output_list)
out_file = open(out_file_name+".vec","w")
out_file.write(out_txt)
out_file.close()

#log_el_list = sorted(list())
out_file = open(out_file_name+".log","w")
out_file.write(str(len(sorted_el_list))+" elements\n"+ DELIM.join(sorted_el_list) )
out_file.close()

