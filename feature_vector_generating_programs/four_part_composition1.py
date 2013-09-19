#!/opt/python3/bin/python3

'''
@Created on 4/19/2012  
@author: Tyler Weirick
This program will calculate the dipeptide composition of amino acids in a 
fasta sequence.  
'''

from optparse import OptionParser
import glob
import sys
from math import floor

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
        
    parser.add_option("-i", "--in_file_name", 
                      dest="in_file_name", 
                      default="",
                      help = "Input file name.")
    
    parser.add_option("-s", "--set_type", 
                      dest="set_type", 
                      default="0",
                      help = "-1 for negative set, "+
                      "0 for classification, 1 for positive training set.")
        
    parser.add_option("-o", "--output_file_name", 
                      dest="output_file_name", 
                      default="",
                      help = "Output file name.")
    
    (options, args) = parser.parse_args()
    if(troubleShoot):print(options);print(args)
            
    in_file_name     = options.in_file_name
    set_type         = options.set_type
    output_file_name = options.output_file_name
    
    return in_file_name,set_type,output_file_name


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
    
    
    
def splitaminoacidcomposition(fasta_entry,vector_type,start_counting_from=1):
    """
    This function will open and read a amino acid contaning fasta file (.faa) 
    Based on "Combining machine learning and homology-based approaches to 
    accurately predict subcellular localization in Arabidopsis"
    http://www.ncbi.nlm.nih.gov/pubmed/20647376
    
    This basically calculates the average of the first X number of aas 
    the last x number of aas and the remaining middle portion. 
    """
    
    sequence_len = len(fasta_sequence)
    #if not sequence_len > terminal_len*2:
    #    print("ERROR: fasta sequence too short.")
    #    sys.exit()
    
    #Ensure sequence is upper case so the sequence elements can be recognized. 
    fasta_sequence = fasta_sequence.upper()   
    
    #You may want to use a number differenct that 25 that was found to be best for the paper cited.
    
    split_at_x = floor(sequence_len/4)
    
    split_sequence = [fasta_entry[0:terminal_len],
                      fasta_entry[terminal_len:-terminal_len],
                      fasta_entry[terminal_len:-terminal_len],
                      fasta_entry[-terminal_len:]]
    
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
        for aa in fasta_sequence:
            if aa in aa_dic:
                aa_dic[aa]+=1
            else:
                if aa != "\n" and aa != "\t" and aa != " ":
                    print("ERROR: unidentified char",aa)
        
        #Convert data struct into vector format
        for key in sorted(aa_dic):
            average_float = float(aa_dic[key])/float(sub_sequence)
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
    SVM_vector = set_type+" "+ dipedtidecomposition(''.join(fasta_data))
    out_data.append(SVM_vector)
    return ''.join(out_data)




in_file_name,set_type,output_file_name = getargs(ver='%prog 0.1')
vector_string = convertotosvm(in_file_name,set_type)
#print(vector_string)

if output_file_name == "":
    print(vector_string)
else:
    out_file = open(output_file_name,'w')
    out_file.write(vector_string)
    out_file.close()
    
    
