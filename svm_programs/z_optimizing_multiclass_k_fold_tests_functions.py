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
from sys import exit
from glob import glob
import os
import subprocess
from time import time
from time import asctime
from math import *
import tempfile
from random import gauss


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


try:
    import argparse
    def getargs(ver='%prog 0.0'):
        parser = argparse.ArgumentParser(description=getheadcomments())    
        parser.add_argument('--file_set',help='')
        parser.add_argument('--k' ,
                            default=5,
                            help='')
        args = parser.parse_args()
        sorted_file_glob = sorted(glob(args.file_set))
        use_vector_strings = args.k
        return sorted_file_glob,use_vector_strings
except:
    try:
        import optparse
    except:
        print("ERROR 1: Cannot import argparse or optparse")


def dofoldclassification(c_cond,j_cond,g_cond,
                         training_data,test_file_name,prediction_file_name):
    #Make the training file. 
    training_file = tempfile.NamedTemporaryFile(mode='w')  
    training_file.write(training_data)
    training_file.flush()
    
    #Make the model data into this file.
    model_file = tempfile.NamedTemporaryFile(mode='r')        
    
    #Run SVM learn svm_learn    example1/train.dat example1/model        
    

               
    subprocess.call("./svm_learn -z c -t 1 "+
     " -c "+str(c_cond)+" -j "+str(j_cond)+" -g "+str(g_cond)+
     " "+training_file.name+" "+model_file.name,
     shell=True,stdout=open(os.devnull, 'w'))# 
    #Training data is no longer needed as we now have a model file. Will be deleted on close.
    training_file.close()
      
    #svm_classify example1/test.dat example1/model example1/predictions
    subprocess.call("./svm_classify "+test_file_name+" "+model_file.name+
    " "+prediction_file_name,shell=True,stdout=open(os.devnull, 'w'))
    
    #Model file no longer needed as we have predictions. 
    model_file.close()


def get_feature_classificationset_list_and_input_class_name_list(file_glob,k):
    class_name_collision_check_list = []
    feature_ClassificationSet_list  = []

    for featurized_file_with_ID in file_glob:
         #Get class name.
         class_name = featurized_file_with_ID.split(".")[0]
         feature_ClassificationSet = ClassificationSet(class_name,k)
         
         if class_name in class_name_collision_check_list:
              print("ERROR Overlapping class names found:",class_name)
              exit()
         class_name_collision_check_list.append(class_name)
         
         #Add the data points in the file to ClassificationSet
         example_list = []
         for line in open(featurized_file_with_ID,"r"):
            example_list.append(FeaturePoint(line))
         feature_ClassificationSet.addclasspointlist(example_list)
         #This list contains all ClassificationSet objects.
         #These should all contain the same training IDs.
         feature_ClassificationSet_list.append(feature_ClassificationSet)
         print(feature_ClassificationSet.class_name,
               len(feature_ClassificationSet.FeaturePoint_class_list))
         
    assert len(class_name_collision_check_list) == len(feature_ClassificationSet_list)
    assert len(file_glob) == len(feature_ClassificationSet_list)
    return feature_ClassificationSet_list,class_name_collision_check_list


def sample_gaussian(mu,sigma,N):
    assert type(mu) == list
    assert len(mu) > 0  
    assert type(mu[0]) == float or type(mu[0]) == int
    
    assert type(sigma) == list
    assert len(sigma) > 0  
    assert type(sigma[0]) == float or type(sigma[0]) == int
    
    assert type(N) == int
    assert N > 0
    N_out_points = []
    for i in range(0,N):
        new_point = []
        for j in range(0,len(mu)): 

            new_point.append(gauss(mu[j],sigma[j]))
            
        N_out_points.append(new_point)
    return N_out_points


def meanof2Dlist(twoD_list):
    some_list = []
    cnt = 0
    #print(twoD_list)
    for i in range(0,len(twoD_list)-1):
        for j in range(0,len(twoD_list[i])):
            twoD_list[0][j]+=twoD_list[i+1][j]
        cnt+=1
    for i in range(0,len(twoD_list[0])):
        twoD_list[0][i] = twoD_list[0][i]/cnt
        
    return twoD_list[0]

def vectorsubtract(a,b):
    
     assert len(a) == len(b)
     out_vec = []
     for i in range(0,len(a)):
         out_vec.append(a[i] - b[i])
     return out_vec

def vectoraddition(a,b):

     assert len(a) == len(b)
     out_vec = []
     for i in range(0,len(a)):
         out_vec.append(a[i] + b[i])
     return out_vec

def vectormultiply(a,b):
     assert len(a) == len(b)
     out_vec = []
     for i in range(0,len(a)):
         out_vec.append(a[i] * b[i])
     return out_vec

def two_pass_2D_variance(data):
    assert len(data) > 0
    assert type(data[0]) == list
    n  = len(data)
    #sum1 = 0
   

    #for x in data:
    #    n    = n + 1
    #    sum1 = sum1 + x
    #mean = sum1/n
    mean = meanof2Dlist(data)
    print(mean)
    sum2 = []
    for e in mean:
        sum2.append(0)
    
    for x in data:
        x_minus_mean = vectorsubtract(x,mean)
        #sum2 = sum2 + (x - mean)*(x - mean)
        x_minus_mean2 = vectormultiply(x_minus_mean,x_minus_mean)
        sum2 = vectoraddition(sum2,x_minus_mean2)
    
    variance = []
    for e in sum2:
        variance.append( e/(n - 1) )
        
    return variance
    




