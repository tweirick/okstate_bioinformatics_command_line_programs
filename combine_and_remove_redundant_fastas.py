'''
@author: Tyler Weirick
@date:  2013-09-02
This program will accept a regex of fastas and output a unique combined fasta. 
'''
import argparse
from glob import glob

parser = argparse.ArgumentParser(
   description=open(__file__).read().split("'''")[1],
   formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('--file_set', help='''The name of a fasta formatted file.''', required=True)
args = parser.parse_args()
file_glob = glob(args.file_set)

out_list = []
print_line_bool = True 
line_set = set()
for file_name in file_glob:
    file = open(file_name,'r')
    while True: 
         line = file.readline()
         if len(line) == 0:
             #print()
             break
         else:
             if line[0] == ">":
                 if line in line_set: 
                     print_line_bool = False
                 else:
                     line_set.add(line)
                     print_line_bool = True

             sline = line.strip()
             if print_line_bool and sline != "":
                 print(sline)    



 
