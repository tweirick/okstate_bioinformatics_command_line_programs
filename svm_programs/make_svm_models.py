import argparse
from glob import glob
from sys import exit
import os
import subprocess
from time import time
from math import sqrt
from z_optimizing_multiclass_k_fold_tests_classes import *
from z_optimizing_multiclass_k_fold_tests_functions import *


class SVMLearn():
    '''
    This handles the creating of svm training strings 
    '''
    def __init__(self):
        
        #c_run_conditions = [60]
        #c_run_conditions = [vi 0, 0.5, 1]
        #c_run_conditions = [1]
        #0.005 - 1000 
        #1-15
        #d run 1-15
        #d_run_conditions = [1,9]
        self.SVM_LEARN_PATH = ""
        self.KERNAL_TYPES = {"LINEAR":"0","POLYNOMIAL":"1","RDF":"2"}
        self.kernal_mode  = ""
        self.c_condition  = ""
        self.g_condition  = ""
        self.j_condition  = ""
        self.d_condition  = ""
        self.example_file = ""
        self.model_file   = ""
    
    def setSVMLearnPath(self,svm_learn_path):  
        #@todo: add code to check for file existence
        self.SVM_LEARN_PATH = svm_learn_path
    
    #Maybe combine these later. 
    def setlinear(self,c,ex_file,mod_file):
        self.kernal_mode  = "LINEAR"
        self.c_condition  = c
        self.example_file = ex_file
        self.model_file   = mod_file      
          
    def setpoly(self,c,d,ex_file,mod_file):
        self.kernal_mode  = "POLYNOMIAL"
        self.c_condition  = c
        self.d_condition  = d
        self.example_file = ex_file
        self.model_file   = mod_file 
           
    def setRDF(self,c,g,d,ex_file):    
        self.kernal_mode  = "RDF"
        self.c_condition  = c
        self.g_condition  = g
        self.d_condition  = d
        self.example_file = ex_file

                        
    def getExecutionString(self):
        cline_command_list = []
        if (self.kernal_mode == "" or self.example_file == "" or 
        self.SVM_LEARN_PATH == ""):
            print("ERROR: Empty string found in", 
            "kernal_mode, example_file, or SVM_LEARN_PATH .",
            "Exiting.")
            exit()
            
        if self.kernal_mode == "LINEAR":
            if self.c_condition == "":
                print("-c is empty string. Exiting.")
                exit()
            else:
                cline_command_list = [
                    SVM_LEARN_PATH,
                    "-z c",
                    "-t", "0", 
                    "-c",self.c_condition,
                    self.example_file,
                    self.model_file]    
        elif self.kernal_mode == "POLYNOMIAL":
            print("POLYMONIAL NOT SUPPORED YET EXITING.")
            exit()
        elif self.kernal_mode == "RDF":
            if (self.c_condition  == "" or self.g_condition == "" or
            self.d_condition == ""):
                print("c,d, or g is empty string. Exiting.")
                exit()
            else:
                self.model_file = (self.example_file+
                "."+
                "c"+self.c_condition+"_"+
                "d"+self.d_condition+"_"+
                "g"+self.g_condition+
                ".rbfmodel")
                
                cline_command_list = [
                    self.SVM_LEARN_PATH,
                    "-z c",
                    "-t", "2", 
                    "-c",self.c_condition,
                    "-d",self.d_condition,
                    "-g",self.g_condition,
                    self.example_file,
                    self.model_file]
        else:
            print("ERROR: Unknown kernel mode. Exiting.")
            exit()
            
        return " ".join(cline_command_list)
        
        
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
        
def makeexamplefiles(named_vector_file_name_list):
    """
    This function takes a set of named vector files and will convert them 
    into 
    """
    POS_SET_MARK,NEG_SET_MARK = "+1","-1"
    pos_neg_to_five_fold_dict = {}
    
    #These are the files with 4/5 of the input info.
    for named_vector_file_name in named_vector_file_name_list:
        #Make a unique list of all vector names in the file. 
        class_list = getclassnames(named_vector_file_name)
        
        #Make a new file for each vector name, in which the vector name is
        #converted to the value of POS_SET_MARK and all other names converted
        #to the value of NEG_SET_MARK
        for vec_class in class_list:
            output_strings_list = []
            for line in open(named_vector_file_name,'r'):
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
            out_f_name = vec_class+"."+named_vector_file_name+"."+"trnvec"
            #!!!!!!!!!!!!!!!Do these need to be sorted???output_strings_list = sorted(output_strings_list) will loose association.
            o_f = open(out_f_name,'w')
            o_f.write("".join(output_strings_list))
            o_f.close()
            #Make a dict so that association can be traced.
            pos_neg_to_five_fold_dict.update({out_f_name:named_vector_file_name})
            
    return pos_neg_to_five_fold_dict


