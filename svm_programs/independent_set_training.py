from z_optimizing_multiclass_k_fold_tests_classes import *
from z_optimizing_multiclass_k_fold_tests_functions import *
from sys import exit
from glob import glob
import os
import subprocess
from time import time
from math import *
import tempfile
import argparse


def average(s): return sum(s) * 1.0 / len(s)
def range1(s): 
    s=sorted(s)
    return s[0] - s[-1]

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
    parser.add_argument('--vector_files',default="",help='Some percentage of files left out converted to vectors.')
    parser.add_argument('--model_files',default="",help='')
    args = parser.parse_args()
    return sorted(glob(args.vector_files)),sorted(glob(args.model_files)),args.vector_files


"""
    #Make the training file. 
    training_file = tempfile.NamedTemporaryFile(mode='w')  
    training_file.write(training_data)
    training_file.flush()
    #Make the model data into this file.
    model_file = tempfile.NamedTemporaryFile(mode='r')        
    training_file.close()
    
    test_file = tempfile.NamedTemporaryFile(mode='w')
    test_file.write(test_str)
    test_file.flush()
    #print(test_file.readlines())
    predictions_file = tempfile.NamedTemporaryFile(mode='r')
    #svm_classify example1/test.dat example1/model example1/predictions
"""

#Get Independent Vectors and Model Files.
#Make feature objects from vector files.
#Classify with each model file?

vec_file_names,model_file_names,glob_term = getargs()

e = sorted(vec_file_names)
m = sorted(model_file_names)
for i_cnt in range(0,len(vec_file_names)):
    print(e[i_cnt],"->",m[i_cnt])

out_base_name = glob_term.replace("*","")+"_"+str(int(time()))


#class_names_from_model_files = {}
#for model_file_name in model_file_names:
#    class_names_from_model_files.update( {model_file_name.split(".")[0]} )
    
class_name_collision_check_list = []
vector_to_classify_list = []
vector_txt_list = []
for vec_file_name in vec_file_names:
     
     #class_name = vec_file_name.split("/")[-1].split(".")[0]
     class_name = vec_file_name.split(".")[0]

     
     if class_name in class_name_collision_check_list:
          print("ERROR Overlapping class names found:",class_name)
          exit()
     class_name_collision_check_list.append(class_name)
     
     
     for line in open(vec_file_name,"r"):
        tmp_feature_point = FeaturePoint(line)
        assert tmp_feature_point.true_class_name.upper() == class_name.upper(),tmp_feature_point.true_class_name.upper()+"|"+class_name.upper()
        tmp_fp = FeaturePoint(line)
        vector_to_classify_list.append(tmp_fp)
        vector_txt_list.append(tmp_fp.getZeroPoint())
    

vector_txt = "\n".join(vector_txt_list)+"\n"

class_of_highest_value = ""
highest_value          = ""
highest_pred_value = None
highest_pred_value_class = "UNKNOWN"
all_values = set()

for model_file_name in model_file_names:

        class_name = model_file_name.split(".")[0] 
        test_file = tempfile.NamedTemporaryFile(mode='w')  
        test_file.write(vector_txt)
        test_file.flush()

        predictions_file = tempfile.NamedTemporaryFile(mode='r')

        subprocess_val = subprocess.call("./svm_classify "+test_file.name+" "+model_file_name+" "+predictions_file.name,
                        shell=True,stdout=open(os.devnull, 'w'))
              
        test_file.close()
        pred_val_lines = predictions_file.readlines()
        assert len(pred_val_lines) == len(vector_to_classify_list),str(len(pred_val_lines))+"|"+str(len(vector_to_classify_list))+"|"+model_file_name
        
        for tmp_i in range(0,len(pred_val_lines)):
            
            line_val = float(pred_val_lines[tmp_i].strip())
            all_values.add((line_val))
            if vector_to_classify_list[tmp_i].value_of_pred == None:
                vector_to_classify_list[tmp_i].value_of_pred = line_val
                vector_to_classify_list[tmp_i].predicted_class = class_name
            elif vector_to_classify_list[tmp_i].value_of_pred < line_val:
                vector_to_classify_list[tmp_i].value_of_pred = line_val
                vector_to_classify_list[tmp_i].predicted_class = class_name
            elif vector_to_classify_list[tmp_i].value_of_pred == line_val:           
                #vector_to_classify_list[tmp_i].value_of_pred = line_val
                vector_to_classify_list[tmp_i].predicted_class = "UNKOWN"
                           
        predictions_file.close()
        

    
    
performance_dict = calculateOverallMCC(vector_to_classify_list,class_name_collision_check_list)

out_list = [asctime(),
            " MCC="+str(performance_dict["mcc"])+
            " accuracy="+str(performance_dict["accuracy"])+
            " precision="+str(performance_dict["precision"])+
            " sensitivity="+str(performance_dict["sensitivity"])+
            " specificity="+str(performance_dict["specificity"])+
            " error="+str(performance_dict["error"])+                            
            " FN="+str(performance_dict["FN"])+
            " FP="+str(performance_dict["FP"])+
            " TN="+str(performance_dict["TN"])+
            " TP="+str(performance_dict["TP"])+
            " total_seqs="+str(performance_dict["total_seqs"])+"\n"]

num_vals=[]

for e in vector_to_classify_list:    
    num_vals.append(e.value_of_pred)
    if e.value_of_pred in all_values:
        all_values.remove(e.value_of_pred)


neg_vals = list(all_values)


print("Positive Values -----------------")  
avg = average(num_vals)
print("average ",avg)
rng = range1(num_vals)
print("range ",rng)
vari = list(map(lambda x: (x - avg)**2, num_vals))
standard_deviation = sqrt(average(vari))
print("stddev ",standard_deviation)
print("Negative  Values -----------------")  
avg = average(neg_vals)
print("average ",avg)
rng = range1(neg_vals)
print("range ",rng,sorted(neg_vals)[0],sorted(neg_vals)[-1])
vari = list(map(lambda x: (x - avg)**2, neg_vals))
standard_deviation = sqrt(average(vari))
print("stddev ",standard_deviation)

print("\n".join(out_list))

file = open("independent_test_stats"+out_base_name+".txt",'w')
file.write("\n".join(out_list))
file.close()
#Vector Type
#Time
#Conditions
file = open("independent_test_confusion_matrix"+out_base_name+".txt",'w')
file.write(makeconfusionmatrix(vector_to_classify_list,class_name_collision_check_list))
file.close()
    
    

    
    
    


