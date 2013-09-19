#web_convert_uniprot_ac_to_fasta.py
'''
convert_GI_or_Assesion_to_fasta.py
@author: Tyler Weirick
@Created on: 5/16/2012 Version 0.0 
@language:Python 3.2
@tags: Uniprot AC flat-file Web

http://www.uniprot.org/batch/?query=
A3N335+A0KP02&format=fasta
'''


from html.parser import HTMLParser
from glob import glob
import urllib.request
from optparse import OptionParser
import argparse


def getargs(ver='%prog 0.0'):

    parser = argparse.ArgumentParser(description='Process some integers.')
    
    parser.add_argument('--file_set', 
                        #action='store_const',
                        #const=sum, 
                        #default=max,
                        help='')
    
    args = parser.parse_args()
    return args.file_set



HTML_HEAD = "http://www.uniprot.org/batch/?query="
HTML_TAIL = "&format=fasta"
file_set_name = getargs()

print("File_Name\t#_of_AC_numbers\tNumber_of_fastas")
#print(file_name)
for file_name in glob(file_set_name):
   
    AC_name_list = []
    for line in open(file_name,'r'):
        AC_name_list.append(line.strip())
        
    
    source_out = []
    temp_list  = []
    for i_ac in range(0,len(AC_name_list)):
        
        if (i_ac != 0 and i_ac%100 == 0) or i_ac == len(AC_name_list)-1 :
            query_str = "+".join(temp_list)
            url = HTML_HEAD + query_str + HTML_TAIL
            response = urllib.request.urlopen(url)
            source = response.read().decode()
            source_out.append(source)
            temp_list = []
        temp_list.append(AC_name_list[i_ac])
    
    fasta_count_int = 0
    
    source_txt = ''.join(source_out)
    
    for e in source_txt:
        if ">" in e:
            fasta_count_int+=e.count(">")
            
    print(str(file_name)+"\t"+str(len(AC_name_list))+"\t"+str(fasta_count_int))
    
    out_file = open(file_name+".fasta","w")
    out_file.write(source_txt)
    out_file.close()
    
    
    
    
