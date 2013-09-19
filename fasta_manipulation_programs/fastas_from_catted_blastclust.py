'''
blastclust_clusters_to_fasta.py
@author: Tyler Weirick
@created: 3/6/2013  
@language: Python 3.2
@tags: blastclust fasta 

'''
#http://casp.rnet.missouri.edu/download/adam/sspro4.1/blast2.2.8/blastclust.txt
import argparse
import itertools
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


parser = argparse.ArgumentParser(description=getheadcomments(),formatter_class=argparse.RawDescriptionHelpFormatter)    

parser.add_argument('--blastclust_cluster_file',
    help='Accepts cluster files output by Blastclust.')
    
parser.add_argument('--fasta_files_used_in_cluster',
    help='The fasta file(s) used to generate the cluster. '+
    'If it is important to keep some sequences over others include them in the following format '+
     'most_important.fasta,second_most.fasta,...' ,default=None)

#Make data structure with amounts of sequences per class.
#Dict with name until first space minus > char at start, points to class or classes.  
#Read through clusters and make lists of seqs to retrieve from input. 

args = parser.parse_args()

cluster_file    = args.blastclust_cluster_file
fasta_file_list = sorted(list(glob(args.fasta_files_used_in_cluster) ))

print(cluster_file)
print(fasta_file_list)

output_fasta_dict = {}
for infilename in fasta_file_list:
    output_fasta_dict.update({infilename:[]})


class_members_count = {}
i=0
j=0
tmp_dict  = {}
for fasta_file_name in fasta_file_list:
    seq_name = None
    fasta_file = open(fasta_file_name,'r')
    entry_cnt = 0
    while True:
        line = fasta_file.readline()
        if line == "" or line[0] == ">":
            assert line != "\n"
            if seq_name != None:
                assert not fasta_file_name in tmp_dict
                tmp_dict.update(
                    #Format key as Blastclust name 
                    #ex: gi|213585708|ref|ZP_03367534.1|   
                    {
                     seq_name.split()[0].strip(">"):
                     #Store file name position 0 fasta data position 1  
                     [
                       fasta_file_name,
                       seq_name+"\n"+"".join(tmp_seq_list)
                     ]
                    }
          
                )
                if "LigJ.trainingdata.faa" == fasta_file_name:j+=1
                entry_cnt+=1
            #Hold name of fasta entry while sequence data is collected.
            seq_name = line.strip()
            tmp_seq_list = []
            #End of file readline() will return empty string. 
            if line == "":break
        else:
            #Sequence data and newlines  
            tmp_seq_list.append(line.strip())
            
    class_members_count.update({fasta_file_name:entry_cnt})
    print(fasta_file_name,entry_cnt)
    #Store dict for use in the 
    #fasta_file_dict_list.append(tmp_dict)



for line in open(cluster_file,'r'):
    lowest_seq_number = None
    #print(line)
    for seq_id in line.split():
        #Get the smallest entry
        #print(seq_id)
        file_or_origin = tmp_dict[seq_id][0]
        seqs_in_class = class_members_count[file_or_origin]
        
        if "LigJ.trainingdata.faa" == file_or_origin:i+=1

        if lowest_seq_number == None:
            lowest_seq_id = seq_id
            lowest_seq_number = seqs_in_class
            lowest_class      = file_or_origin
            lowest_fasta_seq  = tmp_dict[seq_id][1]         
        elif seqs_in_class < lowest_seq_number:
            #if len(output_fasta_dict[lowest_class]) > len(output_fasta_dict[file_or_origin]):
            lowest_seq_id = seq_id
            lowest_seq_number = seqs_in_class
            lowest_class      = file_or_origin
            lowest_fasta_seq  = tmp_dict[seq_id][1]
            
    output_fasta_dict[lowest_class].append(lowest_fasta_seq)
    
print(i,j)    
    
for e in output_fasta_dict:
    out_file = open(e+".blastcomb_faa",'w')
    out_file.write("\n".join(output_fasta_dict[e]))
    out_file.close()
    
     
