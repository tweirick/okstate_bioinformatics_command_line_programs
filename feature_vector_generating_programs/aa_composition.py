#!/opt/python3/bin/python3

'''
@author: Tyler Weirick
@Created on: 12/9/2011 Version 0.0 
@language:Python 3.2
@tags: amino acid composition aacomp vector

This program will calculate the percentage of amino acids in a fasta file. 
'''

from optparse import OptionParser
import argparse
from glob import glob
import sys


exclusion_dict = {}

def getargs(ver='%prog 0.1'):
    """
    Gets file names for input and output.
    """
    desc = []
    start_and_break = "'''"
    read_line_bool = False
    for line in open(__file__,'r'):
        if read_line_bool:
            if not start_and_break in line:
                desc.append(line.replace("\n","")+"\n")
            else:
                break
        if (start_and_break in line) and read_line_bool == False:
            read_line_bool = True
    desc = ''.join(desc)

    troubleShoot = False
    parser = OptionParser(version=ver,description=desc)
        
    parser.add_option("-i", "--file_set", 
                      dest="file_set", 
                      default="",
                      help = "Input file set.")
    
    parser.add_option("-s", "--set_type", 
                      dest="set_type", 
                      default="",
                      help = "This will be added at the start of vector lines.")
        
    #parser.add_option("-o", "--output_file_name", 
    #                  dest="output_file_name", 
    #                  default="20",
    #                  help = "Output file name.")
    
    (options, args) = parser.parse_args()
    if(troubleShoot):print(options);print(args)
            
    file_set     = options.file_set
    set_type         = options.set_type
    #output_file_name = options.output_file_name
    
    return sorted(glob(file_set)),set_type#,output_file_name


def aapercentages(fasta_sequence,file_name):
    global exclusion_dict
    #print(fasta_sequence)
    """
    This will only count the 20 amino acid characters all others will be 
    ignored. 
    Input :a protein sequence string
    Output: SVM formatted string
    """
    seq_len = len(fasta_sequence)
    #print(seq_len)
    aa_dic = {'A':0, 'C':0, 'D':0, 'E':0, 'F':0,
              'G':0, 'H':0, 'I':0, 'K':0, 'L':0,
              'M':0, 'N':0, 'P':0, 'Q':0, 'R':0,
              'S':0, 'T':0, 'V':0, 'W':0, 'Y':0}
    
    fasta_sequence = fasta_sequence.upper()
    file_error_bool = False
    for aa in fasta_sequence:
        if aa in aa_dic:
            aa_dic[aa]+=1
        else:
            if aa != "\n" and aa != "\t" and aa != " ":
                #print("ERROR: unidentified char",aa,"in",file_name)
                #print([fasta_sequence])
                if not file_error_bool:
                    file_error_bool = True
                    if file_name in exclusion_dict:
                        exclusion_dict[file_name]+=1
                    else:
                        exclusion_dict.update({file_name:1})
    out_list = []
    i = 0
    sp = ''
    #print(aa_dic["A"])
    for aa_el in sorted(aa_dic):
       
       out_list.append(sp+str(i+1)+":"+'{number:.{digits}f}'.format(number=(float(aa_dic[aa_el])/float(seq_len)),digits=5))
       
       sp = " "
       i+=1
    return ''.join(out_list)


def convertotosvm(file_name,set_type):
    """
    Input : file name string
    Output: collection of SVM formatted strings
    
    This function separates each fasta from the file and passes it to
    the function aapercentages to be converted into svm format.
    It also collects and assembles the multiple lines of svm formatted
    output into a string.
    """
    out_data = []
    fasta_data = []
    fasta_name = ''
    #Make sure is string
    set_type = str(set_type)
    #Read through line by line. This is done iteratively to allow for very
    #large files. 
    for line in open(file_name,"r"):

        if line[0] == '>':
            """
            If the start of a fasta entry enter data 
            """
            if fasta_name != '':
                #Build the 
                SVM_vector = set_type+" "+aapercentages(''.join(fasta_data),file_name )+'\n' 
                out_data.append(SVM_vector)
                fasta_data = []
                fasta_name = line
            else:
                fasta_name = line    
        else:
            fasta_data.append(line.strip())
    """
    Add data from final fasta entry. As there is no '>' char to trigger it's
    addition. 
    """
    SVM_vector = set_type+" "+aapercentages(''.join(fasta_data),file_name )+'\n' 
    out_data.append(SVM_vector)
    #print(out_data)
    return out_data



#file_glob,set_type,output_file_name = getargs()
file_glob,set_type = getargs()

for file_name in file_glob:
     
    if set_type == "":
        set_type = file_name.split(".")[0]
        svm_data = convertotosvm(file_name,set_type)
        set_type = ""
    else:
        svm_data = convertotosvm(file_name,set_type)
    
    output_file_name = file_name+".aacomp.vec" 
    
    #print(svm_data)
    print(output_file_name,len(svm_data))
    out_file = open(output_file_name,'w')
    out_file.write(''.join(svm_data))
    out_file.close()

print("exclusion_dict------------")
for name  in sorted(list(exclusion_dict)):
    print(name,exclusion_dict[name])




