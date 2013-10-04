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
#SVM light library downloaded from.
#https://bitbucket.org/wcauchois/pysvmlight
import svmlight

if hex(hexversion) > "0x30200f0":
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
else:
    print("This version of python is not supported. Exiting.")

 

class PerformanceCalculation():

    def __init__(self,FN,FP,TN,TP):
        self.FN = FN
        self.FP = FP
        self.TP = TP
        self.TN = TN
        
    def getaccuracy(self):
        numerator   = 100*(self.TP+self.TN)
        denominator = (self.TP+self.TN+self.FP+self.FN)
        if denominator == 0:
            return 0
        else:
            return numerator/denominator
            
    def getprecision(self):
        numerator   = 100*self.TP
        denominator = self.TP+self.FP
        if denominator == 0:
            return 0
        else:
            return numerator/denominator
        
    def getsensitivity(self):
        #{"Sensitivity":100*true_pos/(true_pos+false_neg)})
        numerator   = 100*self.TP
        denominator = self.TP+self.FN
        if denominator == 0:
            return 0
        else:
            return numerator/denominator
        
    def getspecificity(self):
        #{"Specificity":100*true_neg/(true_neg+false_pos)})
        numerator   = 100*self.TN
        denominator = self.TN+self.FP
        if denominator == 0:
            return 0
        else:
            return numerator/denominator
    
    def getMCC(self):
        #numerator = (true_pos*true_neg)-(false_pos*false_neg)
        #denominator = (true_pos+false_pos)*(true_pos+false_neg)*(true_neg+false_pos)*(true_neg+false_neg) 
        numerator   = self.TP*self.TN-self.FP*self.FN
        denominator = sqrt((self.TP+self.FP)*(self.TP+self.FN)*(self.TN+self.FP)*(self.TN+self.FN))
        if denominator == 0:
            return 0
        else:
            return numerator/denominator
    
    def geterror(self):
        #({"Error": 100*numerator/denominator })  numerator   = 100*TP
        #numerator   = (false_pos+false_neg)
        #denominator = (true_pos+true_neg+false_pos+false_neg)
        numerator   = 100*self.FP+self.FN
        denominator = (self.TP+self.TN+self.FP+self.FN)
        return numerator/denominator

    def getperformance(self):
        rtrn_str = (
        '{number:.{digits}f}'.format(number=(self.getaccuracy()),digits=2)+"\t"+
        '{number:.{digits}f}'.format(number=(self.geterror()),digits=2)+"\t"+
        '{number:.{digits}f}'.format(number=(self.getMCC()),digits=5)+"\t"+
        '{number:.{digits}f}'.format(number=(self.getprecision()),digits=2)+"\t"+
        '{number:.{digits}f}'.format(number=(self.getsensitivity()),digits=2)+"\t"+
        '{number:.{digits}f}'.format(number=(self.getspecificity()),digits=2)
         )
        return rtrn_str
    
    def getperformanceasdict(self):
        rtrn_str = (
        "accuracy"   :self.getaccuracy(),
        "error"      :self.geterror(),
        "mcc"        :self.getMCC(),
        "precision"  :self.getprecision(),
        "sensitivity":self.getsensitivity(),
        "specificity":self.getspecificity()
         )
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

def oneifremainder(remainder):
    if remainder > 0:
        return 1,remainder-1
    return 0,0
    

def splitter(n,iterabler):
    average_len = int(len(iterabler)/int(n))
    remainder   = len(iterabler)%int(n)
    tmp_cnt     = 0
    tmp_split   = []
    out_list    = [] 
    one_or_zero, remainder = oneifremainder(remainder)
    for iter_el in iterabler:
        if len(tmp_split) == average_len+one_or_zero :
            one_or_zero, remainder = oneifremainder(remainder)
            out_list.append(tmp_split)
            tmp_split = []
        tmp_split.append(iter_el)
    out_list.append(tmp_split)
    return out_list


def maketrainingandtestingsets(i,n_pos_examples,n_neg_examples):
    #Make the training and testing data. 
    for i in range(0,n_folds):
        if fold_level != i:    
            training_data = training_data + n_pos_exs[i] 
            training_data = training_data + n_neg_exs[i]
        else:
            pos_test_data = pos_test_data + n_pos_exs[i]
            neg_test_data = neg_test_data + n_neg_exs[i]      
    return training_data,pos_test_data,neg_test_data

