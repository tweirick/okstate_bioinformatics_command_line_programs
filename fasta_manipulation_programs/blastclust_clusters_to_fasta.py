'''
blastclust_clusters_to_fasta.py
@author: Tyler Weirick
@created: 3/6/2013  
@language: Python 3.2
'''
#http://casp.rnet.missouri.edu/
#download/adam/sspro4.1/blast2.2.8/blastclust.txt
import argparse
from glob import glob

parser = argparse.ArgumentParser(description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter)    

parser.add_argument('--blastclust_cluster_files',
    help='Accepts cluster files output by Blastclust.')

parser.add_argument('--fasta_files_used_in_cluster_by_presidence',
help='''The fasta file(s) used to generate the cluster. If it is 
important to keep some sequences over others include them in the 
following format most_important.fasta,second_most.fasta,...''' 
,default=None)

parser.add_argument('--fasta_files_used_in_cluster_by_regex',
help='''I there is no presidence to the fastas you can describe them 
with a regex. Be sure to use quotes around your regex'''
,default=None)

parser.add_argument('--by_presidence',
                    help='T for presidence, F for ',
                    default=None)

args = parser.parse_args()
bc_c_files          = glob(args.blastclust_cluster_files)
fasta_cluster_pres  = list(
    str(args.fasta_files_used_in_cluster_by_presidence).split(","))
    
print(fasta_cluster_pres)

fasta_cluster_regex = args.fasta_files_used_in_cluster_by_regex

by_presidence = args.by_presidence


if fasta_cluster_pres == None and fasta_cluster_regex != None:
    fasta_file_list = fasta_cluster_regex
elif fasta_cluster_pres != None and fasta_cluster_regex == None:
    fasta_file_list = fasta_cluster_pres
else:
    print("ERROR:")
    exit()
    
if by_presidence == "T":
    #First covert the lists of fasta file name to lists of blastclust style name: full name\nseq dicts.
    
    fasta_file_dict_list = []
    
    for fasta_file_name in fasta_file_list:
        print(fasta_file_name)
        #Get fasta data.  
        #gi|213585708|ref|ZP_03367534.1|
        #>gi|213585708|ref|ZP_03367534.1| L-serine dehydratase [Salmonella enterica subsp. enterica serovar Typhi str. E98-0664]
        #Split after first space and strip > to get blastclust style name. 
        
        tmp_dict,seq_name = {}, None
        fasta_file = open(fasta_file_name,'r')
        while True:
            line = fasta_file.readline()
            if line == "" or line[0] == ">":
                assert line != "\n"
                if seq_name != None:
                    tmp_dict.update(
                        #Format key as Blastclust name 
                        #ex: gi|213585708|ref|ZP_03367534.1|   
                        {seq_name.split()[0].strip(">"):
                         #Store entire fasta entry as the value. 
                         seq_name+"\n"+"".join(tmp_seq_list)})
                
                #Hold name of fasta entry while sequence data is collected.
                seq_name = line.strip()
                tmp_seq_list = []
                #End of file readline() will return empty string. 
                if line == "":break
            else:
                #Sequence data and newlines  
                tmp_seq_list.append(line.strip())
        
        #Store dict for use in the 
        fasta_file_dict_list.append(tmp_dict)
        
    
    file_data = []
    file_cnt = {}
    
    fasta_file_dict_list = list(reversed(fasta_file_dict_list))
    
    for clust_file_name in bc_c_files:
        out_list = []
        for line in open(clust_file_name,"r"): 
            fasta_to_keep = ""
            keep_priority = -1
            seq_count=len(line.split())
            for seq_name in reversed(line.split()):
                seq_count-=1
                for i in range(0,len(fasta_file_dict_list)):
                    
                    if seq_name in fasta_file_dict_list[i] and i >= keep_priority:
                        fasta_to_keep = fasta_file_dict_list[i][seq_name]
                        keep_priority = i
                        
            if str(keep_priority) in file_cnt:
                file_cnt[str(keep_priority)]+=1
            else:
                file_cnt.update({str(keep_priority):1})
            assert fasta_to_keep != "", file_cnt
    
            out_list.append(fasta_to_keep)     
        print(file_cnt)
        file = open(clust_file_name+".faa","w")
        file.write("\n".join(out_list))
        file.close()
else:
    
    bc_c_files          = glob(args.blastclust_cluster_files)
    fasta_cluster_pres  = list(str(args.fasta_files_used_in_cluster_by_presidence).split(","))
    fasta_cluster_regex = args.fasta_files_used_in_cluster_by_regex
    by_presidence = args.by_presidence
    assert len(bc_c_files) == 1



