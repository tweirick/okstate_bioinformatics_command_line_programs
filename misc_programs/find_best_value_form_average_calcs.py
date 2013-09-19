'''
run_svm_learn.py
@author: Tyler Weirick
@Created on: 7/12/2012 Version 0.0 
@language:Python 3.2
@tags: svm train 

This program finds the best result in output from run_svm_learn.py
'''
import argparse
from glob import glob
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

def getargs(ver='%prog 0.0'):

    parser = argparse.ArgumentParser(description=getheadcomments())    
    
    parser.add_argument('--file_set', 
                        help='')

    args = parser.parse_args()
    return sorted(glob(args.file_set))



#Get set of files 
file_glob = getargs()

#For each file in set.
for file_name in file_glob:
    icnt = 0
    largest_value = None
    best_condition = "No Condition"
    list_rank = []
    for line in open(file_name,'r'):
        # 0 1         2                3      4                  5                              6
        #75 Accuracy 93.47547770360133 Error 6.524522296398656 Matthews_correlation_coefficient 0.7857192408599665 Precision 79.62692961664197 Sensitivity 86.12973165287632 Specificity 94.63573485413787 TOTAL 1.0
    
        split_line = line.split()
        #Name of best condition, for linear kernel.
        c_condition = split_line[0]
        #For now get matthew's coefficient
        mcc_name  = split_line[5]
        mcc_value = split_line[6]
        
        list_rank.append([float(c_condition),mcc_value])
        
        if largest_value == None:
            print("Comparing",mcc_name)
            largest_value  = mcc_value
            best_condition = c_condition
        elif mcc_value > largest_value:
            print(c_condition,"better than",best_condition)
            largest_value  = mcc_value
            best_condition = c_condition



print("The best condition is",best_condition)



out_str = ["cvalue,mcc"]
for e in sorted(list_rank):#,reverse=True
    out_str.append(str(e[0])+","+e[1][0:6])    
    
out_file_name = file_name+".best"+"_c"+best_condition+".csv"
print("Writing to",out_file_name)
out_file = open(out_file_name,'w')
out_file.write('\n'.join(out_str))
out_file.close()
    
    
    
    
    
    