def makeconfusionmatrix(results_list,class_name_collision_check_list):

    confusion_matrix = {}
    for e in results_list:
        print(type(e))
        comb = e.true_class_name+" "+e.predicted_class
        if comb in confusion_matrix:
            confusion_matrix[comb]+=1
        else:
            confusion_matrix.update({comb:1})
            
    horizontal_title = ["Class"]
    rows = []
    for class1 in sorted(class_name_collision_check_list):
        horizontal_title.append("Predicted_"+class1)
        other_stuff = ["Actual_"+class1]
        for class2 in sorted(class_name_collision_check_list):
            if class1+" "+class2 in confusion_matrix:
                numb_str = str(confusion_matrix[class1+" "+class2])
            else:
                numb_str = "0"    
            other_stuff.append(class1+"-"+class2+":"+numb_str)
        rows.append(" ".join(other_stuff))
    
    return(" ".join(horizontal_title) +"\n"+"\n".join(rows))
    
    

def calculateOverallMCC(results_list,class_name_collision_check_list):
    #results_list calc_class -> [FeaturePoint(),..]
    
    #Calculate Statistics need per class stats as well as overall.
    total_seqs = 0
    numerator = 0
    for class_name in class_name_collision_check_list:
        number_of_seqs_per_class = 0
        osd = {"TP":0,"TN":0,"FP":0,"FN":0}
        for e in results_list:
            if e.true_class_name == class_name:
                number_of_seqs_per_class+=1     
            osd[e.checkprediction(class_name)]+=1    
        pc = PerformanceCalculation(osd["FN"],osd["FP"],osd["TN"],osd["TP"])
        
        total_seqs+=number_of_seqs_per_class
        
        numerator+=number_of_seqs_per_class*pc.getMCC()
        
    
    return numerator/total_seqs
    
     

def optimize_c_j_g_with_NCE(pred_qual_measure_list):
    N = len(pred_qual_measure_list)
    epsilon=1e-4
    top_n_percent = 0.2
    #mu     = meanof2Dlist(points_list)

    keep = ceil(int(len(pred_qual_measure_list)*top_n_percent))
    #Get the top top_n_percent of the results.
    try:
        top_values_list = (
            sorted(pred_qual_measure_list,reverse=True)[0:keep])
    except:
        for e in pred_qual_measure_list:
            print(e)
        exit()
    #Make a list of only the points.
    points_list = []
    for preform_value in top_values_list:
        points_list.append(preform_value[1])
    #Calculate a new mu and sigma for the gaussian distribution.
    mu     = meanof2Dlist(points_list)
    sigma2 = two_pass_2D_variance(points_list)
    #Return N new points to check.
    #find largest sigma 
    
    #Need to check if max/min sigma and mu will go out of the problem bounds.  

    if sorted(sigma2,reverse=True)[0] > epsilon:#t < maxits and maxits = 100
        return sample_gaussian(mu,sigma2,N)
    else:
        return False 
             
def make_initial_RBF_point_list(c_start,c_end,j_start,j_end,g_start,g_end):
     parts = 9
     out_point_list = []
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
                 out_point_list.append([c,j,g])
                 
     out_point_list.reverse()   
     print(out_point_list)  
     return out_point_list
 





        



    

"""
    print("Classification took",time()-t1,"seconds")
    
    overall_MCC
     
    #If overall MCC higher than previous.
    if overall_MCC > highest_MCC:
        #Make Confusion Matrix
        makeconfusionmatrix()
    
    #Return a list of mcc values, and the c,j,g linked to them 
    return 
    

    
#Output overall MCC to log file.
for e in results_list:
    #
    print("sdfasdfasdf")
    #count_instances 
    
for e in osd:
    print(e,osd[e])
        #Add to predictions_class 
        #This will calculate and hold the largest value input into 
        #the class for each testing entry
        
        #Input these prediction classes into a function which will calculate over all stats 
        #And update the best entry's confusion matrix and stats, for all others simply keep 
        #The final overall calculations
        #now we should have a matrix 
        #keep for the best run and make confusion matrix 
        
        
def optimize_c_j_g_with_NCE(mu,sigma_squared,t,maxits,N,Ne):
    #[x,count,sz]
    epsilon=1^e-4
    while t < maxits and sigma2 > epsilon:
        N_points_list = sample_gaussian(mu,sigma2,N); 
        S_list = []
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11!!!!
        for point in N_points_list:
            S_list.append([function_result(c,j,g),point,])
        #Sort in desending order
        X = sorted(S_list)
        mu = meanof2Dlist(X[0:Ne]); 
        #sigma2 = var(X(1:Ne));
        sigma2 = two_pass_2D_variance(X[1:Ne])
        t = t+1;     
"""
        



        
        
    


