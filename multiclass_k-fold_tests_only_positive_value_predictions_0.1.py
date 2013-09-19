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
import argparse
import svmlight
from sys import exit     #from sys import exit from sys import exit
from glob import glob    #from glob import glob
import os                #import os
import subprocess        #import subprocess
from time import time    #from time import time
from math import *       #from math import *
import tempfile          #import tempfile
from random import gauss #from random import gauss
from time import asctime
from time import sleep

class FeaturePoint():
    """
    This class describes a point generated by some type of feature(s).
    It holds a string describing the point as well as the name of the 
    class the point is from and can return the point as a positive 
    negative or named point. 
    """
    def __init__(self,feature_line):
        assert type(feature_line) == str
        split_line = feature_line.split()
        #Make sure that a name exists.
        #@todo: make a regex to recognize proper svm format.
        #print(split_line)
        assert not ":" in split_line[0],"ERROR: Point done not have name"+split_line  
       
        self.example_type       = split_line[0]
        self.true_class_name    = split_line[0]
        self.vector_coordiantes = " ".join(split_line[1:])
        self.predicted_class    = None
        self.value_of_pred      = None
        self.class_value_dict = {}
    
    def printdict(self):
        out_dict_str = []
        for e in sorted(list(self.class_value_dict)):
            out_dict_str.append(self.class_value_dict[e])
        return " ".join(out_dict_str)
        
    def getPositivepoint(self):
        return "+1 "+self.vector_coordiantes
    def getNegativepoint(self):
        return "-1 "+self.vector_coordiantes
    def getZeroPoint(self):
        return "0 "+self.vector_coordiantes
    def getnamedpoint(self):
        return self.example_type+" "+self.vector_coordiantes
        
    def updateprediction(self,class_name,value):
        assert type(class_name) == str
        assert type(value)      == float 
        if (self.predicted_class == None and self.value_of_pred == None):
            self.predicted_class   = class_name
            self.value_of_pred     = value 
        elif value > self.value_of_pred:  
            self.predicted_class   = class_name
            self.value_of_pred     = value 
               
#elif value == self.value_of_pred:
#    ewrwe=0
#    #print("WARNING: values for",self.predicted_class,self.true_class_name,
#    #"and",class_name,"are equal. It could be likely your",
#    #"classes have repeats or overlapping sequences.")
           
           
           
    def checkprediction(self,checking_class):
        '''
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
        '''
        if self.value_of_pred >= 0:
            if checking_class == self.true_class_name:
                if checking_class == self.predicted_class:
                    return "TP"
                else:#if self.predicted_class != self.true_class_name:
                    return "FN"
            else:#hecking_class != self.true_class_name:
                if checking_class == self.predicted_class:
                    return "FP"
                else:#if self.predicted_class != self.true_class_name:
                    return "TN"
        else:
            return "FN"
            

class ClassificationSet():
    """
    This class represents one class within the classification system.
    """
    def __init__(self,class_name,k):
        self.class_name = class_name
        self.FeaturePoint_class_list = []
        self.k = k
        self.remainder      = 0
        self.stop_point_list = []
        self.average_length = 0
    
    def resetRemainder(self):
        self.remainder = self.static_remainder
        
    def addclasspointlist(self,class_points_list):
        #This should be a complete list of all members of a class.
        #assert type(class_points_list) == list, class_points_list
        #print("Remainder",len(class_points_list)%self.k)
        self.static_remainder = len(class_points_list)%self.k
        self.average_length = int(len(class_points_list)/self.k)
        self.FeaturePoint_class_list = class_points_list
        self.remainder = len(class_points_list)%self.k
        stoppnt=0
        for sp_i in range(0,self.k):
            
            if sp_i <= self.remainder:
                stoppnt+=self.average_length+1
            elif sp_i == self.k:
                stoppnt = len(class_points_list)
            else:
                stoppnt+=self.average_length
            #print(stoppnt)
            self.stop_point_list.append(stoppnt)
            

   

    def getsubset(self,i,max_k_val):
        """
        Returns a subset 1/k of the total FeaturePoints in the FeaturePoint 
        class list. 
        """
        
        if i == 0:
            start = 0
        else:
            start = self.stop_point_list[i-1]
        stop = self.stop_point_list[i]
        #start = i*self.average_length
        #stop  = start+self.average_length
        #print(i,"starstop",start,stop,stop-start)
        #if self.remainder > 0:
        #    #print(len(self.FeaturePoint_class_list),end=" ")
        #    stop+=1
        #    self.remainder-=1
        #    #print("!!!!!!!!!!!!!!!!!!1")
        rtn = self.FeaturePoint_class_list[start:stop]
        out_list = []
        for e in self.FeaturePoint_class_list[start:stop]:
            out_list.append(e.getnamedpoint())

        return rtn,out_list
    