"""
def evaluatepredictions(predictions,predictions_are_true_positives,confusion_matrix):
    result_dict_ = {"FP":0,"FN":0,"TN":0,"TP":0}
    if predictions_are_true_positives:
        for e in predictions:
            if e >= 0:
                result_dict["TP"]+=1
            else:
                result_dict["FN"]+=1
    else:
        for e in predictions:
            if e >= 0:
                result_dict["FP"]+=1
            else:
                result_dict["TN"]+=1
    return result_dict
"""

def oneagainstrestkfoldtest(n_folds,list_of_class_lists,c_val,gamma_val,c_ratio_val):

    svm_kernal="rbf"
    overall_result_dict = {"FP":0,"FN":0,"TN":0,"TP":0}
    n = len(list_of_class_lists)
    overall_confusion_matrix = [[0]*n]*n

    for fold_level in range(0,n_folds):
        #Make training and testing data as lists.
        fold_confusion_matrix = [[0]*n]*n
        for pos_class_el_int in range(0,len(list_of_class_lists)):
            #Use each class ones as the positive training data.     
            n_pos_examples           = list_of_class_lists[class_el_int]
            n_neg_examples           = []
            #This is to print confusion matrixes. The lists are sorted during
            #input. Thus it is possible to  
            n_neg_examples_class_map = []

            for neg_classes_el_int in range(0,len(list_of_class_lists)):
                if select_el_int != neg_classes_el_int:
                    for el in list_of_class_lists[class_el_int]:
                        n_neg_examples.append(el)
                        n_neg_examples_class_map.append(select_el_int)
            train_data,pos_test_data,neg_test_data = maketrainingandtestsets(
            i,
            n_pos_examples,
            n_neg_examples
            )
            
            #Create a model for use in classification.
            fold_model = svmlight.learn(
                training_data,
                #Options 
                type='classification',
                kernel=svm_kernal,
                C=c_val,
                rbf_gamma=gamma_val,
                costratio=c_ratio_val
            )
            #Test the model.
            predictions = svmlight.classify(fold_model,pos_test_data) 
            #Evaluate the model.
            #Since we have split up the classification of true positives and 
            #true negatives we do not need to check the names of the classes.  
            for e in predictions:
                if e >= 0:
                    result_dict["TP"]+=1
                    overall_result_dict["TP"]+=1
                    overall_confusion_matrix[pos_class_el_int][n_neg_examples_class_map[pred_el_cnt]]+=1
                    fold_confusion_matrix[pos_class_el_int][n_neg_examples_class_map[pred_el_cnt]]+=1
                else:
                    result_dict["FN"]+=1
                    overall_result_dict["FN"]+=1

            #result_dict = evaluatepredictions(predictions,True,result_dict,)
            #Test the negative vectors on the model.
            predictions = svmlight.classify(fold_model,neg_test_data)    

            #Evaluate the model.
            #Since we have split up the classification of true positives and 
            #true negatives we do not need to check the names of the classes.     
            for pred_el_cnt in range( 0,len(predictions) ):
                if e >= 0:
                    result_dict["FP"]+=1
                    overall_result_dict["FP"]+=1
                    overall_confusion_matrix[pos_class_el_int][n_neg_examples_class_map[pred_el_cnt]]+=1
                    fold_confusion_matrix[pos_class_el_int][n_neg_examples_class_map[pred_el_cnt]]+=1
                else:
                    result_dict["TN"]+=1
                    overall_result_dict["TN"]+=1
            #result_dict = evaluatepredictions(predictions,False,result_dict,confusion_matrix)
            #Calculate performance of round.

        perf = PerformanceCalculation(
            FN=result_dict["FN"],
            FP=result_dict["FP"],
            TN=result_dict["TN"],
            TP=result_dict["TP"])   

        print(
              "Fold: "+str(fold_level)+"\t"+ 
              "kernal: "+str(svm_kernal)+"\t"+ 
              "c: "+str(c_val)+"\t"+ 
              "gamma: "+str(gamma_val)+"\t"+ 
              "costratio: "+str(c_ratio_val)+"\t"+ 
              perf)

        performace_calcs.getperformance()

        for matrix_line in fold_confusion_matrix:
            print(matrix_line)

    #Overall Stats
    perf = PerformanceCalculation(
        FN=result_dict["FN"],
        FP=result_dict["FP"],
        TN=result_dict["TN"],
        TP=result_dict["TP"])   

    print(
          "Fold: "+str(fold_level)+"\t"+ 
          "kernal: "+str(svm_kernal)+"\t"+ 
          "c: "+str(c_val)+"\t"+ 
          "gamma: "+str(gamma_val)+"\t"+ 
          "costratio: "+str(c_ratio_val)+"\t"+ 
          perf)

    for matrix_line in overall_confusion_matrix:
        print(matrix_line)

    return overall_result_dict.getperformanceasdict()


