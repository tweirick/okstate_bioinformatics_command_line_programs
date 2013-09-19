'''
convert_GI_or_Assesion_to_fasta.py
@author: Tyler Weirick
@Created on: 3/23/2012 Version 0.0 
@language:Python 3.2
@tags: PSI-blast psi blast 

This program used retirive the corresponding fasta files of GI or accesion 
numbers contained in a flat text file with one entry per line from ncbi-utils.

'''

from html.parser import HTMLParser
import urllib.request
import glob
from optparse import OptionParser

#http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id=YP_001511242.1,YP_001505974.1&rettype=gi
#http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id=
#&rettype=gi
#YP_001511242.1
#file_regex="\\Users\Tyler\Desktop\ligninases\FLOy Stuff\FOLy_UI_FILES\*"
#file_glob = glob.glob(file_regex)



def getargs(ver='%prog 0.2'):
    """
    This function handles command line input for the program via the optparse 
    library
    """
    
    #Gets description from comments at the top of program.
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
    
    troubleShoot = False
    parser = OptionParser(version=ver,description=desc)
    
    #@todo: OptionParser is depreciated in Python 3.2. 
    #Need to move to the new style of parser. 
    parser.add_option("-i", "--input_reg_ex", 
                      dest="psi_blast_name", 
                      default="False",
                      help = "A file name or regular expression"+ 
                             "for psi-blast output.")

    parser.add_option("-o", "--out_directory_path", 
                      dest="out_directory_path", 
                      default="",
                      help = "If not used will create files in working "+ 
                      "directory i.e. the directory the script is in,"+
                      " if used will create files in specified"+ 
                      "directory")

    parser.add_option("-f", "--file_suffix", 
                      dest="file_suffix", 
                      default=".fasta",
                      help = "If not used will create files in working "+ 
                      "directory i.e. the directory the script is in,"+
                      " if used will create files in specified"+ 
                      "directory")

    (options, args) = parser.parse_args()
    if(troubleShoot):print(options);print(args)
            
    file_list = glob.glob(options.psi_blast_name) 
    out_directory_path = options.out_directory_path
    file_suffix = options.file_suffix
     
    #print(file_list) 
    #print(out_directory_path) 
    #print(file_suffix)
    
    return file_list,out_directory_path,file_suffix

#=============================================================================
# Start Main Program
#=============================================================================

#file_list,out_directory_path,file_suffix = getargs(ver='%prog 0.2')

file_list = glob.glob("LO1_uniprot_and_foly.fasta_psi-blast_e1e-40_j3_dnr.3.20.2012.GI_fasta_errors.txt")
out_directory_path = '' 
file_suffix = '.faa'


NAME_OF_FILE_WITH_UIS = "out_ui.txt"
file_suffix = ".from_psi-blast"+file_suffix #Need to fix in the future
OUT_ERROR_FILE_NAME = "_fasta_errors.txt"
DIGITS = "0123456789"
seq_name = ""

HTML_HEAD = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id='
HTML_TAIL = '&rettype=fasta'
list_to_file = []

for file_name in file_list:

        out_list       = []
        error_out_list = []
    
        try:#If no errors in entry will work 
            for line in open(file_name):
               #To fix bug in psi-blast parsing script where omitted entires are
               #ommited but a blank line is still added. 
               if line.strip != "":
                   out_list.append(line.strip()+",")
               
               out_str = ''.join(out_list)
               try:
                    if out_str[-1] == ',':
                        out_str = out_str[:-1]
               except:
                    print("length error")
                    print([file_name])
                    print([out_str])
                    
                
            url = HTML_HEAD + out_str + HTML_TAIL
            response = urllib.request.urlopen(url)
            source = response.read().decode() 
            
            out_file = open(out_directory_path+file_name+file_suffix,'w')
            out_file.write(source)
            out_file.close()
            
        except:
            out_list       = []
            error_out_list = []
            print("Oops, something is wrong with the url build from all entries, converting to entry by entry mode.")
            for line in open(file_name):
                
                try:
                    url = HTML_HEAD + line.strip() + HTML_TAIL
                    response = urllib.request.urlopen(url)
                    source = response.read().decode() 
                    out_list.append(source)       
                except:
                    error_out_list.append(line)

            out_file = open(out_directory_path+file_name+file_suffix,'w')
            out_file.write(''.join(out_list))
            out_file.close()
            
            error_file = open(out_directory_path+file_name+OUT_ERROR_FILE_NAME,'w')
            error_file.write(''.join(error_out_list))
            error_file.close()
            


