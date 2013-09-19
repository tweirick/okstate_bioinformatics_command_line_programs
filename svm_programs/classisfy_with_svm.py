'''
classify_with_svm.py
@author: Tyler Weirick
@Created on: 6/18/2012 Version 0.0 
@language:Python 3.2
@tags: svm classify 

This program accepts a set of vectors and classifies them with svm classify.
'''

import argparse
from glob import glob
from sys import exit
import os
import subprocess
from time import time
from math import sqrt


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

#For wider compatibility. optparse was depreciated in python 3.2
try:
    import argparse
    def getargs(ver='%prog 0.0'):
        parser = argparse.ArgumentParser(description=getheadcomments())  
        #class_vector_file,vectors_to_classify_file   
        parser.add_argument('--train_file', 
                            help='Should not be rexex.')
        
        parser.add_argument('--classify_file', 
                            help='')
        
        parser.add_argument('--c_condition', 
                            help='')
        
        args = parser.parse_args() 
        
        train_file    = args.train_file
        s_example_file_list = sorted(glob(args.classify_file))
        c_condition = args.c_condition       

        type_sefl = type(s_example_file_list)
        if type_sefl != list() and type_sefl == str():
            s_example_file_list = list(s_example_file_list)
            
        return train_file,s_example_file_list,c_condition
    
except:
    
    use_arg = False
    print("Error importing argparse. using optparse instead.")
    from optparse import OptionParser
    def getargs(ver='%prog 0.1'):
        """
        Gets file names for input and output.
        """    
        troubleShoot = False
        parser = OptionParser(version=ver,description=getheadcomments())
            
        parser.add_option("-i", "--file_set", 
            dest="file_set", 
            default="",
            help = "Input file set.")
        
        parser.add_option("-e", "--example_file_names", 
            dest="example_file_names", 
            default="",
            help = "")
                    
        (options, args) = parser.parse_args()
        if(troubleShoot):print(options);print(args)
                
        sorted_file_list    = sorted(glob(options.file_set))
        s_example_file_list = sorted(glob(options.example_file_names))

        type_sfl = type(sorted_file_list)
        if type_sfl != list() and type_sfl == str():
            sorted_file_list = list(sorted_file_list)
                            
        type_sefl = type(s_example_file_list)
        if type_sefl != list() and type_sefl == str():
            s_example_file_list = list(s_example_file_list)

        return sorted_file_list,s_example_file_list
    

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

def classifyvectorfile(model_file_name,s_example_file_list):
    '''
    This function runs svm classify 
    '''
    output_file_list = []
    s_example_file_list = s_example_file_list[0]
    print(s_example_file_list)
    print(model_file_name)
    for example_file in model_file_name:
       score_out_file_name = example_file+"-"+s_example_file_list+".cnt"
       

       subp_str = ("./svm_classify "+s_example_file_list+" "+example_file+" "+" "+score_out_file_name)
       
       output = subprocess.call(subp_str,shell=True)  
       
       output_file_list.append(score_out_file_name)
       
       print(subp_str) 
      
    return output_file_list
    

def make_pos_neg_files(vector_file):
    """
    This function takes a vector file and will name a pos/neg training set
    for all 
    """
    POS_SET_MARK,NEG_SET_MARK = "+1","-1"
    pos_neg_to_five_fold_dict = {}
    
    new_file_names = []

    #Make a unique list of all vector names in the file. 
    class_list = getclassnames(vector_file)
    
    #Make a new file for each vector name, in which the vector name is
    #converted to the value of POS_SET_MARK and all other names converted
    #to the value of NEG_SET_MARK
    for vec_class in class_list:
        output_strings_list = []
        for line in open(vector_file,'r'):
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
        out_f_name = vec_class+"."+vector_file+"."+"maintrnvec"
        #!!!!!!!!!!!!!!!Do these need to be sorted???output_strings_list = sorted(output_strings_list) will loose association.
        new_file_names.append(out_f_name)
        
        o_f = open(out_f_name,'w')
        o_f.write("".join(output_strings_list))
        o_f.close()
   
    return new_file_names,class_list


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
    
    #Average Error--> RFP?
    #        ($fp1+$fn1)/($tp1+$tn1+$fp1+$fn1)
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


def run_svm_learn_linear(pos_neg_file_list,c_condition):
    '''
    There will be one 
    '''
    new_lrn_file_name_list = []
    for pos_neg_file in pos_neg_file_list:    
        
        output_file_name = pos_neg_file+"_"+str(c_condition)+".mainlrn"
        
        new_lrn_file_name_list.append(output_file_name)       
        print(output_file_name)
        subprocess_str = ("./svm_learn -z c -t 0 -c "+c_condition+" "+
                          pos_neg_file+" "+output_file_name)
          
        output = subprocess.call(subprocess_str,shell=True)  

    return  new_lrn_file_name_list


def makescorematrix(count_list,prediction_file,class_vector_file):
     '''
     Makes a matrix from score files which consits of on numerical value per line.
     '''
     
     #class_list = getclassnames(class_vector_file)
    
     out_list = []
     for line in open(prediction_file,'r'):
         out_list.append(line.split()[0])
         
     for file_name in count_list:
        i=0
        prot_class = file_name.split(".")[0]
        for line in open(file_name,'r'):    
            out_list[i] = out_list[i]+" "+prot_class+":"+line.strip() 
            i+=1
     #out_list = ["Seq_Origin"+" "+" ".join(class_list)] + out_list
     out_str = "\n".join(out_list)
     
     return out_str
     
     

