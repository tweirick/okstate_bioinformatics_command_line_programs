'''
This will calculate pIs from amino acid fasta files. 
'''
from sys import hexversion
from glob import glob
py_version = hex(hexversion)


desc=open(__file__).read().split("'''")[1]
if py_version > "0x30200f0":

    import argparse

    def getargs(ver='%prog 0.0'):
        '''
        This function handles the command line arguments. 
        '''
        parser = argparse.ArgumentParser(
            #Get the head comments.
            description=desc,
            formatter_class=argparse.RawDescriptionHelpFormatter)    

        parser.add_argument('--file_set', 
            help='''Accepts single files or regex used "" for regexes ex: --file_set "*.faa" ''')

        args = parser.parse_args()
        sorted_file_glob = sorted(glob(args.file_set))

        return sorted_file_glob
else:

    from optparse import OptionParser

    def getargs(ver='%prog 0.0'):
        '''
        This function handles the command line arguments. 
        '''
        parser = OptionParser(description=desc)

        parser.add_option(
            '--file_set', 
            help='''Accepts single files or regex used "" for regexes ex: --file_set "*.faa" ''')

        options, args = parser.parse_args()

        sorted_file_glob = sorted( glob(options.file_set) )

        return sorted_file_glob




def peptideisoelectripoint(prot_sequence): 
    """
    @author: Tyler Weirick
    @date:   2013-6-26
    Naive calculation of isoelectric point. Based on information and 
    algorithms from http://isoelectric.ovh.org

    Input: An amino acid sequence with amino acids represented as single 
           letter charaters. Assumption is that data validation will be 
           done before this step so no checking for non-standard amino 
           acids, nucleic acid sequences, three letter codes, etc. will 
           be done. 
    Output: A float representing the isoelectric point of the given amino 
            acid. 
    Notes: I compared methods for counting amino acids. Using the built in 
    count function is much faster 
    
    Here are the results of a 100 itterations of the two methods 
    With count() function: 0.000475883483886718 s
    Itterative counting  : 0.011758089065551758 s

    Itterative counting
    C,D,E,H,K,R,Y = 0,0,0,0,0,0,0
    for aa in prot_sequence:
        if   aa == "C":C+=1
        elif aa == "D":D+=1
        elif aa == "E":E+=1
        elif aa == "H":H+=1
        elif aa == "K":K+=1
        elif aa == "R":R+=1
        elif aa == "Y":Y+=1

    This makes sense as this the count() function is most likly implemented in C. Hoever, 
    care should be taken when using on large strings. I don't expect such a large amino 
    acid could exist though. 
    """
    wikipedia_pKas = {
    "C-terminal":3.65,
    "N-terminal":8.2,
    "C":8.18,          #Cys, Cysteine
    "D":3.9,           #Asp, Aspartic acid
    "E":4.07,  #Glu, Glutamic acid
    "H":6.04,  #His, Histidine
    "K":10.54, #Lys, Lysine
    "R":12.48, #Arg, Arginine
    "Y":10.46  #Tyr, Tyrosine
    }

    pKa_d = wikipedia_pKas

    #Just in case. Make sure all characters are upper case.  
    prot_sequence = prot_sequence.upper()

    #Get the number of occurences of each 
    C = prot_sequence.count("C") #Cys, Cysteine
    D = prot_sequence.count("D") #Asp, Aspartic acid
    E = prot_sequence.count("E") #Glu, Glutamic acid
    H = prot_sequence.count("H") #His, Histidine
    K = prot_sequence.count("K") #Lys, Lysine
    R = prot_sequence.count("R") #Arg, Arginine
    Y = prot_sequence.count("Y") #Tyr, Tyrosine

    pH = 6.5 # Average pI 
    pHprev = 0.0
    pHnext = 14.0    
    max_error = 0.001    
    while True:
        QN1 = -1/(1+pow(10,(pKa_d["C-terminal"]-pH ))) #C-terminal charge
        QP2 =  1/(1+pow(10,(pH-pKa_d["N-terminal"])))  #N-terminal charge
        QN4 = -C/(1+pow(10,(pKa_d["C"]-pH)))  #C charge 
        QN2 = -D/(1+pow(10,(pKa_d["D"]-pH)))   #D charge
        QN3 = -E/(1+pow(10,(pKa_d["E"]-pH)))  #E charge
        QP1 =  H/(1+pow(10,(pH-pKa_d["H"])))  #H charge
        QP3 =  K/(1+pow(10,(pH-pKa_d["K"]))) #K charge
        QP4 =  R/(1+pow(10,(pH-pKa_d["R"]))) #R charge
        QN5 = -Y/(1+pow(10,(pKa_d["Y"]-pH))) #Y charge
        NQ = QN1 + QN2 + QN3 + QN4 + QN5 + QP1 + QP2 + QP3 + QP4         

        temp = pH
        if NQ < 0:
            pH = pH- ( (pH-pHprev)/2 )
            pHnext = temp
        elif NQ > 0:
            pH = pH- ( (pH-pHnext)/2 )
            pHprev = temp

        if pH-pHprev < max_error and pHnext-pH < max_error:
            break        

    return pH

file_list = getargs(ver='%prog 0.0')

for file_name in file_list: 
    fasta_file = open(file_name,'r')
    fasta_list = []
    while True: 
        line = fasta_file.readline()
    
        if line == "" or line[0] == ">":
            if fasta_list != []:        
                print( str(peptideisoelectripoint( "".join(fasta_list))) )
            if line == "":
                break
            else:
                print( line.strip()+"\t" ,end="")
            fasta_list = []
        else:    
            fasta_list.append(line.strip())
     