def shuffledaveragedkfoldtest(list_of_class_lists,c,gamma,c_ratio,x_shuffles,n_folds):

    average_perf_dict = PerformanceCalculation().getperformanceasdict()
    overall_shuffle_dict_list = [] 

    for i in range(1,x_shuffles+1):
        if number_of_shuffles > 0:
            #Shuffle the elements of the lists 
            for vcl_el_int in range(0,len(list_of_class_lists)): 
                list_of_class_lists[vcl_el_int] = shuffle(
                    list_of_class_lists[vcl_el_int])
        
        #Performance of one full k-fold test.
        result_dict = oneagainstrestkfoldtest(n_folds,list_of_class_lists,c,gamma,c_ratio,)

        #Store performaces
        overall_shuffle_dict_list.append(result_dict)
    
    #Sum the dictionary elements.
    for perf_dict_el in overall_shuffle_dict_list:
        for avg_key_el in average_perf_dict:
            average_perf_dict[avg_key_el]+=perf_dict_el[avg_key_el]
    
    #Divide dict elements by length to average. 
    for avg_key_el in average_perf_dict:
        average_perf_dict[avg_key_el] = average_perf_dict[avg_key_el]/len(overall_shuffle_dict_list)
    
    return average_perf_dict
        

def makepysvmlightvectorlist(file_name,input_file_format):
    for example_vector in open(pos_file_name,"r"):#base_file_name+"pos.vec"
        if input_file_format == "SVMLIGHT":
            pos_ex_cnt+=1
            tmp_list = []
            for el in pos_ex.split()[1:]:
                el1,el2 = el.strip().split(":")
                tmp_list.append( (int(el1),float(el2)) )
            positive_examples.append( (1,tmp_list) )
        else:
            print("ERROR")


#=============================================================================
#                                Main Program
#=============================================================================

file_name_glob,n_folds,x_shuffles,input_file_format = getargs()

pos_ex_cnt = 0
neg_ex_cnt = 0
best_vals = None
best_mcc  = None
c_start,c_end,c_parts = 1,700,25
j_start,j_end,g_parts = 1,20,3
g_start,g_end,g_parts = 1,700,25
svm_kernal = "rbf"

for c_val in range(c_start,c_end,c_parts):
    for gamma_val in range(j_start,j_end,g_parts):
        for c_ratio_val in range(g_start,g_end,g_parts):

            best_average_mcc = None
            best_class_str   = ""

            shuffledaveragedkfoldtest(
            c=c_val,
            gamma=gamma_val,
            c_ratio=c_ratio_val,
            x_shuffles=x_shuffles,
            n_folds=n_folds)

    if best_average_mcc == None or best_average_mcc < average_perf_dict["mcc"]:
        #Calculate performaces averages mean and varience,etc, of performance statistics
        best_class_str=("kernal: "+str(svm_kernal)+"\t"+ "c: "+str(c_val)+"\t"+"gamma: "
             +str(gamma_val)+"\t"+"costratio: "+str(c_ratio_val)+"\t")
        for e in sorted( average_perf_dict.keys() ):
            best_class_str =  best_class_str+ e+": "+str(average_perf_dict[e])+"\t"
        print("shuffled_average:\t"+best_class_str)




