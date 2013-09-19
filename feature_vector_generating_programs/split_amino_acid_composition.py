#!/opt/python3/bin/python3

'''
@Created on 4/19/2012  
@author: Tyler Weirick
This program will calculate the split amino acid composition of amino acids in a 
fasta sequence.  
'''

#from optparse import OptionParser
import argparse
from glob import glob
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
    
    
    
def splitaminoacidcomposition(fasta_sequence,start_counting_from=1,terminal_len=25):
    """
    This function will open and read a amino acid contaning fasta file (.faa) 
    Based on "Combining machine learning and homology-based approaches to 
    accurately predict subcellular localization in Arabidopsis"
    http://www.ncbi.nlm.nih.gov/pubmed/20647376
    
    This basically calculates the average of the first X number of aas 
    the last x number of aas and the remaining middle portion. 
    """
    
    if not len(fasta_sequence) > terminal_len*2:
        print("ERROR: fasta sequence too short.")
        sys.exit()
    
    #Ensure sequence is upper case so the sequence elements can be recognized. 
    fasta_sequence = fasta_sequence.upper()   
    
    #You may want to use a number differenct that 25 that was found to be best for the paper cited.
    split_sequence = [fasta_sequence[0:terminal_len],
                      fasta_sequence[terminal_len:-terminal_len],
                      fasta_sequence[-terminal_len:]]
    
    #Start with space as a space is added after each vector element but not 
    #for first case. 
    out_vector_list = [" "]
    #Use this in case you want to compound this calculation with others in the future. 
    i = start_counting_from
    for sub_sequence in split_sequence:
        
        aa_dic = {'A':0, 'C':0, 'D':0, 'E':0, 'F':0,
                  'G':0, 'H':0, 'I':0, 'K':0, 'L':0,
                  'M':0, 'N':0, 'P':0, 'Q':0, 'R':0,
                  'S':0, 'T':0, 'V':0, 'W':0, 'Y':0}
        #Count aa's present
        for aa in sub_sequence:
            if aa in aa_dic:
                aa_dic[aa]+=1
            else:
                if aa != "\n" and aa != "\t" and aa != " ":
                    print(fasta_sequence)
                    print("ERROR: unidentified char",aa)
        
        #Convert data struct into vector format
        for key in sorted(aa_dic):
            average_float = float(aa_dic[key])/float(len(sub_sequence))
            out_vector_list.append(str(i)+":"+'{number:.{digits}f} '.format(number=(average_float),digits=5))
            i+=1
            
    out_vector_list.append("\n")
    return ''.join(out_vector_list)
    
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
                SVM_vector = set_type+" "+ splitaminoacidcomposition(''.join(fasta_data))
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
    SVM_vector = set_type+" "+ splitaminoacidcomposition(''.join(fasta_data))
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
    
    output_file_name = file_name+".splitaa.vec" 
    #print(svm_data)
    #print(output_file_name,len(svm_data))
    out_file = open(output_file_name,'w')
    out_file.write(''.join(svm_data))
    out_file.close()

    
