'''
@author: Tyler Weirick
@date: 2013-08-16
'''
import numpy as np
import pylab as pl
from sklearn.cluster import KMeans
from sklearn import datasets
import argparse

number_of_clusters = 2
cluster_names = []
for i in range(number_of_clusters):
    cluster_names.append(str(i))

parser = argparse.ArgumentParser()
parser.add_argument('--true_positives',help='''a ''',required=True)
parser.add_argument('--true_negatives',help='''b ''',required=True)
parser.add_argument('--unknowns',help='''c ''',required=True)

args = parser.parse_args()
true_positives_file = args.true_positives
true_negatives_file = args.true_negatives
unknown_file        = args.unknowns



"""
vec_type = "Geary"
positive_examples_file = "/scratch/tweiric/LigPred_0.3/data/2013-08-22_vecs_from_initial_data_set/4CL_transcriptlevel.faa.pruneBJXZ.fasta.greaterthan61chars.faa.fsp.fasta."+vec_type+".EL_DESC_VAL.vec"
negative_examples_file = "/scratch/tweiric/LigPred_0.3/data/2013-08-22_spnegset_cleaned_combined_faa/4CL.combined_negset.faa."+vec_type+".EL_DESC_VAL.vec"
unknown_examples_file  = "/scratch/tweiric/LigPred_0.3/data/2013-08-22_vecs_from_TrEMBL_psiblast/4CL_proteinlevel.faa.on.trembl.psiblastout.acflat.faa.pruneBJXZ.fasta.greaterthan61chars.faa.fsp.fasta."+vec_type+".EL_DESC_VAL.vec"
"""

# regex of knows seqs to generate clusters. 
known_vec_files  = []
# File of unknowns to cluster onto clusters. 
unknown_vec_file = ""
# output a file for each file entered. with new seqs 


class ClassificationVectors():

    def __init__(self,vec_file_glob_list):
        vecs_tmp_list       = []
        int_lables_tmp_list = []
        vec_ids_tmp         = []
        label_cnt = 0
        for file_name in vec_file_glob_list:
            
            for line in open(file_name,'r'):
                sp_line = line.strip().split()
                vec_name = sp_line[0]                    
                vec_ids_tmp.append(vec_name)
                el_tmp_list = []
                for vec_el in sp_line[1:]:
                    el_tmp_list.append( float(vec_el.split(":")[-1])  )
                vecs_tmp_list.append( el_tmp_list  )    
                int_lables_tmp_list.append(label_cnt) 
            label_cnt+=1            
        #The vectors 
        self.data        = np.array(vecs_tmp_list).astype(np.float32)
        #The integer assignments of the classes 
        self.labels      = int_lables_tmp_list
        #
        self.class_cnt   = label_cnt
        #The Accesison Numbers of the sequence used to genreate the vector. 
        self.vec_id_list = vec_ids_tmp

true_positives_file = args.true_positives
true_negatives_file = args.true_negatives
unknown_file        = args.unknowns

vec_file_glob_list = [true_positives_file,true_negatives_file,unknown_file]
#Gereate ClassificationVectors Class 
known_vecs = ClassificationVectors(vec_file_glob_list)

kmeans = KMeans(init='random', n_clusters=number_of_clusters, n_init=2,max_iter=1000)
clusters = kmeans.fit(known_vecs.data)

file_dict = {}
unknown_ids = {}
for i in range(0,len(clusters.labels_)):   
    seq_from_file = str(known_vecs.labels[i])
    cluster_assng = str(clusters.labels_[i]) 
    seq_id        = known_vecs.vec_id_list[i]
    if str(seq_from_file) in file_dict:
        if cluster_assng in file_dict[seq_from_file]:    
            file_dict[seq_from_file][cluster_assng].append(seq_id)   
            #if known_vecs: unknown_ids
        else:
           file_dict[seq_from_file].update({cluster_assng:[seq_id]})
           #if known_vecs: unknown_ids.update({cluster_assng:[seq_id]})
    else:
        file_dict.update({seq_from_file:{cluster_assng:[seq_id]}})


out_list = []
for e in sorted(file_dict.keys()):   
    col_list = [ vec_file_glob_list[int(e)] ]
    tmp_numbs = []
    title_col = ["data_set"]
    for cluster_num in cluster_names:
        if cluster_num in file_dict[e]:
            title_col.append(str(cluster_num))
            tmp_numbs.append( file_dict[e][cluster_num])
            col_list.append(  str( len( file_dict[e][cluster_num]) ) )
        else: 
            col_list.append( "0"  )
            tmp_numbs.append(0)
        
        if vec_file_glob_list[int(e)] == unknown_file :
            try:
                file = open(unknown_file+".cluster"+str(cluster_num)+'.ids.txt','w')
                file.write("\n".join(file_dict[e][cluster_num]))
                file.close()
            except:
                print("Error: printing file.")
    out_list.append(  "\t".join(col_list)  )
        
log_txt  = "\t".join(title_col) +'\n' +"\n".join(out_list)
print( log_txt ) 

