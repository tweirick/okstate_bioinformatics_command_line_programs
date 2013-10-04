"""
@author: Tyler Weirick  
@date: 2013-08-21
==============================================================================
Checks and fixes for overlaps and non-overlaps in a set of vectors. 
==============================================================================
  n_terminusI:0.00000 n_terminusK:0.00000 n_terminusL:0.00626 n_terminusM:0.00209 n_terminusN:0.00000 
  n_terminusP:0.00000 n_terminusQ:0.00000 n_terminusR:0.00835 n_terminusS:0.00418 n_terminusT:0.00209 
  n_terminusV:0.00209 n_terminusW:0.00000 n_terminusY:0.00000 a_charged_residudes_DREKH:0.25470 
  a_molecular_weight:0.67416 b_hydrophillic_and_neutral_NQSTY:0.23591 b_numb_of_aas_in_prot_seq:0.53607 
  c_basic_polar_or_positivly_charged_HKR:0.12735 d_acidic_or_negativly_charged_DE:0.12735 
"""


parser = argparse.ArgumentParser()

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


