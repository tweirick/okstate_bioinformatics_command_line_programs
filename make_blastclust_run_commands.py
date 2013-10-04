#!/usr/bin/python
"""
@author: Tyler Weirick
@created: 2012-3-7
This program will make qsub files for submission to blastclust. 
"""
import sys
import argparse
import re
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


#Get a set of file names 
parser = argparse.ArgumentParser(description=getheadcomments())
parser.add_argument('--file_set',help='')
parser.add_argument('--path',help='',default="/scratch/tweiric")
args = parser.parse_args()
sorted_file_glob = sorted(glob(args.file_set))
    
print("#!/bin/bash")

for file_name in sorted_file_glob:

    out_list = [
    "#!/bin/bash",
    "#PBS -q batch",
    "#PBS -l nodes=1:ppn=12",
    "#PBS -l walltime=100:00:00",
    "#PBS -N blast_plus_example",
    "#PBS -j oe",
    "date",
    "module load blast+",
    "cd "+args.path,
     "/home/tweiric/blast-2.2.20/bin/blastclust -i "+file_name+" -o "+file_name+".blastclust -p T -L 1.0 -b T -S 40 -e F",
    "date"
    ]
    fn = file_name+".blastclust.qsubsh"
    file = open(fn,"w")
    file.write("\n".join(out_list))
    file.close()

    print("qsub ",fn)

