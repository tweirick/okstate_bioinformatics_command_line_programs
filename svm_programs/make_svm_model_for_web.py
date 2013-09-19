import argparse
from glob import glob
from sys import exit
import os
import subprocess
from time import time
from math import sqrt



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








named_vector_file_name_list = glob("web_data_set.dipep.8-28-2012.veccomb")


svm_learn_path = "./svm_learn"
c        = "50"
d        = "0"
g        = "400"

example_file_dict = makeexamplefiles(named_vector_file_name_list)

for ex_file in example_file_dict.keys():

    svml = SVMLearn()
    svml.setSVMLearnPath(svm_learn_path)  
    svml.setRDF(c,g,d,ex_file)  
    subp_str = svml.getExecutionString()

    output = subprocess.call(subp_str,shell=True)








