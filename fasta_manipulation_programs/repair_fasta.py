'''

'''
from glob import glob
import argparse

def getargs(ver='%prog 0.0'):

    parser = argparse.ArgumentParser(description='Take a blastclust cluster '+
             'file as input and remove all clusters from fasta file set.')    
    parser.add_argument('--file_set', 
                        #action='store_const',
                        #const=sum, 
                        #default=max,
                        help='')
    
    parser.add_argument('--file_suffix', 
                        #action='store_const',
                        #const=sum, 
                        default=".pruneBJXZ.fasta",
                        help='')
    

    parser.add_argument('--remove_over_x_percent', 
                        #action='store_const',
                        #const=sum, 
                        #default=max,
                        help='')
    args = parser.parse_args()
    
    return glob(args.file_set),args.file_suffix,args.remove_over_x_percent


def build_fasta_dict(input_file_name):
    
    #Make a dictionary from the fasta file used for input.
    fasta_dict     = {}
    temp_fasta_seq = []
    fasta_name     = ""
    
    input_fasta_count = 0
    
    for line in open(input_file_name,'r'):
        
        if ">" in line:
            input_fasta_count+=1
            if fasta_name != "":
                fasta_dict.update(
                    {fasta_name.strip():''.join(temp_fasta_seq)})
                temp_fasta_seq = []
            fasta_name = line.strip()
        else:
            temp_fasta_seq.append(line.strip())
    #Catch last entry
   
    fasta_dict.update({fasta_name:''.join(temp_fasta_seq)})   

    return fasta_dict,input_fasta_count

def invert_dict(fasta_dict):
    
    new_dict = {}
    
    for e in fasta_dict:
        new_dict.update({fasta_dict[e]:e})
        
    return new_dict
    
    
def buildnewfasta(new_dict,remove_over_x_percent):
    
    
    out_list = []
    for e in new_dict:
        #print(remove_over_x_percent)
        if remove_over_x_percent != None:
            #print("prune X")
            total_len = len(e)
            x_cnt = 0
            #This could probably be done with the count() function
            #but I have encountered problems before with large sets of text 
            #before when using some of the list functions. 
            #print(e)
            for aa in e:
                if aa.upper() == "B" or aa.upper() == "J" or aa.upper() == "X" or aa.upper() == "Z":
                   x_cnt+=1 
                   
            #print(float(x_cnt)/float(total_len),float(remove_over_x_percent))
            if float(x_cnt)/float(total_len) < float(remove_over_x_percent):    
                out_list.append(new_dict[e]+'\n'
                        +e+'\n')
            #else:
            #    print("!!!!!!!!!!!!!!!!!!!!")
        else:
            out_list.append(new_dict[e]+'\n'
                        +e+'\n')
    return out_list



#PRE_PSI-BLAST_52412/*catted_52412.faa
#file_set = glob("/home/TWeirick/FEATURE_GENERATING_PROGRAMS/40per_Sets/40per_all_catted.faa")#

file_set,file_suffix,remove_over_x_percent = getargs(ver='%prog 0.0')

for file_name in file_set:
    
    fasta_dict,input_fasta_count = build_fasta_dict(file_name)
    
    new_dict = invert_dict(fasta_dict)
    
    out_list = buildnewfasta(new_dict,remove_over_x_percent)
    
    print(file_name,str(input_fasta_count),str(len(out_list)))
    out_file = open(file_name+file_suffix,'w')
    out_file.write(''.join(out_list))
    out_file.close()
    
