"""
@author: Tyler Weirick
@date: 2013-5-20
This script used the pysvmlight library to preforme n-fold testing.

"""

from random    import shuffle
from math      import sqrt
from sys       import hexversion
from itertools import izip, chain, repeat
from glob      import glob
import operator
#SVM light library downloaded from.
#https://bitbucket.org/wcauchois/pysvmlight
import svmlight

#if hex(hexversion) > "0x30200f0":
def getargs():
    import argparse
    parser = argparse.ArgumentParser(description='Do training.')
    parser.add_argument(
        '--training_vecs', 
        type=str, 
        help='')
    parser.add_argument(
        '--n_folds', 
        type=int, 
        default=5,
        help='')
    parser.add_argument(
        '--x_shuffles', 
        type=int,
        default=1, 
        help='')
    parser.add_argument(
        '--input_file_format', 
        type=str,
        default='SVMLIGHT', 
        help='SVMLIGHT')
    """
    parser.add_argument(
        '--always_negative_set', 
        type=int,
        default=1 
        help='')
    """
    args = parser.parse_args()
    training_vecs = sorted(glob(args.training_vecs))
    n_folds       = args.n_folds
    x_shuffles    = args.x_shuffles
    input_file_format    = args.input_file_format

    return training_vecs,n_folds,x_shuffles,input_file_format
#else:
#    print("This version of python is not supported. Exiting.")

 

class PerformanceCalculation():

    def __init__(self,FN=0,FP=0,TN=0,TP=0):
        self.FN = float(FN)
        self.FP = float(FP)
        self.TP = float(TP)
        self.TN = float(TN)
        
    def getaccuracy(self):
        numerator   = float(100*(self.TP+self.TN))
        denominator = float((self.TP+self.TN+self.FP+self.FN))
        if denominator == 0:
            return 0
        else:
            return numerator/denominator
            
    def getprecision(self):
        numerator   = float(100*self.TP)
        denominator = float(self.TP+self.FP)
        if denominator == 0:
            return 0
        else:
            return numerator/denominator
        
    def getsensitivity(self):
        #{"Sensitivity":100*true_pos/(true_pos+false_neg)})
        numerator   = float(100*self.TP)
        denominator = float(self.TP+self.FN)
        if denominator == 0:
            return 0
        else:
            return numerator/denominator
        
    def getspecificity(self):
        #{"Specificity":100*true_neg/(true_neg+false_pos)})
        numerator   = float(100*self.TN)
        denominator = float(self.TN+self.FP)
        if denominator == 0:
            return 0
        else:
            return numerator/denominator

    def ifzeronone(self,x):
        if x == 0.0:
            return 1.0
        else: 
            return x

    def getMCC(self):
        #numerator = (true_pos*true_neg)-(false_pos*false_neg)
        #denominator = (true_pos+false_pos)*(true_pos+false_neg)*(true_neg+false_pos)*(true_neg+false_neg) 
        numerator   = float(self.TP*self.TN-self.FP*self.FN)

        a=self.ifzeronone(self.TP+self.FP)
        b=self.ifzeronone(self.TP+self.FN)
        c=self.ifzeronone(self.TN+self.FP)
        d=self.ifzeronone(self.TN+self.FN)

        denominator = float(sqrt(a*b*c*d))

        if denominator == 0:
            return 0
        else:
            return numerator/denominator
    
    def geterror(self):
        #({"Error": 100*numerator/denominator })  numerator   = 100*TP
        #numerator   = (false_pos+false_neg)
        #denominator = (true_pos+true_neg+false_pos+false_neg)
        numerator   = float(100*self.FP+self.FN)
        denominator = float(self.TP+self.TN+self.FP+self.FN)
        if denominator == 0:
            denominator=-1
        return numerator/denominator

    def getperformance(self):
        rtrn_str = (
        'accuracy: {number:.{digits}f}'.format(number=(self.getaccuracy()),digits=2)+"\t"+
        'error: {number:.{digits}f}'.format(number=(self.geterror()),digits=2)+"\t"+
        'getMCC: {number:.{digits}f}'.format(number=(self.getMCC()),digits=5)+"\t"+
        'precision: {number:.{digits}f}'.format(number=(self.getprecision()),digits=2)+"\t"+
        'sensitivity: {number:.{digits}f}'.format(number=(self.getsensitivity()),digits=2)+"\t"+
        'specificity: {number:.{digits}f}'.format(number=(self.getspecificity()),digits=2)+"\t"+
        'FN: '+str(self.FN)+"\t"+
        'FP: '+str(self.FP)+"\t"+
        'TP: '+str(self.TP)+"\t"+
        'TN: '+str(self.TN)+"\t"
         )
        return rtrn_str
    


    def getperformanceasdict(self):
        rtrn_str = {
        "accuracy"   :self.getaccuracy(),
        "error"      :self.geterror(),
        "mcc"        :self.getMCC(),
        "precision"  :self.getprecision(),
        "sensitivity":self.getsensitivity(),
        "specificity":self.getspecificity(),
        "FN"        :self.FN,
        "FP"  :self.FP,
        "TP":self.TP,
        "TN":self.TN
         }
        return rtrn_str


    def gettitle(self):
        rtrn_str = (
        'accuracy   \t'+
        'error      \t'+
        'MCC        \t'+
        'precision  \t'+
        'sensitivity\t'+
        'specificity')
        
        return rtrn_str

