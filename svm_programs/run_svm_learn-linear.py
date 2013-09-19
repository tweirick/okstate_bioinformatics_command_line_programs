'''
run_svm_learn.py
@author: Tyler Weirick
@Created on: 6/18/2012 Version 0.0 
@language:Python 3.2
@tags: svm train 

This program handles the 5-fold training and validating process. 
It takes a 

/home/TWeirick/COMBINED_FASTAS_6.7.12/40per_6102012/40per_6102012_fastas/NON_REDUNDANT_FASTAS/40_100_40_FASTAS/FIVE_FOLDER_TRAINING_VECTORS
'''

import argparse
from glob import glob
from sys import exit
import os
import subprocess
from time import time
from math import sqrt

run_conditions = [0, .005, .05, .5, 1, 3, 5, 7, 10, 15, 20, 25, 35, 
                  45, 50, 60, 75, 80, 90, 100, 110, 125, 150]


#run_conditions = [100]

#This is the file of sequences you want to remove from file B or 
#Want to use to combine the sequences in common 



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

    parser = argparse.ArgumentParser(description=getheadcomments())    
    
    parser.add_argument('--file_set', 
                        help='')

    args = parser.parse_args()
    return sorted(glob(args.file_set))


def make_file_fold_data_sets(five_file_list):
    """
    This function will make 5 files from 5 files. Each of the 5 new files will 
    be a combination of 4 of the 5 files, so that each of the original files 
    will be have been excluded from one of the new files. 
    
    Output files will be named five_fold_minus(original file name).ffm
    
    Both the input and output will be in the following format. 

    .ffm files contain. 
    EST 1:0.06266 2:0.02089 3:0.04439 4:0.06005 5:0.06005 6:0.08355 
    EST 1:0.06509 2:0.03550 3:0.03254 4:0.00888 5:0.02663 6:0.12130 
    LDA1 1:0.08455 2:0.01749 3:0.05102 4:0.07289 5:0.04373 6:0.08601 
    LDA2_catted_52412 1:0.06773 2:0.01793 3:0.03984 4:0.05578 5:0.04582 6:0.08566 
    LDA3 1:0.11972 2:0.07746 3:0.07746 4:0.04695 5:0.03286 6:0.08920 7:0.00235 
    """     
    if len(five_file_list) != 5:
         print("ERROR: There must be five files.")
         exit()
     
    skip_number = 0
    five_fold_to_original_files_dict = {}
    for i in range(0,5):
        subprocess_string = "cat " 
        
        for x in range(0,5):
            if skip_number != x:
                subprocess_string = subprocess_string + five_file_list[x] +" " 
    
        output_file_name = "five_fold_minus-"+five_file_list[skip_number]+".ffm"
        subprocess_string = subprocess_string +" > "+output_file_name
        output = subprocess.call(subprocess_string,shell=True)  
        
        five_fold_to_original_files_dict.update({output_file_name:five_file_list[skip_number]})
        
        skip_number+=1  
         
    return five_fold_to_original_files_dict
    

def getclassnames(file_name):
    '''
    This function returns a list of unique class names found in the vector 
    file. The class name should be the characters encountered in a line 
    until the first space is reached. 
    Input : file_name 
    Output: a list of unique class names. 
    '''
    class_list = []
   
    for line in open(file_name,'r'):
        split_line = line.split()
        if len(split_line) > 1:
            class_name = split_line[0]
            if not class_name in class_list:
                class_list.append(class_name)
        else:
            print("Warning: empty line found.")
            print(file_name,[line])
    if len(class_list) == 0:
        print("Error: no class names in output list.")
        print(line)
    return class_list



