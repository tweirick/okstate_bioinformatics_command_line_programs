"""
Add file names to this list in the order you want them combined. 
"""

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--file_list',
                   help='A list of file names seperated by commas. ')
parser.add_argument('--out_file_name',
                   help='A list of file names seperated by commas. ')
args = parser.parse_args()
file_name = args.file_list

file_list = args.file_list.split(",")
#file_list = ["AUY922_normalized_HandL_intensities_08092013.txt.filtered.txtt-test_pvals.txt",
#               "AUY922_normalized_HandL_intensities_08092013.txt.filtered.txtwilcox-pvals.txt",
#               "AUY922_normalized_HandL_intensities_08092013.txt.filtered.txtwilcox-pvals.txt.stoky.txt"]
out_file_name = args.out_file_name

out_list = []
first_file = True
for file_name in file_list: 
    cnt=0
    for line in open(file_name,'r'):
        if first_file:
            out_list.append(line.strip())
        else:
            out_list[cnt]+="\t"+line.strip()
        cnt+=1
    first_file = False

assert out_file_name != ""
of = open(out_file_name,'w')
of.write("\n".join(out_list))
of.close()