#=============================================================================
#                                Functions
#=============================================================================


def maketrainingandtestingsets(class_vecs_dict,run_params_dict,fold_level):
    """
    """
    training_vecs_dict = {}
    testing_vecs_dict  = {}
    """
    First split the vectors for each class into training and testing sets. 
    Populating a dictionary with each. Using class names as key values.
    """
    for vec_class in class_vecs_dict:
        #Get class training and testing sequences for a fold. 
        #num_of_vecs_in_class = len(class_vecs_dict[vec_class])
        min_els_per_fold     = len(class_vecs_dict[vec_class])/int(n_folds)
        remainder = min_els_per_fold % run_params_dict["max_folds"]

        if remainder < run_params_dict["max_folds"]-1:
            start = min_els_per_fold*fold_level+fold_level
            stop = start+min_els_per_fold+1
        else:#No remainder
            start = min_els_per_fold*fold_level+fold_level
            stop = start+min_els_per_fold

        if fold_level == 0:
            #Fold 0
            tmp_training_vecs = class_vecs_dict[vec_class][stop:]
            tmp_test_vecs     = class_vecs_dict[vec_class][:stop]
        elif fold_level == run_params_dict["max_folds"]-1:
            #Last Fold
            tmp_training_vecs = class_vecs_dict[vec_class][:start-1]
            tmp_test_vecs     = class_vecs_dict[vec_class][start-1:]
        else:
            #Middle Fold
            tmp_training_vecs = class_vecs_dict[vec_class][:start]+class_vecs_dict[vec_class][stop:]
            tmp_test_vecs     = class_vecs_dict[vec_class][start:stop]

        training_vecs_dict.update({vec_class:tmp_training_vecs})
        testing_vecs_dict.update( {vec_class:tmp_test_vecs})
        
    """
    Now there are two dicts on containing all sequences to be used in 
    training for one fold. The other containing all sequences to be use in 
    testing of the fold. From this we will make a model and store in a new 
    dict. We can then let the training_vecs_dict be garbage collected.
    """
    #Model dict contains a class name for keys and svm models for values. 
    model_dict = {}
    
    xp=0
    xn=0 
    for vector_class in dict_of_class_lists:
        vectors_for_model_list = []
        for training_vc_class in training_vecs_dict:
            for single_class_vec in training_vecs_dict[training_vc_class]:
                if vector_class == training_vc_class:
                    vectors_for_model_list.append( (1,single_class_vec) )
                else:
                    vectors_for_model_list.append( (-1,single_class_vec) )
                
        fold_model = svmlight.learn(
        vectors_for_model_list, 
        type='classification',kernel=svm_kernal,
        C=run_params_dict["c"],
        rbf_gamma=run_params_dict["gamma"],
        costratio=run_params_dict["c_ratio"]
        )
     
        model_dict.update({vector_class:fold_model})
     
    return model_dict,testing_vecs_dict



