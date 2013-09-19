'''
@author: Tyler Weirick
@Created on: 6/18/2012 Version 0.0 
@language:Python 3.2
@tags: svm train 

 /home/TWeirick/COMBINED_FASTAS_6.7.12/40per_6102012/40per_6102012_fastas/NON_REDUNDANT_FASTAS/40_100_40_FASTAS/
'''
from glob import glob
import argparse

def getargs(ver='%prog 0.0'):

    parser = argparse.ArgumentParser(description='Take a blastclust cluster '+
             'file as input and remove all clusters from fasta file set.')    
    parser.add_argument('--file_set', 
                        #action='store_const',
                        #const=sum, 
                        #default=max,
                        help='')
    
    args = parser.parse_args()
    
    return glob(args.file_set)


def getclassnames(file_name):
    '''
    This function returns a list of unique class names found in the vector 
    file. The class name should be the characters encountered in a line 
    until the first space is reached. 
    Input : file_name 
    Output: a list of unique class names. 
    '''
    class_list = []
   
    for line in open(file_name,'r'):
        split_line = line.split()
        if len(split_line) > 1:
            class_name = split_line[0]
            if not class_name in class_list:
                class_list.append(class_name)
        else:
            print("Warning: empty line found.")
            print(file_name,[line])
    if len(class_list) == 0:
        print("Error: no class names in output list.")
        print(line)
    return class_list


#=============================================================================
#Start Main Program
#=============================================================================
    
file_glob = getargs()

for file_name in file_glob:

    class_list = getclassnames(file_name)
    #output_strings_list = maketrainingfileforeachclass(file_name,class_list)
    
    pos_set_mark = "+1"
    neg_set_mark = "-1"
    for vec_class in class_list:
        output_strings_list = []
        for line in open(file_name,'r'):
            out_line = ""
            split_line = line.split()
            
            if len(split_line) > 1:
                if split_line[0] in class_list:
                     if split_line[0] == vec_class:
                         split_line[0] = pos_set_mark
                     else:
                         split_line[0] = neg_set_mark
                else:
                    print("Warning: Entry found not in classes.")
            output_strings_list.append(" ".join(split_line)+"\n")
        
         
        out_file_name = file_name+"."+vec_class+"."+"trnvec"
        print(out_file_name,len(output_strings_list))
        
        #Sort so that counting pos and neg vectors is easier.
        output_strings_list = sorted(output_strings_list)
        
        
        out_file = open(out_file_name,'w')
        out_file.write("".join(output_strings_list))
        out_file.close()




