from random import shuffle
from math import sqrt
import svmlight#https://bitbucket.org/wcauchois/pysvmlight
from itertools import izip, chain, repeat
import argparse

parser = argparse.ArgumentParser(description='Do training.')
parser.add_argument('--positive_training_vecs', 
                    #metavar='', 
                    type=str, 
                    #nargs='1',
                    help='')
parser.add_argument('--negative_training_vecs', 
                    #metavar='', 
                    type=str, 
                    #nargs='1',
                    help='')

parser.add_argument('--unknown_vecs', 
                    #metavar='', 
                    type=str, 
                    #nargs='1',
                    help='')

args = parser.parse_args()

pos_file_name = args.positive_training_vecs
neg_file_name = args.negative_training_vecs
unknown_vec_file_name = args.unknown_vecs

#pos_file_name = "specific_laccase_positive_set_5-20.faa.pruneBJXZ.fasta.DIPEP.SVM_LIGHT.vec"
#neg_file_name = "specific_laccase_negative_set_5-20.faa.pruneBJXZ.fasta.DIPEP.SVM_LIGHT.vec"
#unknown_vec_file_name = "ab_initio_switchgrass_protein_preds.faa.pruneBJXZ.fasta.greaterthan61chars.faa.DIPEP.SVM_LIGHT.vec"


#For each file there should be a pos and neg file 
#Or use other files as neg files. 
# Pos Vec Files 

# Neg Vec Files 

#base_file_list     = ["/scratch/tweiric/specific_laccase_*_5-20.faa.pruneBJXZ.fasta.DIPEP.SVM_LIGHT.vec."]
#["/home/tweiric/pysvmlight_test.AACOMP"]

#pos_file_name = "specific_laccase_positive_set_5-20.faa.pruneBJXZ.fasta.DIPEP.SVM_LIGHT.vec"
#neg_file_name = "specific_laccase_negative_set_5-20.faa.pruneBJXZ.fasta.DIPEP.SVM_LIGHT.vec"
#unknown_vec_file_name = "ab_initio_switchgrass_protein_preds.faa.pruneBJXZ.fasta.greaterthan61chars.faa.DIPEP.SVM_LIGHT.vec"

number_of_shuffles = 1
n_folds            = 5
randomize          = False
input_format = "SVMLIGHT"
#TABDELIM, get from vector making program. 

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
        '{number:.{digits}f} '.format(number=(self.getaccuracy()),digits=2)+"\t"+
        '{number:.{digits}f} '.format(number=(self.geterror()),digits=2)+"\t"+
        '{number:.{digits}f} '.format(number=(self.getMCC()),digits=5)+"\t"+
        '{number:.{digits}f} '.format(number=(self.getprecision()),digits=2)+"\t"+
        '{number:.{digits}f} '.format(number=(self.getsensitivity()),digits=2)+"\t"+
        '{number:.{digits}f} '.format(number=(self.getspecificity()),digits=2)
         )

        return rtrn_str
    
    def gettitle(self):
        
        rtrn_str = (
        'accuracy   \t'+
        'error      \t'+
        'MCC        \t'+
        'precision  \t'+
        'sensitivity\t'+
        'specificity'
        )
        
        return rtrn_str
    
    
    

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


pos_ex_cnt = 0
neg_ex_cnt = 0



#for base_file_name in base_file_list:    
positive_examples = []
for pos_ex in open(pos_file_name,"r"):#base_file_name+"pos.vec"
    if "SVMLIGHT":
        pos_ex_cnt+=1
        tmp_list = []
        for el in pos_ex.split()[1:]:
            el1,el2 = el.strip().split(":")
            tmp_list.append( (int(el1),float(el2)) )
        positive_examples.append( (1,tmp_list) )
    else:
        print("ERROR")
        
negative_examples = []
for neg_ex in open(neg_file_name,"r"):#base_file_name+"neg.vec"
    neg_ex_cnt+=1
    if "SVMLIGHT":
        tmp_list = []
        for el in neg_ex.split()[1:]:
            el1,el2 = el.strip().split(":")
            tmp_list.append( (int(el1),float(el2)) )
        negative_examples.append( (-1,tmp_list) )
    else:
        print("ERROR")
             


FP = 0
FN = 0
TN = 0
TP = 0

best_vals = None
best_mcc  = None

result_dict = {"FP":0,"FN":0,"TN":0,"TP":0}

c_start,c_end,c_parts = 1,700,400
j_start,j_end,g_parts = 1,20,15
g_start,g_end,g_parts = 1,700,200


#print(c,g,j+"\t"+performace_calcs.gettitle())

for c_val in range(c_start,c_end,c_parts):
    for gamma_val in range(j_start,j_end,g_parts):
        for c_ratio_val in range(g_start,g_end,g_parts):

            for i in range(0,number_of_shuffles):
                
                if randomize:
                    shuffle(positive_examples)
                    shuffle(negative_examples)
                #Split into n parts
                n_pos_examples = splitter(n_folds,positive_examples)
                n_neg_examples = splitter(n_folds,negative_examples)
            
                for fold_level in range(0,n_folds):
                    #Make a model.
                    training_data    = []
                    testing_data     = []
                    pos_testing_data = []
                    neg_testing_data = []
                    
                    for i in range(0,n_folds):
                        if fold_level != i:    
                            #print( len(n_pos_examples) )
                            training_data = training_data + n_pos_examples[i] 
                            training_data = training_data + n_neg_examples[i]
                        else:
                            pos_testing_data = pos_testing_data + n_pos_examples[i]
                            neg_testing_data = neg_testing_data + n_neg_examples[i]      
                    
                    fold_model  = svmlight.learn(
                        training_data,
                        #Options 
                        type='classification',
                        kernel="rbf",
                        C=c_val,
                        rbf_gamma=gamma_val,
                        costratio=c_ratio_val
                    )
                    
            
                    #Test the model.
            
                    predictions = svmlight.classify(fold_model,pos_testing_data) 
                    for e in predictions:
                        #print(e)
                        if e >= 0:
                            result_dict["TP"]+=1
                        else:
                            result_dict["FN"]+=1
            
                    predictions = svmlight.classify(fold_model,neg_testing_data)     
                    for e in predictions:
                        #print(e)
                        if e >= 0:
                            #False Positive
                            result_dict["FP"]+=1
                        else:
                            result_dict["TN"]+=1
            
            
            
            performace_calcs = PerformanceCalculation(FN=result_dict["FN"],
                                                      FP=result_dict["FP"],
                                                      TN=result_dict["TN"],
                                                      TP=result_dict["TP"])
                    
            #print("TP",result_dict["TP"])
            #print("TN",result_dict["TN"])
            #print("FN",result_dict["FN"])
            #print("FP",result_dict["FP"])
            
            #print(c,g,j+"\t"+performace_calcs.gettitle())
            if best_mcc == None or performace_calcs.getMCC() > best_mcc: 
                best_vals = str(c_val)+","+str(gamma_val)+","+str(c_ratio_val)+"\t"+performace_calcs.getperformance()
                best_mcc  = performace_calcs.getMCC()
            
            
            print(str(c_val)+","+str(gamma_val)+","+str(c_ratio_val)+"\t"+performace_calcs.getperformance())

print()
print(best_vals)