def oneagainstrestkfoldtest(dict_of_class_lists,run_params_dict):
    
    svm_kernal="rbf"
    overall_result_dict = {"FP":0,"FN":0,"TN":0,"TP":0}
    n = len(dict_of_class_lists)

    overall_confusion_matrix = {
        y:{x:0 for x in dict_of_class_lists} for y in dict_of_class_lists
    }

    class_performance = {}
    for key_el in dict_of_class_lists:
        class_performance.update({key_el:{"FP":0,"FN":0,"TN":0,"TP":0}})

    for fold_level in range(0,n_folds):
        #Make training and testing data as lists.
        result_dict = {"FP":0,"FN":0,"TN":0,"TP":0}

        fold_confusion_matrix = {
            y:{x:0 for x in dict_of_class_lists} for y in dict_of_class_lists
        }
        #Make fold models
        models_dict,test_data_dict = maketrainingandtestingsets(
            dict_of_class_lists,
            run_params_dict,
            fold_level
        )


        for class_of_vecs_being_tested_1 in test_data_dict:
            pred_values_list = []
            for class_of_vecs_being_tested in test_data_dict:
            
                for single_test_vec in test_data_dict[class_of_vecs_being_tested]:
                    pred_values_dict = {}
                    for model_name in models_dict:
                        #print(model_name,class_of_vecs_being_tested)
                        pred = svmlight.classify(
                                models_dict[model_name],
                                [(0,single_test_vec)],
                        )
                        pred_values_dict.update({model_name:pred[0]})    
                    pred_values_list.append(
                        [class_of_vecs_being_tested,pred_values_dict])      
                        #pred_values_list.append( [model_name,class_of_vecs_being_tested_1,pred_values_dict] )

                        #print(pred_values_list)
                        #Vectors contained as values in test_data_dict are true positves
                        #for the key to access them. 
                        #pred_values_dict = {}
                        #for class_of_vecs_being_tested_1 in test_data_dict:
                        #    for single_test_vec in test_data_dict[class_of_vecs_being_tested_1]:
                        #        for model_name in models_dict:
                        #            #print(model_name,class_of_vecs_being_tested)
                        #            pred = svmlight.classify(
                        #                models_dict[model_name],
                        #                [(0,single_test_vec)],
                        #            )                   
                        #            pred_values_dict.update( {model_name:pred[0]} )
            
            result_dict = {"FP":0,"FN":0,"TN":0,"TP":0}
            for vec_pred_el in pred_values_list:
                tp_class = vec_pred_el[0]
                tp_preds = vec_pred_el[1]
                sorted_preds = sorted(tp_preds, key=tp_preds.get, reverse=True)
                class_of_max_pred = sorted_preds[0]
                #second_max_val = sorted_preds[1]
                #Get the max value 
                #class_of_max_pred = sorted(pred_values_dict, key=pred_values_dict.get, reverse=True)[0]
                #second_max_val = sorted(pred_values_dict, key=pred_values_dict.get, reverse=True)[1]
                #assert pred_values_dict[class_of_max_pred] != pred_values_dict[second_max_val]
                #If max value greater than zero 
                #If max value is unique
                #If none greater than zero
                #test_class_vec_list true postive class
                #tested agaisnt the model 
                #class_of_max_pred the prediction value
                if class_of_vecs_being_tested_1 == tp_class:
                    if (class_of_vecs_being_tested_1 == class_of_max_pred and
                    tp_preds[class_of_max_pred] >= 0):
                        result_dict["TP"]+=1
                        overall_result_dict["TP"]+=1
                        p = "TP"
                        #overall_confusion_matrix[class_of_max_pred][class_of_vecs_being_tested]+=1
                        #fold_confusion_matrix[class_of_max_pred][class_of_vecs_being_tested]+=1
                    else:
                        result_dict["FN"]+=1
                        overall_result_dict["FN"]+=1
                        p = "FN"
                else:
                    if (class_of_vecs_being_tested_1 == class_of_max_pred and
                    tp_preds[class_of_max_pred] >= 0):
                        result_dict["FP"]+=1
                        overall_result_dict["FP"]+=1
                        #overall_confusion_matrix[class_of_max_pred][class_of_vecs_being_tested]+=1
                        #fold_confusion_matrix[class_of_max_pred][class_of_vecs_being_tested]+=1
                        p = "FP"
                    else:
                        result_dict["TN"]+=1
                        overall_result_dict["TN"]+=1     
                        p = "TN"
                #print(class_of_vecs_being_tested_1,tp_class,class_of_max_pred,tp_preds[class_of_max_pred],p)
            class_performance[class_of_vecs_being_tested_1]["FN"]=result_dict["FN"]
            class_performance[class_of_vecs_being_tested_1]["FP"]=result_dict["FP"]
            class_performance[class_of_vecs_being_tested_1]["TN"]=result_dict["TN"]
            class_performance[class_of_vecs_being_tested_1]["TP"]=result_dict["TP"]

            #perf_calc = PerformanceCalculation(
            #    FN=result_dict["FN"],
            #    FP=result_dict["FP"],
            #    TN=result_dict["TN"],
            #    TP=result_dict["TP"]
            #)   
            """   
            print(
                  class_of_vecs_being_tested_1+str(fold_level)+"\t"+ 
                  "kernal: "+str(svm_kernal)+"\t"+ 
                  "c: "+str(c_val)+"\t"+ 
                  "gamma: "+str(gamma_val)+"\t"+ 
                  "costratio: "+str(c_ratio_val)+"\t"+ 
                  perf_calc.getperformance())
            """

    #Performance Per Class
    #print("=================================")
    class_perf_out_list = [
              "kernal: "+str(svm_kernal)+"\t"+
              "c: "+str(c_val)+"\t"+
              "gamma: "+str(gamma_val)+"\t"+
              "costratio: "+str(c_ratio_val)+"\t"]
    for key_el in sorted(test_data_dict.keys()):

        perf_calc = PerformanceCalculation(
            FN=class_performance[key_el]["FN"],
            FP=class_performance[key_el]["FP"],
            TN=class_performance[key_el]["TN"],
            TP=class_performance[key_el]["TP"])   
        
        pref_str = (
              "CLASS:"+key_el+"\t"+ 
              perf_calc.getperformance()
              )
        #print(pref_str)
        class_perf_out_list.append(pref_str)

    #print("-----------------------------------")
        #Overall Stats
    overall_perf = PerformanceCalculation(
        FN=overall_result_dict["FN"],
        FP=overall_result_dict["FP"],
        TN=overall_result_dict["TN"],
        TP=overall_result_dict["TP"])  
 
    #print(
    #      "overall:"+"\t"+ 
    #      "kernal: "+str(svm_kernal)+"\t"+ 
    #      "c: "+str(c_val)+"\t"+ 
    #      "gamma: "+str(gamma_val)+"\t"+ 
    #      "costratio: "+str(c_ratio_val)+"\t"+ 
    #      overall_perf.getperformance()
    #)
    #for matrix_line in overall_confusion_matrix:
    #    print(matrix_line)

    return overall_perf.getperformanceasdict(),"\n".join(class_perf_out_list) #overall_result_dict


