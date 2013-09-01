'''
@author: Tyler Weirick
@date 2013-7-16
==============================================================================
This program will combine rows from two different tab delimited text files 
based on the keys from a column. 
=============================================================================
'''

from math import fsum
from sys import hexversion
import argparse

#=============================================================================
#                                 Constants
#=============================================================================
MIN_VERSION = "0x30200f0"
#Enter the file names here. 
#=============================================================================
#                                 Functions
#=============================================================================

def outputtotsv(file_name,file_set,file_dict):
    """
    Output a the list contained as a value in a dict as a tsv file.
    names as the file name. 
    """
    output_list = []
    for key_el in file_set:
        output_list.append("\t".join(file_dict[key_el]))
    out_file = open(file_name,"w")
    out_file.write("\n".join(output_list))
    out_file.close()


def averageofnumberlist_ignorezeros(numb_list):
    assert type(numb_list) == list
    f_sum = 0.0
    el_cnt = 0.0
    for el in numb_list:
        f_sum+=float(el)
        if float(el) != 0.0:
           el_cnt+=1.0
    return f_sum/el_cnt

def outputintersectiontotsv(out_file_name,file_set,file_dict1,file_dict2):
    """
    Output a the list contained as a value in a dict as a tsv file.
    names as the file name. 
    """
    average_cutoff = 0.6 
    max_pval       = 0.5
    output_list = []
    for key_el in file_set:
        #average netative log2 ratio for file1, need to ignore zeros
        #numb_list = file_dict1[key_el][ratio_col_start:ratio_col_end]
        #file1_avg_log2_val = averageofnumberlist_ignorezeros(numb_list)*-1
        #average negative log2 ration for file2 
        #numb_list = file_dict2[key_el][ratio_col_start:ratio_col_end]
        #averageofnumberlist_ignorezeros(numb_list)
        #file2_avg_log2_val = averageofnumberlist_ignorezeros(numb_list)*-1
        #f1out_pval_list = []
        #f2out_pval_list = []
        #for int_el in pvalue_cols_list:
        #   #Check pvals for file1 
        #   f1out_pval_list.append(
        #   converttoplusorblank(file_dict1[key_el][int_el],
        #   max_pval,file1_avg_log2_val,average_cutoff)
        #   )
        #   #Check pvals for file2 
        #   f2out_pval_list.append(converttoplusorblank( file_dict2[key_el][int_el],
        #   max_pval,file2_avg_log2_val,average_cutoff))
        output_list.append(
            "\t".join(file_dict1[key_el])+"\t"+"\t".join(file_dict2[key_el])
        )
    out_file = open(out_file_name,"w")
    out_file.write("\n".join(output_list))
    out_file.close()
    

def average(ac_num,txt_list,illegal_str="No Values"):
    """
    This function averages the values from a list. Some of the elements may 
    contain the string "No Values" thus we will remove these before averageing
    the numerical values. If there are more "No Values" than normal values in 
    the list an average will not be preformed and "No Values" will be returned.
    If an average is done the float will be returned as a string. 
    """

    if illegal_str in txt_list:
        print("WARNING: ",txt_list.count(illegal_str),"found in ",ac_num)

    numbers_only_list = [x for x in txt_list if x != illegal_str]

    if float(len(numbers_only_list)) / float(len(txt_list)) > 0.5:
        sum_val = fsum([float(i) for i in numbers_only_list])
        return str( float(sum_val)/float(len(numbers_only_list)) )
    else:
        return illegal_str


def converttoplusorblank(pval,max_pval,average_value,average_cutoff):
    average_cutoff = float(average_cutoff)
    average_value = abs(float(average_value))
    pval = float(pval)
    max_pval = float(max_pval)

    if pval <= max_pval and average_value >= average_cutoff:
        return '"+"'
    else:
        return '"-"'


def tsvtodict(file_name,num_of_key_col):
    """
    This function converts a tab delimited to a dictionary with the specified 
    column number num_of_key_col as the key. 
    """
    prot_dict = {}
    start_reading = True
    max_pval = 0.05
    for line in open(file_name,'r'):
       split_line = line.strip().split("\t")
       key_val = split_line[num_of_key_col]
       if not key_val in prot_dict:
           prot_dict.update({key_val:split_line})       
       else: 
           print('Warning: Overlapping values "'+key_val+'" found in file '+file_name+".")

    return prot_dict


#=============================================================================
#                                 Main Program
#=============================================================================

parser = argparse.ArgumentParser()
parser.add_argument('--file_name1',
                   help='Input the name of the file to be processed. ')
parser.add_argument('--file_name2',
                   help='Input the name of the file to be processed. ')
parser.add_argument('--key_col_number',
                   help='The number of the column where the repicates end.',
                   default=10)
args = parser.parse_args()
file1           = args.file_name1
file2           = args.file_name2
assert file1 != file2
#To allow for entry as col appear in excel. 
key_col_number  = int(args.key_col_number)  -1

#Convert the tsv files to dicts 
file_dict1 = tsvtodict(file1,key_col_number)
file_dict2 = tsvtodict(file2,key_col_number)

print("Number of unique entries in",file1+":",len(file_dict1))
print("Number of unique entries in",file2+":",len(file_dict2))
#Generate sets of acs
set1 = set(file_dict1.keys())
set2 = set(file_dict2.keys())
#Get the overlapping acs 
intersetion_of_files = set1 & set2
print("Number of overlapping entries between",file1,"and",file2+":",len(intersetion_of_files))
out_file_name = file1.strip(".txt")+"_"+file2.strip(".txt")+"intersection.txt"
outputintersectiontotsv(out_file_name,intersetion_of_files,file_dict1,file_dict2)
         
unique_to_file1 = set1 - set2
print("Number of unique entries in",file1,":",len(unique_to_file1))
file_name = file1.strip(".txt")+"_disjoint"+file2.strip(".txt")+".txt"
outputtotsv(file_name,unique_to_file1,file_dict1)

unique_to_file2 = set2 - set1
print("Number of unique entries in",file2,":",len(unique_to_file2))
file_name = file2.strip(".txt")+"_disjoint"+file1.strip(".txt")+".txt"
outputtotsv(file_name,unique_to_file2,file_dict2)


