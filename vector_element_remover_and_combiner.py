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
"""
"""
A:0.06681 C:0.00418 D:0.07098 E:0.05637 F:0.03967 G:0.10438 H:0.03758 I:0.03549 K:0.01879 L:0.07724
 M:0.02923 N:0.02923 P:0.06889 Q:0.02714 R:0.07098 S:0.08559 T:0.06472 V:0.07098 W:0.01253 Y:0.02923 
 AA:0.00000 AC:0.00000 AD:0.00837 ... YS:0.00209 
  YT:0.00209 YV:0.00209 YW:0.00000 YY:0.00000 c_terminusA:0.00209 c_terminusC:0.00209 c_terminusD:0.00000 
  c_terminusE:0.00418 c_terminusF:0.00000 c_terminusG:0.00209 c_terminusH:0.00418 c_terminusI:0.00418 
  c_terminusK:0.00209 c_terminusL:0.00418 c_terminusM:0.00209 c_terminusN:0.00209 c_terminusP:0.00000 
  c_terminusQ:0.00000 c_terminusR:0.00418 c_terminusS:0.00209 c_terminusT:0.00000 c_terminusV:0.00209 
  c_terminusW:0.00000 c_terminusY:0.00418 middleA:0.06054 middleC:0.00209 middleD:0.06681 middleE:0.05219 
  middleF:0.03758 middleG:0.09603 middleH:0.03340 middleI:0.03132 middleK:0.01670 middleL:0.06681 
  middleM:0.02505 middleN:0.02714 middleP:0.06889 middleQ:0.02714 middleR:0.05846 middleS:0.07933 
  middleT:0.06263 middleV:0.06681 middleW:0.01253 middleY:0.02505 n_terminusA:0.00418 n_terminusC:0.00000 
  n_terminusD:0.00418 n_terminusE:0.00000 n_terminusF:0.00209 n_terminusG:0.00626 n_terminusH:0.00000 
  n_terminusI:0.00000 n_terminusK:0.00000 n_terminusL:0.00626 n_terminusM:0.00209 n_terminusN:0.00000 
  n_terminusP:0.00000 n_terminusQ:0.00000 n_terminusR:0.00835 n_terminusS:0.00418 n_terminusT:0.00209 
  n_terminusV:0.00209 n_terminusW:0.00000 n_terminusY:0.00000 a_charged_residudes_DREKH:0.25470 
  a_molecular_weight:0.67416 b_hydrophillic_and_neutral_NQSTY:0.23591 b_numb_of_aas_in_prot_seq:0.53607 
  c_basic_polar_or_positivly_charged_HKR:0.12735 d_acidic_or_negativly_charged_DE:0.12735 
  e_aliphatic_AGILV:0.35491 f_aromatic_FWY:0.08142 g_small_DNT:0.16493 h_tiny_AGPS:0.32568 
  i_large_FRWY:0.15240 j_hydrophobic_and_aromatic_WF:0.05219 k_hydrophobic_and_neutral_ACGILMFPWV:0.50939 
  l_amidic_NQ:0.05637 m_cyclic_P:0.06889 n_hydroxylic_ST:0.15031 o_contains_sulfer_CM:0.03340 
  p_hbonding_CWNQSTYKRHDE:0.50731 q_acidic_and_amide_DENQ:0.18372 r_ionizable_DEHCYKR:0.28810 
  s_sulfer_bonding_C:0.00418 t_pI:0.37888 u_molecular_weight:0.01309 v_numb_of_aas_in_prot_seq:0.01261

"""
import argparse 
from glob import glob 
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

    args = parser.parse_args()
    return args.els_to_keep_file,glob(args.vec_file_glob),args.out_file_name

#=============================================================================
#                             Main Program
#=============================================================================

vecs_to_keep,file_name_glob,out_file_name = getargs()

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
    

#All files should be on the same dataset i.e. the same number of lines  
out_vec_collection = []
first_file         = True
number_of_vecs     = 0

for file_name in file_name_glob:

    if first_file:
        for line in open(file_name,'r'): 
            out_vec_collection.append(dict())
            first_file = False
    #print(len(out_vec_collection))
    line_cnt = 0
    for line in open(file_name,'r'): 
        sp_line = line.strip().split()
        for el in sp_line:
            el_id,el_val = el.split(":")
            if vecs_to_keep == None or el_id in vecs_to_keep:
                out_vec_collection[line_cnt].update( {el_id:el_val} )
        line_cnt+=1

#The symetric differece of the vec and the 
if vecs_to_keep != None:
    assert ( set(out_vec_collection[-1].keys()) ^ vecs_to_keep ) == set()
#Output the new file.

output_list = []
for vec_el in out_vec_collection:
    tmp_list = []
    for dict_key in sorted( vec_el.keys() ):
        tmp_list.append( dict_key+":"+vec_el[dict_key] )
    output_list.append(" ".join(tmp_list))
    
out_file = open(out_file_name+".vec","w")
out_file.write("\n".join(output_list))
out_file.close()




out_file = open(out_file_name+".log","w")
out_file.write(" ".join(list(   out_vec_collection[0].keys()   )))
out_file.close()