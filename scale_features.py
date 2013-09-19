"""
@author: Tyler Weirick
@date: 2013-08-18
==============================================================================
This program takes sets of vectors pertaining to classes and finds a subset 
of features better correlated to classification. It will output the findings 
as a file with the element descriptions sepatated by spaces. The input 
vectors need to be in description:value format.
==============================================================================

python scale_features.py --comma_delimited_vec_file_names "../data/LO1_proteinlevel.faa.on.trembl.psiblastout.acflat.faa.pruneBJXZ.fasta.AACOMP-DIPEP-SPLITAA-PLPredPhysChem22_nolog.EL_DESC_VAL.vec,../data/4CL_proteinlevel.faa.on.trembl.psiblastout.acflat.faa.pruneBJXZ.fasta.AACOMP-DIPEP-SPLITAA-PLPredPhysChem22_nolog.EL_DESC_VAL.vec" --out_file_name test_red.txt
"""

from sklearn.svm import SVC
from sklearn.datasets import load_digits
from sklearn.feature_selection import RFE
from sklearn.feature_selection import SelectKBest, f_regression, f_classif
from sklearn.cluster import KMeans
from sklearn import datasets
import numpy as np
import pylab as pl
import argparse 

def unique(a):
    order = np.lexsort(a.T)
    a = a[order]
    diff = np.diff(a, axis=0)
    ui = np.ones(len(a), 'bool')
    ui[1:] = (diff != 0).any(axis=1) 
    return a[ui]

#=============================================================================
#                               Classes
#=============================================================================

class clusterset():
    '''Used for storing and interpreting feature scaling. 
    '''
    def __init__(self):
        self.data       = []
        self.true_preds = []
        self.el_titles  = []

    def makefeaturereductionarray(self,class_file_list):
        '''
        Vectorize a set of classes. This creates two lists, the first 
        containing a 2D array of values obtained from the input vectors
        the second vector contains one entry for each row in the 2D 
        vector which corresponds to the class it belongs to.
        output: 
        self.data = np.array([ [0.93423,0.25662,...]...])
        self.true_preds = np.array([ 0,0,...1,1,...])
        '''
        out_vecs   = []
        tpred_list = []
        first_round = True 
        class_number = 0
        line_dict = {}

        for file_name in class_file_list:
            for line in open(file_name,'r'):
                tmp_vals = []
                #For a vec line get all values and store as an list
                for vec_el in line.strip().split():
                    el_title,el_val = vec_el.split(":")
                    if first_round:  self.el_titles.append(el_title)        
                    tmp_vals.append(float(el_val))
                #Add the row to another list. 
                out_vecs.append( tmp_vals )
                #For each row there must be a corresponding class number. 
                tpred_list.append(class_number)
            #Increment to indicate a new class. 
            class_number+=1
        self.data       = np.array(out_vecs).astype(np.float32)
        self.true_preds = np.array(tpred_list).astype(np.float32)    


#=============================================================================
#                               Functions
#=============================================================================

def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--vec_file_glob',
                       help='''Should be in EL_DESC_VAL format.''',
                       default=None)

    parser.add_argument('--comma_delimited_vec_file_names',
                       help='''Should be in EL_DESC_VAL format, 
                       takes presidence over vec_file_set if given.''',
                       default=None)

    parser.add_argument('--out_file_name',
                       help='''Should be in EL_DESC_VAL format, 
                       takes presidence over vec_file_set if given.''',
                       default=None)

    args = parser.parse_args()
    out_file_name = args.out_file_name
    vec_file_glob = args.vec_file_glob
    comma_delimited_vec_file_names = args.comma_delimited_vec_file_names

    if vec_file_glob != None: 
        file_name_set =  glob(vec_file_glob)

    if comma_delimited_vec_file_names != None:
        file_name_set = comma_delimited_vec_file_names.split(",")

    return file_name_set,out_file_name


#=============================================================================
#                               Main Program
#=============================================================================

file_name_glob,out_file_name = getargs()

#Make a cluster class
c = clusterset()
#Add generate vectors in the class. 
c.makefeaturereductionarray(file_name_glob)

#Generate and array of boolean values, the T|F values depend on wether the 
#standard deviation of a given column is zero, indicating a column of all 
#the same values. This can cause errors durring the anova_filter fitting. 
bool_arr = (np.std(c.data, axis=0) == 0)
for i in range(len(bool_arr)-1,0,-1):
   if bool_arr[i]:
       #Remove the column from the data
       c.data = np.delete(c.data,i,1)
       #Also remove the column title from the element titles list. 
       #Important as equivalents is determined by order. 
       c.el_titles.pop(i)

#Can also use chi2, f_classif, or f_regression.
anova_filter = SelectKBest(f_classif, k='all')
z = anova_filter.fit(c.data,c.true_preds)

#Calculate stats for the run.  
score_array = z.scores_
f_score_average = np.mean(score_array)
f_score_25th    = np.percentile(score_array,25)
f_score_75th    = np.percentile(score_array,75.0)
f_score_90th    = np.percentile(score_array,90.0)
mean            = np.mean(score_array)
median          = np.median(score_array)
min_val         = np.amin(score_array)
max_val         = np.amax(score_array)
std_dev         = np.std(score_array)

#Get data for desired conditions. 
score_above_mean_dict = {}
score_above_75th_dict = {}
score_above_90th_dict = {}
for i in z.get_support(indices=True):
    if z.scores_[i] > f_score_average:
        score_above_mean_dict.update({c.el_titles[i]:z.scores_[i]})
    if z.scores_[i] > f_score_75th:
        score_above_75th_dict.update({c.el_titles[i]:z.scores_[i]})
    if z.scores_[i] > f_score_90th:
        score_above_90th_dict.update({c.el_titles[i]:z.scores_[i]})

#Output the 
out_list = []
for e in sorted(score_above_mean_dict, key=score_above_mean_dict.get):
    out_list.append(e)
out_file = open(out_file_name+".reducedtomean.vec",'w')
out_file.write(" ".join(out_list))
out_file.close()
out_list = []
for e in sorted(score_above_75th_dict, key=score_above_75th_dict.get):
    out_list.append(e)
out_file = open(out_file_name+".reducedto75th.vec",'w')
out_file.write(" ".join(out_list))
out_file.close()
out_list = []
for e in sorted(score_above_90th_dict, key=score_above_90th_dict.get):
    out_list.append(e)
out_file = open(out_file_name+".reducedto90th.vec",'w')
out_file.write(" ".join(out_list))
out_file.close()


out_list = []
out_list.append("Total number of elements: "        +str(len(out_list)))
out_list.append("Elements above average: "+str(len(score_above_mean_dict)))
out_list.append("Elements above 75th percentile: "+str(len(score_above_mean_dict)))
out_list.append("Elements above 90th percentile: "+str(len(score_above_mean_dict)))
out_list.append("MIN"+str(min_val))
out_list.append("25th_PER"+str(f_score_25th))
out_list.append("MEAN"+str(mean))
out_list.append("MEDIAN"+str(median))
out_list.append("75th_PER"+str(f_score_75th))
out_list.append("MAX"+str(max_val))
out_list.append("STANDARD_DEV"+str(std_dev))
#out_list.append(" ".join(out_list))
out_file = open(out_file_name+".reduced.vec.log",'w')
out_file.write("\n".join(out_list))
out_file.close()

#Output full list of weights 
#Output elements over threshold as .vecids