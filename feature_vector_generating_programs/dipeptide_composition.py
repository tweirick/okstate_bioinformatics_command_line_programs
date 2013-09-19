#!/opt/python3/bin/python3

'''
@Created on 4/19/2012  
@author: Tyler Weirick
This program will calculate the dipeptide composition of amino acids in a 
fasta sequence.  
'''

#from optparse import OptionParser
import argparse
from glob import  glob
import sys


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
           default="", 
           help='File or regex. If regex put in quotes.')

    parser.add_argument('--set_type', 
          default="",
          help='If not given, will name of file before first period.')
    
    args = parser.parse_args()
    return sorted(glob(args.file_set)),args.set_type



def builddipeptidedict():
    """
    Making a 400 element dictionary by hand is a pain in the ass, so I will 
    build it programmatically each time the program is executed.
    Input : None
    Output: A dictionary containing an amino acid di-peptied adn the key and 
            zero as the value'WG': 0, 'WF': 0,...
    """
    #The twenty amino acids. 
    aa_dic = ['A','C','D','E','F','G','H','I','K','L',
              'M','N','P','Q','R','S','T','V','W','Y']
    
    dipeptide_dict = dict()
    
    #Build the dipeptide dictionary.
    for x in aa_dic:
        for y in aa_dic:
            dipeptide_dict.update({ x+y:0 })
    return dipeptide_dict
    
    
    
def dipedtidecomposition(fasta_entry):
    """
    This function will open and read a amino acid contaning fasta file (.faa) 
    
    """
    fasta_entry = fasta_entry.upper()
    aa_dic = ['A','C','D','E','F','G','H','I','K','L',
              'M','N','P','Q','R','S','T','V','W','Y'] 
    #Build the dipeptide dictionary.
    dipeptide_dict = dict()
    for x in aa_dic:
        for y in aa_dic:
            dipeptide_dict.update({ x+y:0 })
    #return dipeptide_dict
 
    #get a fasta entry !!!!!!!!!!!!!!!!!!!!!!!!11
    #exclude name and all formatting chars. 
    fasta_entry_len = len(fasta_entry)
    for i in range(1,fasta_entry_len-1):
        #print(fasta_entry[i-2:i])
        if fasta_entry[i-1:i] in dipeptide_dict:
            dipeptide_dict[fasta_entry[i:i+2] ]+=1
        elif fasta_entry[i:i+2] in dipeptide_dict:
            dipeptide_dict[fasta_entry[i:i+2]]+=1
    
    out_vector_list = [" "]
    i = 0
    for key in sorted(dipeptide_dict):
        average_float = float(dipeptide_dict[key])/float(fasta_entry_len)
        out_vector_list.append(str(i+1)+":"+'{number:.{digits}f} '.format(number=(average_float),digits=5))
        i+=1
    out_vector_list.append("\n")
    
    return ''.join(out_vector_list)
    
    
    
    
    
def convertotosvm(file_name,set_type):
    """
    Input : 
    file_name(str) - Name of a fasta file.
    set_type(str) - Name to put at the start of the vector. 
    Output: collection of SVM formatted strings
    
    This function separates each fasta from the file and passes it to
    the function dipedtidecomposition to be converted into svm format.
    It also collects and assembles the multiple lines of svm formatted
    output into a string.
    """
    out_data = []
    fasta_data = []
    fasta_name = ''
    
    #Read through line by line. This is done iteratively to allow for very
    #large files. 
    for line in open(file_name,"r"):

        if line[0] == '>':
            """
            If the start of a fasta entry enter data 
            """
            if fasta_name != '':
                #Build the 
                #print(fasta_data)
                #print( dipedtidecomposition(''.join(fasta_data)))
                SVM_vector = set_type+" "+ dipedtidecomposition(''.join(fasta_data))
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
    SVM_vector = set_type+" "+ dipedtidecomposition(''.join(fasta_data))
    out_data.append(SVM_vector)
    return ''.join(out_data)





file_glob,set_type = getargs()

for file_name in file_glob:
     
    if set_type == "":
        set_type = file_name.split(".")[0]
        svm_data = convertotosvm(file_name,set_type)
        set_type = ""
    else:
        svm_data = convertotosvm(file_name,set_type)
    
    output_file_name = file_name+".dipep.vec" 

    #print(svm_data)
    print(output_file_name,len(svm_data))
    out_file = open(output_file_name,'w')
    out_file.write(''.join(svm_data))
    out_file.close()


