def calculate_matrix_stats(matrix_file_name_list):
    """
    This function will calculate the true positives, true negatives, false 
    positives, and false negatives found by running svm_classify on a model 
    file and the data excluded from the five fold training set used to 
    generate the model file using svm_learn. 
    
    To accomplish this the program will 
    for 1of5, 2of5 , 3of5 , 4of5 , 5of5 need to add up
    """
    
    MATRIX_DELIM_CHAR  = ":"
    LV_INITIAL_VALUE = "Largest value not set yet."
    DEFAULT_CALCS_DICT = {"TOTAL_SEQS":0,"TP":0,"TN":0,"FP":0,"FN":0}
    calcs_out_list     = []
    
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
                
                class_of_largest_value = LV_INITIAL_VALUE
                
                #Find largest value
                #print("Start search for largest value.")
                for name_val_pair in matrix_name_vals_pair_list:
                    class_name,class_value = name_val_pair.split(MATRIX_DELIM_CHAR)
                    class_value = float(class_value)
                    #print(class_name,",",class_value,",",largest_class_value,[class_of_largest_value])
                    
                    if class_name != "" and class_value > largest_class_value:
                       #print(class_name,class_value,largest_class_value)
                       class_of_largest_value = class_name
                       largest_class_value    = class_value    
                    elif class_name != "" and class_value == largest_class_value: 
                        print("WARNING: Case where matrix values are equal has not been handled. EXITING")
                        print("Largest val name:",class_of_largest_value,"Current Class name",class_name,largest_class_value,class_value)
                        #exit()
                    elif class_of_largest_value == "Largest value not set yet.":
                       #print("@@@@@@@@@@@@@@@",class_of_largest_value,largest_class_value)
                       class_of_largest_value = class_name
                       largest_class_value    = class_value
                                        
                if (class_ID == prot_class):
                    total_class_seqs+=1
                    if (prot_class == class_of_largest_value):
                        #True Positive + +)
                        #print("True Positive")
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
        
        output_cals_list = []
        temp_line_list   = []
        
        for cls in sorted(class_names_list):
            #first_line_list = first_line_list + ["Class"] + calcs_order_list
            temp_line_list.append(cls)
            for calc_val in calcs_order_list:    
                temp_line_list.append(str(class_calcs_dict[cls][calc_val]))
        
        
        #FN FP TN TOTAL TP
        
        output_cnt_txt = " ".join(temp_line_list) #+ tempstr
        output_count_file = open(matrix_file_name+".cnt",'w')
        output_count_file.write(output_cnt_txt+"\n")
        output_count_file.close()


     
#=============================================================================
#                              Main Program
#=============================================================================

class_vector_file,vectors_to_classify_file,c_condition = getargs(ver='%prog 0.1')

#for each class in class vector file make a training file.
pos_neg_file_names,class_list = make_pos_neg_files(class_vector_file)




lrn_file_list = run_svm_learn_linear(pos_neg_file_names,c_condition)


cnt_file_list = classifyvectorfile(lrn_file_list,
                                   vectors_to_classify_file)

matrix_text = makescorematrix(cnt_file_list,
                              vectors_to_classify_file[0],
                              class_vector_file)



out_file = open("zt","w")
out_file.write(matrix_text)
out_file.close()


calculate_matrix_stats(["zt"])


'''
def countTFPN(matrix_file_name):

    MATRIX_DELIM_CHAR  = ":"
    class_calcs_dict = {"TOTAL_SEQS":0,"TP":0,"TN":0,"FP":0,"FN":0}
    
    for line in open(matrix_file_name,"r"):
        split_line  = line.split()
        class_ID    = split_line[0]
        matrix_name_vals_pair_list = split_line[1:]
        class_name             = ""
        class_val            = 0
        largest_class_value    = 0
        

        
        nv_pair = matrix_name_vals_pair_list[0].split(MATRIX_DELIM_CHAR)
        
        largest_class,largest_class_val = nv_pair[0],float(nv_pair[1])
        #Find largest value
        for name_val_pair in matrix_name_vals_pair_list[1:]:
            class_name,class_value = name_val_pair.split(MATRIX_DELIM_CHAR)
            class_val = float(class_val)
            if class_val > largest_class_value:
               largest_class_name = class_name
               largest_class_val   = class_val    
            elif class_val == largest_class_value: 
                print("WARNING: Case where matrix values are equal has not been handled. EXITING")
                print("Largest val name:",class_of_largest_value,"Current Class name",class_name,largest_class_value,class_value)

        if class_ID == largest_class_name:
            #True Positive
        elif class_ID != largest_class_name:
            #True Negative 
        
        if (class_ID == largest_class_value):
            total_class_seqs+=1
            if (largest_class_value == largest_class_name):
                #True Positive + +)
                class_calcs_dict[prot_class]["TP"]+=1 
            else:# + and -
                class_calcs_dict[prot_class]["FN"]+=1 
        else:# (class_ID != prot_class):
            if prot_class == largest_class_name:# - + 
                class_calcs_dict[prot_class]["FP"]+=1
            else: # - -
                class_calcs_dict[prot_class]["TN"]+=1
    
    print(class_calcs_dict)
    
    return class_calcs_dict


'''




    