class SVMLearnClass():
    def __init__(self,class_name,pos_neg_examples_str,test_examples):
        self.pos_examples_are_class = class_name
        self.pos_neg_list  = pos_neg_examples_str
        self.test_examples = test_examples_str
        
class KFoldSet():
    def __init__(self):
        self.general_example_data = []
        self.test_data            = []

class TrainingFile():
    def __init__(self,pcn,tt):
        self.protein_class_name = ""
        self.training_text = ""
        
class Predictions():    
    def __init__(self):
        self.test_file_2D_list = []     

class PlusMinusFile():
    def __init__(self,psn,training_data):
        self.pos_set_name  = psn
        self.training_data = training_data
        #self.test_file     = test_file ,test_fil

#Should be K of these
class KFold():    
    def __init__(self,pmdl,tf,cd):
        self.plus_minus_data_list = pmdl
        assert type(tf) == str
        self.test_file = tf
        self.calc_data = cd



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
        return sorted(glob(args.file_set)),int(args.k)
except:
    try:
        import optparse
    except:
        print("ERROR 1: Cannot import argparse or optparse")


def dofoldclassification(c_cond,j_cond,g_cond,training_data,test_str):
    #Make the training file. 
    training_file = tempfile.NamedTemporaryFile(mode='w')  
    training_file.write(training_data)
    training_file.flush()
    #Make the model data into this file.
    model_file = tempfile.NamedTemporaryFile(mode='r')
    #print(training_data)
    #Run SVM learn svm_learn    example1/train.dat example1/model        
    #subprocess.call("free -m",shell=True)# 

    subprocess.call("svm_learn -z c -t 2 "+
     " -c "+str(c_cond)+" -j "+str(j_cond)+" -g "+str(g_cond)+
     " "+training_file.name+" "+model_file.name,
     shell=True,stdout=open(os.devnull, 'w'))# 
    
    #print(model_file.readlines())
    
    #Training data is no longer needed as we now have a model file. Will be deleted on close.
    sleep(1)
    training_file.close()
    
    test_file = tempfile.NamedTemporaryFile(mode='w')
    test_file.write(test_str)
    test_file.flush()
    
    #print(test_file.readlines())
    
    predictions_file = tempfile.NamedTemporaryFile(mode='r')
    #svm_classify example1/test.dat example1/model example1/predictions
    subprocess.call("./svm_classify "+test_file.name+" "+model_file.name+" "+predictions_file.name,shell=True,stdout=open(os.devnull, 'w'))
    
    test_file.close()
    model_file.close()#Model file no longer needed as we have predictions. 
    #print(predictions_file.readlines())
    return predictions_file





def get_feature_classificationset_list_and_input_class_name_list(file_glob,k):
    class_name_collision_check_list = []
    feature_ClassificationSet_list  = []

    for featurized_file_with_ID in file_glob:
         #Get class name.
         class_name = featurized_file_with_ID.split("/")[-1].split(".")[0]
         print(class_name)
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
        #print(type(e))
        comb = e.true_class_name.upper()+" "+e.predicted_class.upper()
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
            if class1.upper()+" "+class2.upper() in confusion_matrix:
                numb_str = str(confusion_matrix[class1.upper()+" "+class2.upper()])
            else:
                numb_str = "0"    
            #other_stuff.append(class1+"-"+class2+":"+numb_str)
            other_stuff.append(numb_str)
        rows.append(" ".join(other_stuff))
    
    return(" ".join(horizontal_title) +"\n"+"\n".join(rows))
    
    