def make_pos_neg_files(five_fold_to_original_files_dict):
    """
    This function takes a set of named vector files and will convert them 
    into 
    """
    POS_SET_MARK,NEG_SET_MARK = "+1","-1"
    pos_neg_to_five_fold_dict = {}
    
    #These are the files with 4/5 of the input info.
    for five_fold_file_name in five_fold_to_original_files_dict:
        #Make a unique list of all vector names in the file. 
        class_list = getclassnames(five_fold_file_name)
        
        #Make a new file for each vector name, in which the vector name is
        #converted to the value of POS_SET_MARK and all other names converted
        #to the value of NEG_SET_MARK
        for vec_class in class_list:
            output_strings_list = []
            for line in open(five_fold_file_name,'r'):
                split_line = line.split()#out_line = ""
                if len(split_line) > 1:
                    if split_line[0] in class_list:
                         if split_line[0] == vec_class:
                             split_line[0] = POS_SET_MARK
                         else:
                             split_line[0] = NEG_SET_MARK
                    else:
                        print("Warning: ",[split_line[0]],"not in class list.")
                        
                output_strings_list.append(" ".join(split_line)+"\n")
           
            #New pos/neg vector file is make output to file.
            out_f_name = vec_class+"."+five_fold_file_name+"."+"trnvec"
            #!!!!!!!!!!!!!!!Do these need to be sorted???output_strings_list = sorted(output_strings_list) will loose association.
            o_f = open(out_f_name,'w')
            o_f.write("".join(output_strings_list))
            o_f.close()
            #Make a dict so that association can be traced.
            pos_neg_to_five_fold_dict.update({out_f_name:five_fold_file_name})
            
            """
            .trnvec
            +1 1:0.13596 2:0.01974 3:0.03454 4:0.03673 5:0.03070 6:0.09320 ...
            .
            .
            .
            -1 1:0.02597 2:0.00260 3:0.06494 4:0.05455 5:0.05455 6:0.08312 ...
            .
            .
            .
            """
    return pos_neg_to_five_fold_dict


    
def model_cals(true_pos,true_neg,false_pos,false_neg):
    '''
        $totp1=$tp1+$fn1;
        $totq1=$tn1+$fp1;
        $totr1=$tp1+$fp1;
        $tots1=$tn1+$fn1;
        $err1=$fp1+$fn1;
        $tot1=$tp1+$tn1+$fp1+$fn1;
        
        
        $error1=($err1/$tot1)*100;
        ($fp1+$fn1)/($tp1+$tn1+$fp1+$fn1)
        
        $spec1=($tn1/$totq1)*100;
        $prec1=($tp1/$totr1)*100;
        
        $accuracy1=($tp1/$totp1)*100;
        
        
        $num1=($tp1*$tn1)-($fp1*$fn1);
        $dnum1=sqrt($totp1*$totq1*$totr1*$tots1);
        $cc1=$num1/$dnum1;


$accuracy1=($tp1/$totp1)*100;
$totp1=$tp1+$fn1;

    '''
    calcs_out_dict = {}
    #print(true_pos,true_neg,false_pos,false_neg)
    #Average Accuracy
    #average_accuracy = 0
    calcs_out_dict.update({"Accuracy":
                        100*(true_pos+true_neg)/(true_pos+true_neg+false_pos+false_neg)})
    
    
    #if true_pos+false_pos != 0:
    #    calcs_out_dict.update({"Accuracy" : true_pos/(true_pos+false_neg)})
    #else:
    #    calcs_out_dict.update({"Accuracy" : 0})
    
    
    #Average PResision
    #average_precision = 0
    if true_pos+false_pos != 0:
        calcs_out_dict.update({"Precision" :100*true_pos/(true_pos+false_pos)})
    else:
        calcs_out_dict.update({"Precision" : 0})
        
    #Average Sensitivity - The probability of a false positive 
    #average_sensitivity = true_pos/(true_pos+false_neg)
    if true_pos+false_neg != 0:
        calcs_out_dict.update({"Sensitivity":100*true_pos/(true_pos+false_neg)})
    else: 
        calcs_out_dict.update({"Sensitivity":0})
    
    #Average Specificity - The probability of a false negative
    #average_specificity = true_neg/(true_neg+false_pos)
    if true_neg+false_pos != 0:
        calcs_out_dict.update({"Specificity":100*true_neg/(true_neg+false_pos)})
    else: 
        calcs_out_dict.update({"Specificity":0})
    #Average MCC Matthews correlation coefficient
    
    #average_mmc = 0
    numerator = (true_pos*true_neg)-(false_pos*false_neg)
    denominator = (true_pos+false_pos)*(true_pos+false_neg)*(true_neg+false_pos)*(true_neg+false_neg) 
    if denominator != 0:
        calcs_out_dict.update({"Matthews_correlation_coefficient": numerator/sqrt(denominator) })
    else: 
        calcs_out_dict.update({"Matthews_correlation_coefficient":0})  
    
    #Average Error
    numerator   = (false_pos+false_neg)
    denominator = (true_pos+true_neg+false_pos+false_neg)
    
    if denominator != 0:
        calcs_out_dict.update({"Error": 100*numerator/denominator })
    else: 
        calcs_out_dict.update({"Error":0})       
    #out_str = []
    #for calc in sorted(list(calcs_out_dict.keys())):
    #    out_str.append(calc+" = "+str(calcs_out_dict[calc])+" ")
    #out_str.append("\n")
    
    return calcs_out_dict





