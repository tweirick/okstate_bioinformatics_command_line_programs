from random import shuffle
from math import sqrt
import svmlight#https://bitbucket.org/wcauchois/pysvmlight
from itertools import izip, chain, repeat
import argparse


parser = argparse.ArgumentParser(description='Do training.')
parser.add_argument('--positive_training_vecs', 
                    #metavar='', 
                    type=str, 
                    #nargs='1',
                    help='')
parser.add_argument('--negative_training_vecs', 
                    #metavar='', 
                    type=str, 
                    #nargs='1',
                    help='')
parser.add_argument('--unknown_vecs', 
                    #metavar='', 
                    type=str, 
                    #nargs='1',
                    help='')

args = parser.parse_args()

pos_vec_file_name = args.positive_training_vecs
neg_vec_file_name = args.negative_training_vecs
unknown_vec_file_name = args.unknown_vecs

#Get Pos Neg and unknown Vector Files 
#pos_vec_file_name     = "specific_laccase_positive_set_5-20.faa.pruneBJXZ.fasta.AACOMP.SVM_LIGHT.vec"
#neg_vec_file_name     = "specific_laccase_negative_set_5-20.faa.pruneBJXZ.fasta.AACOMP.SVM_LIGHT.vec"
#unknown_vec_file_name = "ab_initio_switchgrass_protein_preds.faa.pruneBJXZ.fasta.greaterthan61chars.faa.AACOMP.SVM_LIGHT.vec"

"""
SPECIFIC_LACCASE_NEGATIVE_SET_5-20 1:0.05225  2:0.01441  3:0.04505  4:0.03964  5:0.03784  6:0.08468  7:0.02883  8:0.05045  9:0.05766  10:0.07748  11:0.01622  12:0.06847  13:0.06486  14:0.03964  15:0.04324  16:0.05586  17:0.07568  18:0.07748  19:0.01982  20:0.05045
SPECIFIC_LACCASE_NEGATIVE_SET_5-20 1:0.06318  2:0.01083  3:0.03791  4:0.04332  5:0.04693  6:0.08484  7:0.02166  8:0.05776  9:0.05054  10:0.07942  11:0.02347  12:0.07942  13:0.06498  14:0.03430  15:0.04693  16:0.06498  17:0.05596  18:0.06318  19:0.01805  20:0.05235
"""

#Make a Model 
pos_ex_cnt = 0
neg_ex_cnt = 0

#for base_file_name in base_file_list:    
training_set = []
for pos_ex in open(pos_vec_file_name,"r"):#base_file_name+"pos.vec"
    if "SVMLIGHT":
        pos_ex_cnt+=1
        tmp_list = []
        for el in pos_ex.split()[1:]:
            el1,el2 = el.strip().split(":")
            tmp_list.append( (int(el1),float(el2)) )
        training_set.append( (1,tmp_list) )
    else:
        print("ERROR")
        

for neg_ex in open(neg_vec_file_name,"r"):#base_file_name+"neg.vec"
    neg_ex_cnt+=1
    if "SVMLIGHT":
        tmp_list = []
        for el in neg_ex.split()[1:]:
            el1,el2 = el.strip().split(":")
            tmp_list.append( (int(el1),float(el2)) )
        training_set.append( (-1,tmp_list) )
    else:
        print("ERROR")
             

#Classify Do in sets of 10,000
fold_model  = svmlight.learn(
    training_set,
    #Options 
    type='classification',
    kernel="rbf",
    C=50,
    rbf_gamma=50,
    costratio=50
)




for unknown_vec in open(unknown_vec_file_name,"r"):#base_file_name+"neg.vec"unknown_vec_file_name
    tmp_list = []
    unknowns = []#
    for el in unknown_vec.split()[1:]:
        el1,el2 = el.strip().split(":")
        tmp_list.append( (int(el1),float(el2)) )
    unknowns.append( (-1,tmp_list)   )


    prediction = svmlight.classify(fold_model, unknowns) 

    if prediction[0] > 0.048:
        print unknown_vec.split()[0],prediction[0] ,"T"
    #else:
    #    print unknown_vec.split()[0],prediction,"F"
    #Output IDs of Positive Hits





