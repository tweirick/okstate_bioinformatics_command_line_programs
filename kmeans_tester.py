'''
@author: Tyler Weirick
@date: 2013-08-16
'''
import numpy as np
import pylab as pl
from sklearn.cluster import KMeans
from sklearn import datasets


positive_examples_file = "data/LO1_proteinlevel.faa.DIPEP.SPACED_VALS.vec"
negative_examples_file = "data/LO1_proteinlevel.faa.on.trembl.psiblastout.acflat.faa.DIPEP.SPACED_VALS.vec"
negative_examples_file = "data/PAL_proteinlevel.faa.DIPEP.SPACED_VALS.vec"
class clusterset():
    def __init__(self):
        self.data    = []
        self.pos_end = -1
    def makeposnegarray(self,pos_file_name,neg_file_name):
        out_vecs = []
        for line in open(pos_file_name,'r'):
            out_vecs.append( line.strip().split() )
        self.pos_end = len(out_vecs)
        for line in open(neg_file_name,'r'):
            out_vecs.append( line.strip().split() )
        tmp_arr = np.array(out_vecs)
        self.data = tmp_arr.astype(np.float32)
        #self.data.dtype = 'float64'

c = clusterset()
c.makeposnegarray(positive_examples_file,negative_examples_file)

kmeans = KMeans(init='k-means++', n_clusters=2, n_init=2)
print("Cluster object created.")
clusters = kmeans.fit_predict(c.data)
print("Clusters computed.")
cnt_dict = {}

for i in range(0,len(clusters)):
    
    se = str(clusters[i])
    if se in cnt_dict:
        if i < c.pos_end:
            #Pos set.
            cnt_dict[se][0]+=1
        else:
            #Neg Set
            cnt_dict[se][1]+=1
    else:
        if i < c.pos_end:
            cnt_dict.update({se:[1,0]})
        else:
            cnt_dict.update({se:[0,1]})

 
#True positives
#False postives
tps = []
fps = []
col_names = []
for e in sorted(cnt_dict.keys()):
    col_names.append(str(e))
    tps.append( int(cnt_dict[e][0]) )
    fps.append( int(cnt_dict[e][1]) )
    print(e,cnt_dict[e][0],cnt_dict[e][1])


#N = 5
#ind = np.arange(N)    #
#p1 = plt.bar(ind, menMeans,   width, color='r', yerr=womenStd)
#p2 = plt.bar(ind, womenMeans, width, color='y', bottom=menMeans, yerr=menStd)

#plt.title('Cluster Assignments')
#plt.ylabel('Scores')
#plt.xticks(ind+width/2., col_names )
#plt.yticks(np.arange(0,81,10))
#plt.legend( (p1[0], p2[0]), ('True Positives', 'False Negatives') )
#plt.show()