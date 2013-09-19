'''
run_svm_learn.py
@author: Tyler Weirick
@Created on: 6/18/2012 Version 0.0 
@language:Python 3.2
@tags: svm train 
This program handles the 5-fold training and validating process. 
It takes a 
/home/TWeirick/COMBINED_FASTAS_6.7.12/40per_6102012/40per_6102012_fastas/NON_REDUNDANT_FASTAS/40_100_40_FASTAS/FIVE_FOLDER_TRAINING_VECTORS
python3 /home/TWeirick/PY_PROGRAMS/PYSVM/multiclass_five_fold_test_classes.py --help

'''
from z_optimizing_multiclass_k_fold_tests_classes import *
from z_optimizing_multiclass_k_fold_tests_functions import *
from sys import exit
from glob import glob
import os
import subprocess
from time import time
from math import *
import tempfile
from random import gauss


#=============================================================================
#                             Varibles
#=============================================================================
DEBUG = True    
c_start,c_end = 0,500
j_start,j_end = 0,15
g_start,g_end = 0,15
max_mcc = 0.0

class_name_collision_check_list = []
#Make a list of ClassificationSets, each ClassificationSet will have one of the 
#classes of data desired 
feature_ClassificationSet_list  = []
#Make a list containing k elements containing ~ k-1/k of the total data.
k_fold_learning_set     = []
k_fold_list             = []
k_level_plus_minus_list = []

#=============================================================================
#                             Main Program
#=============================================================================

#Get input files 
sorted_file_glob,k = getargs()
k = int(k)
print(k)
print(sorted_file_glob)
print("Start Classification.")
#Reset logfile.
file = open("training_history.txt",'w')
file.write("")
file.close()
#feature_ClassificationSet_list,class_name_collision_check_list
x,y = get_feature_classificationset_list_and_input_class_name_list(sorted_file_glob,k)
feature_ClassificationSet_list,class_name_collision_check_list = x,y
print(feature_ClassificationSet_list,class_name_collision_check_list)

#print(feature_ClassificationSet_list)
#[<z_optimizing_multiclass_k_fold_tests_classes.ClassificationSet object at 0x18814c10>, ... ]
#print(class_name_collision_check_list)
#['LDA5_PTH',...]
#exit()

for k_level in range(0,k):
    general_example_data = []
    test_data            = []
    calc_data            = []
    for j in range(0,k):
        if k_level == j:
            for classifer in feature_ClassificationSet_list:
                #Make a list of FeaturePoint Classes 
                test_data.append(classifer.gettextsubset(k_level))
                '''
                SVMClassification():
    
                def __init__(self,entry_class):
                '''
                calc_data = calc_data + classifer.getsubset(k_level)
        else:
            for classifer in feature_ClassificationSet_list:
                general_example_data = general_example_data+classifer.getsubset(k_level)
    print(calc_data)
    k_fold_learning_set.append([general_example_data,"\n".join(test_data),calc_data])
    

"""
for i in range(0,k):
    fold_set = []
    for k_fold in k_fold_learning_set:
        training_data,test_data,calc_data = k_fold

        plus_minus_data_list = []
        for class_name in class_name_collision_check_list:
            #for n class_types make plus negative files.
            ex = []
            for example in training_data:
                if example.example_type == class_name:
                    ex.append(example.getPositivepoint())
                else:
                    ex.append(example.getNegativepoint())
            #Should be 12 
            plus_minus_data_list.append(PlusMinusFile(class_name,"\n".join(ex)))
        fold_set.append(plus_minus_data_list)

    k_fold_list.append(KFold(plus_minus_data_list,test_data,calc_data))
    #k_level_plus_minus_list.append(fold_set)
"""
#Calculate initial points to test around point_list = make_initial_RBF_point_list(c_start,c_end,j_start,j_end,g_start,g_end)
#point_list = make_initial_RBF_point_list(c_start,c_end,j_start,j_end,g_start,g_end)