def shuffledaveragedkfoldtest(dict_of_class_lists,run_params_dict,x_shuffles):

    average_perf_dict = PerformanceCalculation().getperformanceasdict()

    overall_shuffle_dict_list = [] 

    for i in range(1,x_shuffles+1):
        if x_shuffles > 0:
            #Shuffle the elements of the lists 
            for vector_class in dict_of_class_lists: 
                #Do not need to reassign
                shuffle(dict_of_class_lists[vector_class])
        
        #Performance of one full k-fold test.
        result_dict = oneagainstrestkfoldtest(dict_of_class_lists,run_params_dict)

        #Store performaces
        overall_shuffle_dict_list.append(result_dict)
    
    #Sum the dictionary elements.
    for perf_dict_el in overall_shuffle_dict_list:
        for avg_key_el in average_perf_dict:
            #print(average_perf_dict,perf_dict_el)
            average_perf_dict[avg_key_el]+=perf_dict_el[avg_key_el]
    
    #Divide dict elements by length to average. 
    for avg_key_el in average_perf_dict:
        average_perf_dict[avg_key_el] = average_perf_dict[avg_key_el]/len(overall_shuffle_dict_list)
    
    return average_perf_dict
        


def makepysvmlightvectorlist(file_name_list,input_file_format):
    vector_list_dict = {}

    for file_name in file_name_list: 
         
        #Remove file path if present.
        class_name = file_name
        if "/" in file_name:    
            class_name = file_name.split("/")[-1]

        vector_list = []
        for example_vector_list in open(file_name,"r"):
            if input_file_format == "SVMLIGHT":
                #Build vector list 
                tmp_list = []
                for el in example_vector_list.split()[1:]:
                    el1,el2 = el.strip().split(":")
                    tmp_list.append( (int(el1),float(el2)) )

                #Add the vector list to class list. 
                vector_list.append( tmp_list )
            else:
                print("ERROR")
        #Add a vector class to the classification dict
        vector_list_dict.update( {class_name:vector_list} )

    return vector_list_dict

