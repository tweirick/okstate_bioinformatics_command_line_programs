'''


'''

import argparse
from glob import glob
from sys import exit
import os
import subprocess
from time import time
from math import sqrt


def model_cals(true_pos,true_neg,false_pos,false_neg):

    calcs_out_dict = {}
    #print(true_pos,true_neg,false_pos,false_neg)
    #Average Accuracy
    #average_accuracy = 0
    calcs_out_dict.update({"Accuracy":
                        100*(true_pos+true_neg)/(true_pos+true_neg+false_pos+false_neg)})
    
    if true_pos+false_pos != 0:
        calcs_out_dict.update({"Precision" :100*true_pos/(true_pos+false_pos)})
    else:
        calcs_out_dict.update({"Precision" : 0})
        
    if true_pos+false_neg != 0:
        calcs_out_dict.update({"Sensitivity":100*true_pos/(true_pos+false_neg)})
    else: 
        calcs_out_dict.update({"Sensitivity":0})
    
    if true_neg+false_pos != 0:
        calcs_out_dict.update({"Specificity":100*true_neg/(true_neg+false_pos)})
    else: 
        calcs_out_dict.update({"Specificity":0})

    #average_mmc = 0
    #Average MCC Matthews correlation coefficient
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

    return calcs_out_dict




base = "lrnscr.matrix.cnt"
delim = "_"
star = "*"
file_glob = glob("*"+base)

print(len(file_glob))

number_list = []

for file_name in file_glob:
    start_of_file = file_name.split(base)[0]
    number = start_of_file.split(delim)[-1]
    
    if not number in number_list:
        number_list.append(number)




for numb in sorted(number_list):
    #print(star+delim+numb+base)
    file_glob = glob(star+delim+numb+base)
    #print(file_glob)
    is_first = True 
    
    out_numbs_list = []
    for file_name in file_glob:
        for line in open(file_name,"r"):
            
            if is_first:
                is_first = False 
                out_numbs_list = line.split()
                #for sub_i in range(0,len(out_numbs_list)):
                #    if out_numbs_list[sub_i].isdigit():
                #        out_numbs_list[sub_i] = int(out_numbs_list[sub_i])
                     
            else:
                current_line = line.split()
                for i in range(0,len(current_line)):
                    if out_numbs_list[i].isdigit():

                       out_numbs_list[i] = str(int(out_numbs_list[i])+int(current_line[i]))
    temp_out_str = []          
    for i6 in range(0,len(out_numbs_list),6):        
        #print(out_numbs_list)
        calcs_dict = model_cals(int(out_numbs_list[i6+5]),#true_pos,
                                int(out_numbs_list[i6+3]),#true_neg,
                                int(out_numbs_list[i6+2]),#false_pos,
                                int(out_numbs_list[i6+1]))#false_neg)

        for calc in sorted(list(calcs_dict.keys())):
            temp_out_str.append(out_numbs_list[i6]+"_"+calc+" "+str(calcs_dict[calc]))
            
    print(numb+" "+" ".join(temp_out_str))
            
            

            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
    