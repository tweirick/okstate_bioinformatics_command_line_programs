'''
@Created on Oct 24, 2011 
@author: Tyler Weirick
@keyword: fasta error split 
This program reads through a set of fasta file and removes the characters 
which designate errors (the default is x). If error characters are found to 
contain an erroneous character the fasta will be split at these characters    
'''
from optparse import OptionParser
import glob
import sys

MAX_CHARS_PER_LINE = 80

def getargs(desc="",ver='%prog 0.1'):
    """Gets file names for input and output 
    will use the first name and append out on the end of the file
    if no outfile name is given"""
    
    troubleShoot = False
    parser = OptionParser(version=ver,description=desc)
        
    parser.add_option("-i", "--in_file_name", 
                      dest="in_file_name", 
                      default="",
                      help = "Input file name or regular expression.")
        
    parser.add_option("-e", "--error_char", 
                      dest="error_char", 
                      default="x",
                      help = "The character which designates an erroneous reading. If this argument is not give the error character will default to 'x'")
    
    parser.add_option("-l", "--minimun_sequence_length", 
                      dest="minimun_sequence_length", 
                      default=15,
                      help = "All values below this integer will be excluded. Default value is 15.")
    
    
    (options, args) = parser.parse_args()
    if(troubleShoot):print(options);print(args)
            
    in_file_name = options.in_file_name
    error_char = options.error_char
    minimun_sequence_length = options.minimun_sequence_length
    
    error_char = str(error_char)
    if len(error_char) !=1: sys.exit("error_char must be one character.")
    
    minimun_sequence_length = int(minimun_sequence_length)
    if minimun_sequence_length < 0: sys.exit("minimun_sequence_length cannot be negative.")
          
    file_list = glob.glob(in_file_name) 

    return file_list,error_char,minimun_sequence_length

def format_fasta(data):
    i=0
    if type(data) == list:
        data = ''.join(data)
        
    rtn_list = list()
    data = data.replace('\n', '')
    
    for e in data:
        if (i%MAX_CHARS_PER_LINE == 0 and i!=0):
            rtn_list.append('\n') 
        rtn_list.append(e)
        i+=1
    rtn_list.append('\n')
    return ''.join(rtn_list)



def removeerrorcharsfromfasta(fasta_tag,fasta_data,error_char,minimun_sequence_length):
    """
    This function takes the information for one fasta entry, if no error chars are found 
    the fasta entry will be returned as it entered. If a error character is found the 
    fasta will be returned as a number of fasta entries split around the error chars.  
    """
    out_list = list()
    
    #if fasta_data[0] == fasta_data[0].upper():
    #    """If True then the sequence in in upper case."""
    #    split_data = fasta_data.split(error_char.upper())
    #else:
    #    """If False then the sequence in in upper case."""
    #    split_data = fasta_data.split(error_char.lower())
    
    split_data = fasta_data.upper().split(error_char.upper())
    
    i=0
    for fasta_sub_seq in split_data:
        if len(fasta_sub_seq) >= minimun_sequence_length:
            out_list.append(fasta_tag.strip()+"."+str(i)+"\n")
            out_list.append(format_fasta(fasta_sub_seq))
            i+=1
    
    return ''.join(out_list)



def cleanfastafile(file_list,error_char,minimun_sequence_length):

    out_list = []

    for file_name in file_list:
        fasta_data = []
        fasta_tag = ""
        for line in open(file_name,'r'):
            
            if line != '' and line[0] == ">":
                if fasta_tag != "":
                        out_list.append(removeerrorcharsfromfasta(fasta_tag,
                      ''.join(fasta_data),
                      error_char,
                      minimun_sequence_length))
                fasta_tag = line
                fasta_data = []
            else:
                fasta_data.append(line)
        out_list.append(removeerrorcharsfromfasta(fasta_tag,
                      ''.join(fasta_data),
                      error_char,
                      minimun_sequence_length))      
        
        out_file = open(file_name+".noErrorChars",'w')
        out_file.write( ''.join(out_list) )
        out_file.close()
        out_list = []


file_list,error_char,minimun_sequence_length = getargs(desc="",ver='%prog 0.1')

cleanfastafile(file_list,error_char,minimun_sequence_length)