def run_svm_learn(pos_neg_to_five_fold_dict,run_conditions):
    #print("?s",len(pos_neg_to_five_fold_dict))
    stat_output_list = []
    
    five_fold_and_name_dict_to_members_list = {}
    lrn_to_pos_neg_vec_file_dict = {}
    #The length of this list should allways be five
    for pos_neg_file in pos_neg_to_five_fold_dict:    
        #print("********",pos_neg_file)
        cor_pos   = 0
        cor_neg   = 0
        false_pos = 0
        false_neg = 0
        stat_output_list     = []
        accuracy_counts      = []
        classify_fnames_list = []
        
        four_name_list = []
                
        for float_el in run_conditions:
            condition = str(float_el)
            output_file_name = pos_neg_file+"_"+condition+".lrn"
            
            subprocess_string = (
            "./svm_learn -z c -t 0 -c "+condition+" "+pos_neg_file+" "+output_file_name)
            #print("WARNING!!!!")
            output = subprocess.call(subprocess_string,shell=True)  
            
            lrn_to_pos_neg_vec_file_dict.update({output_file_name:pos_neg_file})
            
            #For running statistics on classify.
            five_fold_name = pos_neg_to_five_fold_dict[pos_neg_file]
            parent_and_condition_name = five_fold_name+condition
            if parent_and_condition_name in five_fold_and_name_dict_to_members_list:
                temp_list = five_fold_and_name_dict_to_members_list[parent_and_condition_name]
                temp_list.append(output_file_name)
                five_fold_and_name_dict_to_members_list[parent_and_condition_name] = temp_list
            else:
                five_fold_and_name_dict_to_members_list.update({parent_and_condition_name:[output_file_name]})
            
        #stat_output_list.append(model_cals(cor_pos,cor_neg,false_pos,false_neg))
        #stats_file = open(five_fold_name+".stat",'w') 
        #stats_file.write(five_fold_name+".stat"+"\n"+''.join(stat_output_list))
        #stats_file.close()
        """
        .lrn files contain 
        SVM-light Version V5.00
        0 # kernel type
        3 # kernel parameter -d 
        1 # kernel parameter -g 
        1 # kernel parameter -s 
        1 # kernel parameter -r 
        empty# kernel parameter -u 
        20 # highest feature index 
        2772 # number of training documents 
        133 # number of support vectors plus 1 
        3.2086237 # threshold b, each following line is a SV (starting with alpha*y)
        -80 1:0.10569 2:0 3:0.037939999 4:0.048780002 5:0.046069998 6:0.084009998 7:0.02981 ...
        -80 1:0.088040002 2:0.0033199999 3:0.049830001 4:0.04817 5:0.036540002 6:0.086379997 ...
        .
        .
        .
        """
    return lrn_to_pos_neg_vec_file_dict,five_fold_and_name_dict_to_members_list
        
        
        
        