#Program is using too much memory. I don't think this will make a difference as python is garbage collected but just in case. 
#k_fold_learning_set = None

parts = 9
out_point_list = []
overall_MCC_list = []
c_increment = (c_end-c_start)/parts
j_increment = (j_end-j_start)/parts
g_increment = (g_end-g_start)/parts
for c_int in range(0,parts+1):
    c = c_int*c_increment
    if c == 0:c=0.1
    for j_int in range(0,parts+1):
        j = j_int*j_increment
        if j == 0: j =0.1
        for g_int in range(0,parts+1):
            g = g_int*g_increment
            if g == 0: g=0.1

            c_cond,j_cond,g_cond = c,j,g
            results_list = [] 
            print("Classifiy with varibles",c_cond,j_cond,g_cond)   
            
            
            for i in range(0,k):
                fold_set = []
                for k_fold in k_fold_learning_set:
                    training_data,test_data,calc_data = k_fold
            
                    plus_minus_data_list = []
                    for class_name in class_name_collision_check_list:
                        #for n class_types make plus negative files.
                        ex = []
                        for example in training_data:
                            if example.example_type == class_name:
                                ex.append(example.getPositivepoint())
                            else:
                                ex.append(example.getNegativepoint())
                        #Should be 12 
                        plus_minus_data_list.append(PlusMinusFile(class_name,"\n".join(ex)))
                    fold_set.append(plus_minus_data_list)
            
                #k_fold_list.append(KFold(plus_minus_data_list,test_data,calc_data))
                #plus_minus_data_list,test_data,calc_data
                #for k_fold in k_fold_list:#1-5
                #Get fold testing data.
                #test_str = k_fold.test_file
                test_str = test_data
                #List of feature points
                #calc_data = k_fold.calc_data
                assert test_str.count('\n')+1 == len(calc_data),calc_data
                #Make temporary file to hold testing data. 
   
                #for plus_minus_class in k_fold.plus_minus_data_list:#12
                for plus_minus_class in plus_minus_data_list:
                    i = 0
                    #Make predictions file, one float per line. 
                    predictions_file = tempfile.NamedTemporaryFile(mode='r')
                    #Do svm_learn and svm_classify results written into prediction_file.name
                    
                    dofoldclassification(c_cond,j_cond,g_cond,
                        plus_minus_class.training_data,
                        test_str,
                        predictions_file.name)
                    
                    for line in open(predictions_file.name,'r'):
                        #There will be one floating point number for each line. 
                        calc_data[i].updateprediction(
                        plus_minus_class.pos_set_name,float(line.strip()));i+=1
                    predictions_file.close()
                
                results_list = results_list + calc_data
                #================================================
                #Test file no longer needed as we have predictions. 
                
            print("Classification Complete")
            overall_MCC = calculateOverallMCC(results_list,class_name_collision_check_list)
            #overall_MCC_list.append([overall_MCC,point])
            if max_mcc < overall_MCC:
                #Set new max MCC.
                max_mcc = overall_MCC
                #Write detailed stats to a file
                #Vector Type
                #Time
                #Conditions
                out_list = [asctime(),"c="+str(c_cond)+" j="+str(j_cond)+" g="+str(g_cond)+" MCC="+str(max_mcc)]
                file = open("training_best_stats.txt",'w')
                file.write("\n".join(out_list))
                file.close()
                #Vector Type
                #Time
                #Conditions
                file = open("best_stats_confusion_matrix.txt",'w')
                file.write(makeconfusionmatrix(results_list,class_name_collision_check_list))
                file.close()
            #append run history to logfile. 
            #Time conditions MCC
            file = open("training_history.txt",'a')
            out_list = [asctime(),"c="+str(c_cond),"j="+str(j_cond),"g="+str(g_cond),"MCC="+str(max_mcc)+"\n"]
            file.write(",".join(out_list))
            file.close()
            #point_list = optimize_c_j_g_with_NCE(overall_MCC_list,[[c_start,c_end],[j_start,j_end],[g_start,g_end]])
            #point_list = False