def calculateOverallMCC(results_list,class_name_collision_check_list):
    #results_list calc_class -> [FeaturePoint(),..]
    #print(results_list,class_name_collision_check_list)
    #Calculate Statistics need per class stats as well as overall.
    total_seqs = 0
    numerator = 0
    MCC_numerator         = 0
    accuracy_numerator    = 0
    precision_numerator   = 0
    sensitivity_numerator = 0
    specificity_numerator = 0
    error_numerator       = 0
    total_FN = 0
    total_FP = 0
    total_TN = 0
    total_TP = 0
    for class_name in class_name_collision_check_list:
        number_of_seqs_per_class = 0
        osd = {"TP":0,"TN":0,"FP":0,"FN":0}
        for e in results_list:
            #print(e,e.true_class_name.upper(),class_name.upper())
            if e.true_class_name.upper() == class_name.upper():
                number_of_seqs_per_class+=1     
            osd[e.checkprediction(class_name)]+=1    
        pc = PerformanceCalculation(osd["FN"],osd["FP"],osd["TN"],osd["TP"])
        
        print(osd["FN"],osd["FP"],osd["TN"],osd["TP"],number_of_seqs_per_class)
        total_seqs+=number_of_seqs_per_class
      
        MCC_numerator         += number_of_seqs_per_class*pc.getMCC()
        accuracy_numerator    += number_of_seqs_per_class*pc.getaccuracy()  
        precision_numerator   += number_of_seqs_per_class*pc.getprecision()
        sensitivity_numerator += number_of_seqs_per_class*pc.getsensitivity()
        specificity_numerator += number_of_seqs_per_class*pc.getspecificity()
        error_numerator       += number_of_seqs_per_class*pc.geterror()
        total_FN += osd["FN"]
        total_FP += osd["FP"]
        total_TN += osd["TN"]
        total_TP += osd["TP"]
        print(osd["FN"],osd["FP"],osd["TN"],osd["TP"],class_name.upper(),pc.getMCC(),number_of_seqs_per_class)

    out_cals = {
    "mcc":MCC_numerator/total_seqs,        
    "accuracy":accuracy_numerator/total_seqs,    
    "precision":precision_numerator/total_seqs,  
    "sensitivity":sensitivity_numerator/total_seqs, 
    "specificity":specificity_numerator/total_seqs, 
    "error":error_numerator/total_seqs,      
    "FN":total_FN,
    "FP":total_FP,
    "TN":total_TN, 
    "TP":total_TP,
    "total_seqs":total_seqs
    }
    
    return out_cals
    
    



    
     

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

    if sorted(sigma2,reverse=True)[0] > epsilon:#t < maxits and maxits = 100oko
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
     #print(out_point_list)  
     return out_point_list




#=============================================================================
#                             Varibles
#=============================================================================
DEBUG = True    
c_start,c_end = 0.1,500
j_start,j_end = 1,15
g_start,g_end = 1,500
max_mcc = 0.0
parts = 4


#Make a list containing k elements containing ~ k-1/k of the total data.
k_fold_learning_set     = []
k_fold_list             = []
k_level_plus_minus_list = []

#=============================================================================
#                             Main Program
#=============================================================================

#Get command line arguments. 
parser = argparse.ArgumentParser(description=getheadcomments())    
parser.add_argument('--file_set',help='')
parser.add_argument('--k' ,default=5,help='')
parser.add_argument('--allways_negative_fasta' ,default=5,help='')
args = parser.parse_args()
print(args.file_set)
sorted_file_glob = sorted(glob(args.file_set))
print(sorted_file_glob)
out_base_name = args.file_set.replace("*","")+"_"+str(int(time()))
k = int(args.k)

#Generate two lists, one of ClassificationSet Objects and another a list of 
#the class names. 
class_name_collision_check_list = []
feature_ClassificationSet_list  = []
for featurized_file_with_ID in sorted_file_glob:
     #Get class name.
     class_name = featurized_file_with_ID.split("/")[-1].split(".")[0]
     feature_ClassificationSet = ClassificationSet(class_name,k)
     
     if class_name in class_name_collision_check_list:
          print("ERROR Overlapping class names found:",class_name)
          exit()
     class_name_collision_check_list.append(class_name)
     
     #Add the data points in the file to ClassificationSet
     example_list = []
     for line in open(featurized_file_with_ID,"r"):
        #print([line])
        line = line.strip() 
        if line != "":
            example_list.append(FeaturePoint(line))
        else:
            print(featurized_file_with_ID)

     feature_ClassificationSet.addclasspointlist(example_list)
     #This list contains all ClassificationSet objects.
     #These should all contain the same training IDs.
     feature_ClassificationSet_list.append(feature_ClassificationSet)
     print(feature_ClassificationSet.class_name,len(feature_ClassificationSet.FeaturePoint_class_list))
         
assert len(class_name_collision_check_list) == len(feature_ClassificationSet_list)
assert len(sorted_file_glob) == len(feature_ClassificationSet_list)


parts = 9
c_parts = 7
g_parts = 10
j_parts = 4
out_point_list = []
overall_MCC_list = []
c_increment = (c_end-c_start)/c_parts
j_increment = (j_end-j_start)/j_parts
g_increment = (g_end-g_start)/g_parts