#exit("No input value exiting.")
def getargs(ver='%prog 0.0'):
    parser = argparse.ArgumentParser()    
    parser.add_argument('--file_set',default="", help='')
    parser.add_argument('--kernal',default="2", help='0=linear,1=polynomial,2=RBF')
    parser.add_argument('--c',default=-1.0,help='')
    parser.add_argument('--d',default=-1.0,help='')
    parser.add_argument('--j',default=-1.0,help='')
    parser.add_argument('--g',default=-1.0,help='')
    args = parser.parse_args()
    kernal = int(args.kernal)
    c = str(args.c)
    d = str(args.d)
    j = str(args.j)
    g = str(args.g)
    out_base_name = args.file_set.replace("*","star")+"_"
    sorted_file_glob = sorted(glob(args.file_set))
    return sorted_file_glob,kernal,c,d,j,g,out_base_name


named_vector_file_name_list,kernal,c,d,j,g,out_base_name = getargs()
#if kernal == 2 and (c == None or j == None or g == None):
#    print("Need values for c,j, and g exiting.")
#    exit()    
    
svm_learn_path = "./svm_learn"

#example_file_dict = makeexamplefiles(named_vector_file_name_list)
example_list = []
class_name_collision_check_list = []
for featurized_file_with_ID in named_vector_file_name_list:
     #Get class name.
     class_name = featurized_file_with_ID.split(".")[0]
     #feature_ClassificationSet = ClassificationSet(class_name,k)
     
     if class_name in class_name_collision_check_list:
          print("ERROR Overlapping class names found:",class_name)
          exit()
     class_name_collision_check_list.append(class_name)
     
     #Add the data points in the file to ClassificationSet
     #example_list = []
     for line in open(featurized_file_with_ID,"r"):
        example_list.append(FeaturePoint(line))
     #feature_ClassificationSet.addclasspointlist(example_list)
     #This list contains all ClassificationSet objects.
     #These should all contain the same training IDs.
     #feature_ClassificationSet_list.append(feature_ClassificationSet)
     #print(feature_ClassificationSet.class_name,len(feature_ClassificationSet.FeaturePoint_class_list))
     


#print(example_file_dict)
#for ex_file in class_name_collision_check_list:
last_trn_len = None
print(class_name_collision_check_list)
if kernal == 2:
        #for class_name in class_name_collision_check_list:
        
        for class_name in class_name_collision_check_list:
            #for n class_types make plus negative files.
            #Will need to make one for every class. 
            ex = []
            neg_examples = 0
            pos_examples = 0
            for example in example_list:
                #print(example.true_class_name,class_name,class_name1)
                if example.true_class_name == class_name:
                    ex.append(example.getPositivepoint())
                    pos_examples+=1
                else:
                    ex.append(example.getNegativepoint())
                    neg_examples+=1
            print(class_name,pos_examples,neg_examples,len(ex))
            
            if last_trn_len == None:
                last_trn_len = len(ex)
            assert len(ex) == last_trn_len
            last_trn_len = len(ex)
            
            #print("\n".join(ex))
            #exit()
            training_file = tempfile.NamedTemporaryFile(mode='w')  
            training_file.write("\n".join(ex))
            training_file.flush()
            
            model_file_name = class_name+"."+out_base_name+".t2_c"+c+"_j"+j+"_g"+g+".model"
            print(model_file_name)
            subprocess.call("./svm_learn -z c -t 2 "+" -c "+c+" -j "+j+" -g "+g+" "+
                            training_file.name+" "+
                            model_file_name,shell=True,stdout=open(os.devnull, 'w'))# 
            training_file.close()
else:
        print("Kernal ",kernal,"is not supported. Exiting.")

"""
svml = SVMLearn()
svml.setSVMLearnPath(svm_learn_path)  
svml.setRDF(c,g,d,ex_file)  
subp_str = svml.getExecutionString()
print(subp_str)
output = subprocess.call(subp_str,shell=True)
"""