def run_svm_classify(five_fold_to_original_files_dict,#.ffm -> .vec
    pos_neg_to_five_fold_dict,lrn_to_pos_neg_vec_file_dict,#.trnvec -> .ffm ,#.lrn -> .trnvec ->
    five_fold_and_name_dict_to_members_list):#names to runs
    #print("************************")
    #./svm_classify AA_Set_" + j + " model_L_" + j + "_" + c[i] + " output_L_" + j + "_" + c[i]);
    """
    The input file example_file contains the training examples. The first 
    lines may contain comments and are ignored if they start with #. Each of 
    the following lines represents one training example and is of the following 
    format:
    
    <line> .=. <target> <feature>:<value> <feature>:<value> ... <feature>:<value> # <info>
    <target> .=. +1 | -1 | 0 | <float> 
    <feature> .=. <integer> | "qid"
    <value> .=. <float>
    <info> .=. <string>
    """
    matrix_file_name_list = []
    for five_fold_name in five_fold_and_name_dict_to_members_list:
         
         classify_set_list = five_fold_and_name_dict_to_members_list[five_fold_name]
         
         number_line_file_list = []
         
         for model_file_name in sorted(classify_set_list):
             #print(five_fold_name)
             #print("!!!",model_file_name)
             #print("!!!!!!!!",lrn_to_pos_neg_vec_file_dict[model_file_name])
             #print("!!!!!!!!!!!!!",pos_neg_to_five_fold_dict[lrn_to_pos_neg_vec_file_dict[model_file_name]])
             #print("!!!!!!!!!!!!!",five_fold_to_original_files_dict[pos_neg_to_five_fold_dict[lrn_to_pos_neg_vec_file_dict[model_file_name]]])
             
             #Not sure to use .ffm or .trnvec
             excluded_file_name = five_fold_to_original_files_dict[
                            pos_neg_to_five_fold_dict[
                            lrn_to_pos_neg_vec_file_dict[model_file_name]]]
             
             score_out_file_name = model_file_name+".scr"
             
             svmc_subprocess_string = "./svm_classify "+excluded_file_name +" "+model_file_name+" "+score_out_file_name
             print(svmc_subprocess_string)
             output = subprocess.call(svmc_subprocess_string,shell=True)  
             #print("WARNIGN!!!!")
             number_line_file_list.append(score_out_file_name)

         matrix_list = []
         for line in open(excluded_file_name,'r'):
             matrix_list.append( [ line.split()[0] ] )
             
         for number_file_name in sorted(number_line_file_list):
             i = 0
             class_name = number_file_name.split(".")[0]
             for line in open(number_file_name,"r"):
                 matrix_list[i].append(class_name+":"+line.strip())
                 i+=1
         matrix_out_list = []
         for e in matrix_list:
            matrix_out_list.append(" ".join(e)+"\n")
         matrix_file_out_name = "".join(number_file_name.split(".")[1:])+".matrix"
         matrix_file_name_list.append(matrix_file_out_name)
         matrix_out_file = open(matrix_file_out_name,'w')
         matrix_out_file.write("".join(matrix_out_list))
         matrix_out_file.close()
        #model_file_name
    return matrix_file_name_list


def getclassnameserrorcalcdict(file_name):
    '''
    
    '''
    class_list = {}
   
    for line in open(file_name,'r'):
        split_line = line.split()
        if len(split_line) > 1:
            class_name = split_line[0]
            if not class_name in class_list:
                class_list.update({class_name:{"TP":0,"TN":0,"FP":0,"FN":0} })
        else:
            print("Warning: empty line found.")
            print(file_name,[line])
    if len(class_list) == 0:
        print("Error: no class names in output list.")
        print(line)
        
        
    return class_list


