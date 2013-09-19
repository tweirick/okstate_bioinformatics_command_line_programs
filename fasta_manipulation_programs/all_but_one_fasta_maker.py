'''
This program will take a set of files and make the same number of files 
with all entires in the file set minus on of the files.
'''
import urllib.request
from glob import glob
import argparse
import datetime


def getheadcomments():
    desc_list = []
    start_and_break = "'''"
    read_line_bool = False
    for line in open(__file__,'r'):
        if read_line_bool:
            if not start_and_break in line:
                line_minus_newline = line.replace("\n","")
                space_list = []
                for i in range(len(line_minus_newline),80):
                     space_list.append(" ")
                desc_list.append(line_minus_newline+''.join(space_list)+"\n")
            else:
                break    
        if (start_and_break in line) and read_line_bool == False:
            read_line_bool = True
    desc = ''.join(desc_list)
    return desc

def getargs():
 
    desc = getheadcomments()
       
    parser = argparse.ArgumentParser(description=desc)
    
    parser.add_argument('--ID_file_names', 
                        help='')
    args = parser.parse_args()
    return glob(args.ID_file_names)


file_name_set = getargs()
some_set = set(file_name_set)
for name in file_name_set:
    print("cat"," ".join(some_set - set(name)) + " > " + name)
    
    
    
    
    
    
    
    
    
    