'''
This program accepts a regex describing a set of best-stats files and 
calculates the overall statistics of the classifier.  

The format of these files is a line containing the following data:
overall number_of_folds: 10     g:1.0   j:8.5   c:31.0  accuracy: 99.74 error: 0.03	getMCC: 0.82360 precision: 95.24        sensitivity: 71.43	specificity: 99.97      FN: 8.0 FP: 1.0 TP: 20.0        TN: 3408.0
'''
from glob import glob 
import argparse

parser = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('--file_set',help='')
args = parser.parse_args()

file_glob = sorted(glob(args.file_set))
    
#This holds the overall stats 
stat_dict = {}

total_seqs = 0
total_negative_seqs = 0
for file_name in file_glob:
    for line in open(file_name,'r'):
        sp_line = line.strip().split("\t")
        #Need to get TP and FN

        fns = float( sp_line[-4].split(":")[-1].strip() )
        fps = float( sp_line[-3].split(":")[-1].strip() )
        tps = float( sp_line[-2].split(":")[-1].strip() )
        tns = float( sp_line[-1].split(":")[-1].strip() )

        total_seqs+=tps+fns
        total_negative_seqs = tns+fps
        for stat_el in sp_line[5:-4]:
            stat_type,stat_val = stat_el.split(":")
            stat_type = stat_type.strip()
            stat_val  = float(stat_val.strip())

            stat_val = stat_val*(tps+fns)

            if stat_type in stat_dict:
                stat_dict[stat_type]+=stat_val
            else: 
                stat_dict.update( {stat_type:stat_val} ) 

for el in sorted( stat_dict.keys() ): 
    print(el+":",stat_dict[el]/total_seqs,end="\t")