def calculate_matrix_stats(matrix_file_name_list):
    """
    This function will calculate the true positives, true negatives, false 
    positives, and false negatives found by running svm_classify on a model 
    file and the data excluded from the five fold training set used to 
    generate the model file using svm_learn. 
    
    To accomplish this the program will 
    for 1of5, 2of5 , 3of5 , 4of5 , 5of5 need to add up
    """
    
    MATRIX_DELIM_CHAR = ":"
    DEFAULT_CALCS_DICT = {"TOTAL_SEQS":0,"TP":0,"TN":0,"FP":0,"FN":0}
    calcs_out_list = []
    
    for matrix_file_name in matrix_file_name_list:
    
        class_names_list = getclassnames(matrix_file_name)

        class_calcs_dict = {}
        
        for prot_class in class_names_list:
            #Make dict for the selected protein class. 
            class_calcs_dict.update({prot_class:{"TOTAL_SEQS":0,"TP":0,"TN":0,"FP":0,"FN":0} })
            total_class_seqs = 0
            for line in open(matrix_file_name,"r"):
                split_line  = line.split()
                class_ID    = split_line[0] # + or -
                matrix_name_vals_pair_list = split_line[1:]
                #print(matrix_name_vals_pair_list)
                class_name             = ""
                class_value            = 0
                largest_class_value    = 0
                class_of_largest_value = 0
                
                #Find largest value
                for name_val_pair in matrix_name_vals_pair_list:
                    class_name,class_value = name_val_pair.split(MATRIX_DELIM_CHAR)
                    class_value = float(class_value)
                    
                    if class_name != "" and class_value > largest_class_value:
                       print(class_name,class_value,largest_class_value)
                       class_of_largest_value = class_name
                       largest_class_value    = class_value    
                    elif class_name != "" and class_value == largest_class_value: 
                        print("WARNING: Case where matrix values are equal has not been handled. EXITING")
                        exit()
                    elif class_name == "":
                       class_of_largest_value = class_name
                       largest_class_value    = class_value
                        
                # + and +
                #print(prot_class,class_ID,class_of_largest_value,class_calcs_dict)
                if (class_ID == prot_class):
                    total_class_seqs+=1
                    if (prot_class == class_of_largest_value):
                        #True Positive + +)
                        class_calcs_dict[prot_class]["TP"]+=1 
                    else:# + and -
                        class_calcs_dict[prot_class]["FN"]+=1 
                else:# (class_ID != prot_class):
                    if prot_class == class_of_largest_value:# - + 
                        class_calcs_dict[prot_class]["FP"]+=1
                    else: # - -
                        class_calcs_dict[prot_class]["TN"]+=1
                        
            class_calcs_dict[prot_class]["TOTAL_SEQS"] = total_class_seqs
        #Make pre-ordered list to save calculating for every instance
        calcs_order_list = sorted(list(DEFAULT_CALCS_DICT.keys()))        
        
        print(calcs_order_list)
        
        output_cals_list = []
        temp_line_list   = []
        
        for cls in sorted(class_names_list):
            #first_line_list = first_line_list + ["Class"] + calcs_order_list
            temp_line_list.append(cls)
            for calc_val in calcs_order_list:    
                temp_line_list.append(str(class_calcs_dict[cls][calc_val]))
            
        output_cnt_txt = " ".join(temp_line_list) #+ tempstr
        output_count_file = open(matrix_file_name+".cnt",'w')
        output_count_file.write(output_cnt_txt+"\n")
        output_count_file.close()
        
    
"""
    for model_file_name in five_fold_and_name_dict_to_members_list:
        score_out_file_name = model_file_name+".scr"

        ./svm_classify five_fold_minus-Lig_3of5.vec.ffm five_fold_minus-Lig_3of5.vec.ffm.LDA6.trnvec_0.lrn five_fold_minus-Lig_3of5.vec.ffm.LDA6.trnvec_0.lrn.scr

        .scr files contain
        -3.6885815
        -1.3181178
        
        cor_pos = 0
        cor_neg = 0
        false_pos = 0
        false_neg = 0
        #This needs to be changed to work with a table
    
        return score_out_file_name,model_file_name
"""

def addfivefoldresults(run_conditions):        

    #_50lrnscr.matrix.cnt
    zzzzz_out_numbers_list = []
    for condition in run_conditions:
        
        five_fold_glob = glob( "*_"+str(condition).replace(".","")+'*.cnt' )
        
        average_calcs_dict = {"TOTAL":0}
        
        for file_name in five_fold_glob:
            
            TP,TN,FP,FN = 0,0,0,0
            
            for line in open(file_name,"r"):
                sp_line = line.split()          
                #if len(sp_line)%5 == 0:
                for i in range(0,len(sp_line)-1,6):
                    #FN  FP  TN  TP
                    #print(sp_line)
                    CLASS_NAME = sp_line[(i)]
                    FN = float(sp_line[(i+1)])
                    FP = float(sp_line[(i+2)])
                    TN = float(sp_line[(i+3)])
                    TP = float(sp_line[(i+4)])
                    TOTAL = float(sp_line[(i+5)])
                    
                    calcs_dict = model_cals(TP,TN,FP,FN)
                    
                    #Print class by class ---------------------------
                    temp_out_str = [file_name+" "+CLASS_NAME+" TOTAL "+(sp_line[(i+5)])]
                    for calc in sorted(list(calcs_dict.keys())):
                        temp_out_str.append(calc+" "+str(calcs_dict[calc]))
                    print(" ".join(temp_out_str))
                    
                    #For Total Average Calcs
                    average_calcs_dict["TOTAL"]+=TOTAL
                    for calc_name in calcs_dict:
                        
                        if calc_name in average_calcs_dict:
                            average_calcs_dict[calc_name]+= calcs_dict[calc_name]*TOTAL
                        else:
                            average_calcs_dict.update({calc_name:calcs_dict[calc_name]*TOTAL})
        
        out_str = [str(condition)]
        for calc in sorted(list(average_calcs_dict.keys())):
            out_str.append(calc+" "+str(average_calcs_dict[calc]/average_calcs_dict["TOTAL"]))
            
        zzzzz_out_numbers_list.append(" ".join(sorted(out_str)))
            
    out_result_file = open("zzz_results.rslt",'w')
    out_result_file.write("\n".join(zzzzz_out_numbers_list))
    out_result_file.close()
                        
    