#=============================================================================
#                                Main Program
#=============================================================================

file_name_glob,n_folds,x_shuffles,input_file_format = getargs()

pos_ex_cnt = 0
neg_ex_cnt = 0
best_vals = None
best_mcc  = None
c_start,c_end,c_parts = 1,500,25
j_start,j_end,j_parts = 1,500,25
g_start,g_end,g_parts = 1,500,25
svm_kernal = "rbf"

"""
First make a dictionary with class names as keys and the vector elements 
converted to keys. Additionally the vector elements will be converted to lists
of tuples needed for svmlight format.
Ex: 
{"class1":[(1, 0.13456), (2, 0.02902), (3, 0.04749),...],...}
"""
dict_of_class_lists = makepysvmlightvectorlist(file_name_glob,input_file_format)

best_average_mcc = None
best_class_str   = ""

for c_val in range(c_start,c_end,c_parts):
    for gamma_val in range(j_start,j_end,j_parts):
        for c_ratio_val in range(g_start,g_end,g_parts):

            run_params_dict = {
                "c"         : c_val,
                "gamma"     : gamma_val,
                "c_ratio"   : c_ratio_val,
                "max_folds" : n_folds
            }
            overall_perf_dict,class_perf_str = oneagainstrestkfoldtest(dict_of_class_lists,run_params_dict)

            #average_perf_dict = shuffledaveragedkfoldtest(
            #    dict_of_class_lists,
            #    run_params_dict,
            #    x_shuffles
            #)

        if(best_average_mcc == None or best_average_mcc < overall_perf_dict["mcc"]):
            #Calculate performaces averages mean and varience,etc, of performance statistics
            best_average_mcc = overall_perf_dict["mcc"]

            best_class_str=(
                "kernal: "+str(svm_kernal)+"\t"+
                "c: "+str(c_val)+"\t"+
                "gamma: "+str(gamma_val)+"\t"+
                "costratio: "+str(c_ratio_val)+"\t"
            )

            for e in sorted( overall_perf_dict.keys() ):
                 best_class_str =  best_class_str+ e+": "+str(overall_perf_dict[e])+"\t"

            print("============================================")
            print("best_overall:\t"+best_class_str)
            print("By Class:")
            print(class_perf_str)            

"""
if pred_values_dict[class_of_max_pred] >= 0:
    if class_of_vecs_being_tested == class_of_max_pred:
        #print(class_of_vecs_being_tested,pred_values_dict)
        #and preds_dict[class_of_max_pred] != preds_dict[second_max_val]):
        result_dict["TP"]+=1
        overall_result_dict["TP"]+=1
    else:#class_of_vecs_being_tested != class_of_max_pred:
        result_dict["FP"]+=1
        overall_result_dict["FP"]+=1
    overall_confusion_matrix[class_of_max_pred][class_of_vecs_being_tested]+=1
    fold_confusion_matrix[class_of_max_pred][class_of_vecs_being_tested]+=1
else:
    if class_of_vecs_being_tested == class_of_max_pred:
        result_dict["FN"]+=1
        overall_result_dict["FN"]+=1
    else:
        result_dict["TN"]+=1
        overall_result_dict["TN"]+=1      
"""                     
