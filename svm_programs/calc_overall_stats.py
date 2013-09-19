'''
run_svm_learn.py
@author: Tyler Weirick
@Created on: 7/16/2012 Version 0.0 
@language:Python 3.2
@tags: overall stats


'''
import argparse
from glob import glob
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

def getargs(ver='%prog 0.0'):

    parser = argparse.ArgumentParser(description=getheadcomments())    
    
    parser.add_argument('--file_set', 
                        help='')

    args = parser.parse_args()
    return sorted(glob(args.file_set))


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




#=============================================================================
#                              Main program 
#=============================================================================


five_fold_glob= getargs(ver='%prog 0.0')

#In this file glob there should be 5 files of the same type with the format 
#of EST 52 51 469 151 99 LDA1 27 16 594 61 34 LDA2 .....
out_dict_list = []
for file_name in five_fold_glob:
 
    round_dict = {}   
 
    for line in open(file_name,"r"):
        sp_line = line.split()    

        for i in range(0,len(sp_line)-1,6):
            CLASS_NAME = sp_line[(i)]
            FN = float(sp_line[(i+1)])
            FP = float(sp_line[(i+2)])
            TN = float(sp_line[(i+3)])
            TP = float(sp_line[(i+5)])
            TOTAL = float(sp_line[(i+4)])
            
            #if CLASS_NAME == "LDA4":
            #    print(sp_line[i:i+6],sp_line[i+4],TOTAL,"-------------")       
            tmp_dict = model_cals(TP,TN,FP,FN)
   
            tmp_dict.update({"1TOTAL":TOTAL})
    
            round_dict.update({CLASS_NAME:tmp_dict})
            #if CLASS_NAME == "LDA4":
            #    print(round_dict,"-------------")               
    #Should contain 5 entries        
    out_dict_list.append(round_dict)    
                    

#print(out_dict_list)
 
keys = out_dict_list[0].keys()
keys = sorted(list(keys))             

output_list = []

#print(keys)

for class_name in keys:

    
    stat_types =  sorted(list(out_dict_list[0][class_name].keys()))
 
    out_str_list = []
    #out_str_list.append(class_name)
    #if class_name == "LDA4":
    #    print(stat_types)
    
    for stat_type in stat_types:
        tmp_stat    = 0
        tmp_seq_num = 0
        tmp_total   = 0
        average     = 0
        
        if stat_type != "1TOTAL":
            #print(stat_type)
            
            for sub_dict in out_dict_list:
                #print(sub_dict[class_name][stat_type])
                tmp_stat =sub_dict[class_name][stat_type]
                tmp_seq_num=sub_dict[class_name]["1TOTAL"]
                tmp_total+=tmp_seq_num
                average+=(tmp_stat*tmp_seq_num)
                
            if tmp_total != 0: 
                out_str_list.append( str(average / tmp_total) )
            else:
                out_str_list.append(str(0))
        

    #out_str_list.append("\n")
    output_list.append(class_name+" "+
                       str(tmp_total)+" "+ 
                       " ".join(out_str_list))    
            
overall_out = []
#Do for all but first to skip total
for calc_type in range(0,len(stat_types[1:])):
    sum_of_total=0
    calc_val = 0
    for class_key in range(0,len(keys)):
        total = float(output_list[class_key].split()[1])
        sum_of_total+=total
        #Values start from 2
        calc_val+=total*float(output_list[class_key].split()[calc_type+2])
        #print(calc_val)
        
        
    overall_out.append(str(calc_val/sum_of_total))
overall_out = ["Overall",str(sum_of_total)] + overall_out
#    #for calc_type in output_list
#    #total = e[1]
    
print(keys)

#print(stat_types) 

print(out_str_list)    
print("class"," ".join(stat_types))
for e in output_list:
    print(e)
print(" ".join(overall_out) )   
    

    
"""
    TP,TN,FP,FN = 0,0,0,0
    
    for line in open(file_name,"r"):
        sp_line = line.split()          
        #if len(sp_line)%5 == 0:
        
'FN','FP','TN' ,'TP','TOTAL'    
"""