'''
@author: Tyler Weirick 
@date: 2013-09-24

This program will remove sequence and name matches from one file 
that match another. 
'''
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--file_name1',
    help='A set of fastas, fastas will be removed from this file.')

parser.add_argument('--file_name2',
    help='Any fasta entry within this set will be omited from the main set.')

args = parser.parse_args()
file_name1 = args.file_name1
file_name2 = args.file_name2

#Make name and sequence dicts 

file2 = open(file_name2,'r')
fasta_name = None
fasta_seq_list  = []
fasta_seq_set  = set()
fasta_name_set = set()

while True: 
     line = file2.readline()
     if line == "" or line[0] == ">":
          if line != "" and fasta_seq_list != []:
              joined_seq = "".join(fasta_seq_list)
              if joined_seq in fasta_seq_set:
                   print(joined_seq)
              fasta_seq_set.add( "".join(fasta_seq_list) )
          if line == "":
              break
          fasta_name_set.add( line.strip() )
          fasta_seq_list = []
     else:
         fasta_seq_list.append( line.strip() )
     
print(len( fasta_name_set ))
print(len( fasta_seq_set  ))