#=============================================================================
#                      Main Program 
#=============================================================================

t1 = time()
file_glob = getargs()

#Returns 5 five fold files(Named vector files with 1/5 of the original data excluded.)
five_fold_to_original_files_dict = make_file_fold_data_sets(file_glob)

#print("**********************")
#for e in five_fold_to_original_files_dict:
#    print(e)

"""
Returns
['five_fold_minus-Lig_1of5.vec.ffm', 'Lig_1of5.vec']
['five_fold_minus-Lig_2of5.vec.ffm', 'Lig_2of5.vec']
['five_fold_minus-Lig_3of5.vec.ffm', 'Lig_3of5.vec']
['five_fold_minus-Lig_4of5.vec.ffm', 'Lig_4of5.vec']
['five_fold_minus-Lig_5of5.vec.ffm', 'Lig_5of5.vec']
"""
#For each of the 5 fold files 
pos_neg_to_five_fold_dict = make_pos_neg_files(five_fold_to_original_files_dict)
#print("=====================")
#for e in pos_neg_to_five_fold_dict:
#    print(e)
lrn_to_pos_neg_vec_file_dict,five_fold_and_name_dict_to_members_list = run_svm_learn(pos_neg_to_five_fold_dict,run_conditions)
#print("!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#for e in lrn_to_pos_neg_vec_file_dict:
#    print(e)
#print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#for e in sorted(list((five_fold_and_name_dict_to_members_list.keys()))):
#    print(e)
#exit()
#SVM Classify .lrn -> .trnvec -> .ffm -> .vec
#Compare against Five fold files

testout = run_svm_classify(five_fold_to_original_files_dict,#.ffm -> .vec
                                                 pos_neg_to_five_fold_dict,       #.trnvec -> .ffm
                                                 lrn_to_pos_neg_vec_file_dict,    #.lrn -> .trnvec ->
                                                 five_fold_and_name_dict_to_members_list)

#classify_fnames_list.append([score_out_f_name,model_f_name])
#print(testout)
calculate_matrix_stats(testout)


addfivefoldresults(run_conditions)

print("Run time was",time()-t1,"seconds")




#run_conditions = [0, .005, .05, .5, 1, 3, 5, 7, 10, 15, 20, 25, 35, 
#                  45, 50, 60, 75, 80, 90, 100, 110, 125, 150]



'''        
/home/TWeirick/COMBINED_FASTAS_6.7.12/40per_6102012/40per_6102012_fastas/NON_REDUNDANT_FASTAS/40_100_40_FASTAS/FIVE_FOLDER_TRAINING_VECTORS
$agaccuracy=(($accuracy1*601)+
              ($accuracy2*220)+
              ($accuracy3*106)+
              ($accuracy4*391)+
              ($accuracy5*452)+
              ($accuracy6*1197)+
              ($accuracy7*247))/3214;
$avgprecision=(($prec1*601)+($prec2*220)+($prec3*106)+($prec4*391)+($prec5*452)+($prec6*1197)+($prec7*247))/3214;
$avgspecificity=(($spec1*601)+($spec2*220)+($spec3*106)+($spec4*391)+($spec5*452)+($spec6*1197)+($spec7*247))/3214;
$avgMCC=(($cc1*601)+($cc2*220)+($cc3*106)+($cc4*391)+($cc5*452)+($cc6*1197)+($cc7*247))/3214;
$avgerror=(($error1*601)+($error2*220)+($error3*106)+($error4*391)+($error5*452)+($error6*1197)+($error7*247))/3214;
print FL4 "Average Accuracy = $avgaccuracy\n";
print FL4 "Average Precision = $avgprecision\n";
print FL4 "Average Specificity = $avgspecificity\n";
print FL4 "Average MCC = $avgMCC\n";
print FL4 "Average Error = $avgerror\n\n\n";
'''
