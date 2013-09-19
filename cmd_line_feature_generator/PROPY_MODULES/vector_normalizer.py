'''
descriptor.
'''
desc=""
import argparse
from glob import glob
import math


def average(s): 
    return sum(s)/len(s)

def variance(s,avg): 
    return list(map(lambda x: (x - avg)**2, s))

def stddev(variance_list):
    return math.sqrt(average(variance_list))


def getargs(desc,ver='%prog 0.0'):
    '''
    This function handles the command line arguments. 
    '''

    parser = argparse.ArgumentParser()
    #description=desc,
    #formatter_class=argparse.RawDescriptionHelpFormatter
    
    parser.add_argument('--file_set', 
        help='''Accepts single files or regex used "" for regexes ex: --file_set "*.faa" ''')

    #parser.add_argument('--normalization_type', 
    #    help=''' val-min or STDDEV ''')

    parser.add_argument('--indexes_to_normalize', 
        help='''ex:1,2,4,5-8,10''')
   
    args = parser.parse_args()
    return glob(args.file_set),args.indexes_to_normalize #args.normalization_type,


file_glob,indexes_to_normalize = getargs(desc)#normalization_type



columns_to_normalize = set()

for e in indexes_to_normalize.split(","):
    if "-" in e:
        x,y = e.split("-")
        for i in range(int(x),int(y)+1):
            columns_to_normalize.update({i}) 
    else:
         columns_to_normalize.update({ int(e) }) 

#Now we have all columns we wish to normalize. 
set_list = sorted(list(columns_to_normalize))

point_pos_and_max_min_vals = []
tmp_max = None
tmp_min = None
for column in set_list:
    #print(column)
    tmp_max     = None
    tmp_min     = None
    col_vals_list = []    
    #average_val = None
    #N=0
    for file_name in file_glob:
        for line in open(file_name,"r"):
            if line.strip()!="":
                line_pos_value_pairs = float(line.split()[column].split(":")[-1])
                if tmp_max == None or tmp_max > line_pos_value_pairs:
                    tmp_max = line_pos_value_pairs
                if tmp_min == None or tmp_min < line_pos_value_pairs:
                    tmp_min = line_pos_value_pairs
                col_vals_list.append(line_pos_value_pairs)
                
    average_val = average(col_vals_list)      
    vari = variance(col_vals_list,average_val)
    sdev = stddev(vari)
    point_pos_and_max_min_vals.append([column,tmp_max,tmp_min,average_val,sdev])
        

for file_name in file_glob:
    std_outlist    = []
    maxmin_outlist = []
    for line in open(file_name,"r"):
        if line.strip() != "":
            split_line = line.split()
            split_line1 = line.split()
            for min_max in point_pos_and_max_min_vals:
                el_number,min_val,max_val,mean_val,sdev = min_max
                number,val = split_line[el_number].split(":")
                
                val = float(val)
                split_line[el_number] = str(number)+":"+'{number:.{digits}f} '.format(number=(((val - min_val)/(max_val-min_val))),digits=5)
                split_line1[el_number] = str(number)+":"+'{number:.{digits}f} '.format(number=(((val - mean_val)/(sdev))),digits=5)
                    
            maxmin_outlist.append(" ".join(split_line))
            std_outlist.append(" ".join(split_line1))
            
    outfile = open(file_name+".max-min.vec","w")
    outfile.write("\n".join(maxmin_outlist))
    outfile.close()
    
    outfile = open(file_name+".stdev.vec","w")
    outfile.write("\n".join(std_outlist))
    outfile.close()

    
     