for g_int in range(1,g_parts+1):
    g = g_int*g_increment
    if g == 0: g=0.1
    for c_int in range(0,c_parts+1):
        c = c_int*c_increment
        if c == 0:c=0.1
        for j_int in range(0,j_parts+1):
            j = j_int*j_increment
            if j == 0: j =0.1
            print("WARNING")

            c_cond,j_cond,g_cond = c,j,g
                        
            for classifer in feature_ClassificationSet_list:
                classifer.resetRemainder()
            
            print("Classify with variables",c_cond,j_cond,g_cond)   
            results_list = [] 
            tmp_print = []
            for fold_x in range(0,k):
                    k_level = fold_x
                    print("fold_x",fold_x,time())
                    #for k_level in range(0,k):
                    #print("k_level",k_level,time())

                    training_data = []
                    test_data            = []
                    calc_data            = []
                    
                    tmp_set,tmp_txt_list = [],[]
                    tempcnt4cl=0
                    for fold_member in range(0,k):
                        if k_level == fold_member:
                            for classifer in feature_ClassificationSet_list:
                                
                                #Make a list of FeaturePoint Classes 
                                #test_data.append(classifer.gettextsubset(k_level))
                                # = classifer.gettextsubset(k_level)
                                nn,mm = classifer.getsubset(k_level,k-1)
                                test_data = test_data + mm
                                calc_data = calc_data + nn
                                test_data,calc_data


                        else:
                            #Get level k for each protein class.  
                            tb=True
                            for classifer in feature_ClassificationSet_list:
                                
                                tmp_set,tmp_txt_list = classifer.getsubset(k_level,k-1)
                                #if classifer == feature_ClassificationSet_list[1]:
                                #    print(len(tmp_txt_list))                                
                                training_data = training_data + tmp_set

                                #if classifer.class_name == "4CL":
                                #    tempcnt4cl+=len(tmp_set)
                                #    print(classifer.class_name,tempcnt4cl,len(tmp_set),classifer.remainder)

                            
                    test_str = "\n".join(test_data)
    
                    plus_minus_data_list = []
                    for class_name in class_name_collision_check_list:
                        #for n class_types make plus negative files.
                        #Will need to make one for every class. 
                        ex = []
                        for example in training_data:
                            if example.example_type == class_name:
                                ex.append(example.getPositivepoint())
                            else:
                                ex.append(example.getNegativepoint())
                            
                        plus_minus_class = PlusMinusFile(class_name,"\n".join(ex))
                        print("Start Classification.",class_name,"c",c_cond,"j",j_cond,"g",g_cond,"time",time())
                        predictions_file = dofoldclassification(c_cond,j_cond,g_cond,plus_minus_class.training_data,test_str)
                        #predictions_file = dofoldclassificationPOLY(c_cond,j_cond,g_cond,plus_minus_class.training_data,test_str)
                        print("Classification Complete.",time())
                        i = 0
                        
                        for line in open(predictions_file.name,'r'):
                            calc_data[i].updateprediction(plus_minus_class.pos_set_name,float(line.strip()))
                            calc_data[i].class_value_dict.update({class_name:line.strip()})
                            
                            i+=1
                        predictions_file.close()
                    results_list = results_list + calc_data

                                        
            #for fff in results_list:
            #    print(fff.true_class_name+" "+fff.predicted_class+" "+fff.printdict())
            #exit()
            
            assert test_str.count('\n')+1 == len(calc_data),calc_data
            #Make temporary file to hold testing data. 
            
            #print("Classification Complete")
            performance_dict = calculateOverallMCC(results_list,class_name_collision_check_list)
                        
            #overall_MCC_list.append([overall_MCC,point])
            if max_mcc < performance_dict["mcc"]:
                #Set new max MCC.
                max_mcc = performance_dict["mcc"]
    
                #Write detailed stats to a file
                #Vector Type
                #Time
                #Conditions
                out_list = [asctime(),"c="+str(c_cond)+" j="+str(j_cond)+" g="+str(g_cond)+
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
                
                file = open("training_best_stats"+out_base_name+".posvalonly.txt",'w')
                file.write("\n".join(out_list))
                file.close()
                #Vector Type
                #Time
                #Conditions
                file = open("best_stats_confusion_matrix"+out_base_name+".posvalonly.txt",'w')
                file.write(makeconfusionmatrix(results_list,class_name_collision_check_list))
                file.close()
            #append run history to logfile. 
            #Time conditions MCC
            file = open("training_history"+out_base_name+".txt",'a')
            out_list = [asctime(),"c="+str(c_cond)+" j="+str(j_cond)+" g="+str(g_cond)+
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
                        
            print(",".join(out_list))
            file.write(",".join(out_list))
            file.close()
            #point_list = optimize_c_j_g_with_NCE(overall_MCC_list,[[c_start,c_end],[j_start,j_end],[g_start,g_end]])
            #point_list = False
            #exit()
            

