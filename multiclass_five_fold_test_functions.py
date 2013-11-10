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

from sys import exit
try:
    from glob import glob
except:
    print("ERROR: Cannot import glob.")
    
import os
import subprocess
from time import time
from math import sqrt


class FastaClass():
    
    def __init__(self,class_name,sequence_list):
        self.class_name    = class_name
        self.sequence_list = sequence_list


class SVMLearn():
    def __init__(self):
        self.example_file = ""
        self.model_file   = ""
        self.svm_kernal   = ""
        

class SVMClassify():
    #svm_classify [options] example_file model_file output_file
    def __init__(self):
        self.example_file
        self.model_file
        self.output_file



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


