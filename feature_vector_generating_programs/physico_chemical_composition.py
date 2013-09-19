'''
@author: Tyler Weirick
@Created on: 12/9/2011 Version 0.0 
@language:Python 3.2
@tags: physico-chemical physico chemcial properties composition vector 

This program takes a set of fasta files as input and for each file in the 
set outputs a vector file containg vectors correcsponding to the 
physico-chemical properties of each fasta entry. The vector will be of the 
same for used by COPid http://www.imtech.res.in/raghava/copid/help.html.
It will contain:
    1  Molecular weight of protein $
    2  Number of amino acids in the protein sequnece $
    3  % Composition of charged residues (DEKHR)
    4  % Composition of aliphatic residues (ILV)
    5  % Composition of Aromatic residues (FHWY)
    6  % Composition of Polar residues (DERKQN)
    7  % Composition of Neutral residues (AGHPSTY)
    8  % Composition of Hydrophobic residues (CVLIMFW)
    9  % composition of Positive charged residues (HKR)
    10 % Composition of Negative charged residues (DE)
    11 % Composition of tiny residues (ACDGST)*
    12 % Composition of Small residues (EHILKMNPQV)* and
    13 % Composition of Large residues (FRWY)*.
'''

from glob import glob
use_arg = True

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


#For wider compatibility. optparse was depreciated in python 3.2
try:
    import argparse
    def getargs(ver='%prog 0.0'):
        parser = argparse.ArgumentParser(description=getheadcomments())    
        
        parser.add_argument('--file_set', 
                        help='')

        parser.add_argument('--set_type', 
                        default="",
                        help='')

        
        args = parser.parse_args()
        
        sorted_file_glob = sorted(glob(args.file_set))
            
        return sorted_file_glob,args.set_type
except:
    use_arg = False
    print("Error importing argparse. using optparse instead.")
    from optparse import OptionParser
    
    def getargs(ver='%prog 0.1'):
        """
        Gets file names for input and output.
        """    
        troubleShoot = False
        parser = OptionParser(version=ver,description=getheadcomments())
            
        parser.add_option("-i", "--file_set", 
            dest="file_set", 
            default="",
            help = "Input file set.")
        
        parser.add_option("-s", "--set_type", 
            dest="set_type", 
            default="",
            help = "This will be added at the start of vector lines.")
            
        (options, args) = parser.parse_args()
        if(troubleShoot):print(options);print(args)
                
        file_set     = options.file_set
        set_type         = options.set_type

        return sorted(glob(file_set)),set_type  


"""
AA 3-letter 1letter  side-chain-pol side-change-charge hydropath absorb
Aminoacid    Chemical formula    Molecular weight,g/mol
Alanine    Ala    A    nonpolar    neutral    1.8 Alanine    C3H7NO2    89.0935   
Arginine    Arg    R    polar    positive    −4.5      Arginine    C6H14N4O2    174.2017  
Asparagine    Asn    N    polar    neutral    −3.5        Asparagine    C4H8N2O3    132.1184
Aspartic acid    Asp    D    polar    negative    −3.5   Aspartate    C4H7NO4    133.1032      
Cysteine    Cys    C    polar    neutral    2.5    250    0.3 Cysteine    C3H7NO2S    121.1590
Glutamic acid    Glu    E    polar    negative    −3.5     Glutamate    C5H9NO4    147.1299    
Glutamine    Gln    Q    polar    neutral    −3.5        Glutamine    C5H10N2O3    146.1451
Glycine    Gly    G    nonpolar    neutral    −0.4  Glycine    C2H5NO2    75.0669       
Histidine    His    H    polar    positive(10%)  Histidine    C6H9N3O2    155.1552
neutral(90%)

−3.2    211    5.9
Isoleucine    Ile    I    nonpolar    neutral    4.5        Isoleucine    C6H13NO2    131.1736
Leucine    Leu    L    nonpolar    neutral    3.8        Leucine    C6H13NO2    131.1736
Lysine    Lys    K    polar    positive    −3.9      Lysine    C6H14N2O2    146.1882   
Methionine    Met    M    nonpolar    neutral    1.9        Methionine    C5H11NO2S    149.2124
Phenylalanine    Phe    F    nonpolar    neutral    2.8    257, 206, 188    0.2, 9.3, 60.0 Phenylalanine    C9H11NO2    165.1900 
Proline    Pro    P    nonpolar    neutral    −1.6  Proline    C5H9NO2    115.1310      
Serine    Ser    S    polar    neutral    −0.8        Serine    C3H7NO3    105.0930
Threonine    Thr    T    polar    neutral    −0.7     Threonine    C4H9NO3    119.1197    
Tryptophan    Trp    W    nonpolar    neutral    −0.9    280, 219    5.6, 47.0 Tryptophan    C11H12N2O2    204.2262
Tyrosine    Tyr    Y    polar    neutral    −1.3    274, 222, 193    1.4, 8.0, 48.0 Tyrosine    C9H11NO3    181.1894
Valine    Val    V    nonpolar    neutral    4.2 Valine    C5H11NO2    117.1469    

"""


    
    
    

def make_aacount_dict(fasta_sequence):
    """
    INPUT: 
    Returns a dictionary whose keys are comprised of the one letter 
    abbreviations of the twenty amino acids. The values corresponding to the 
    keys are the the number of that amino acid in the input string. 
    """
    aa_dic = {'A':0, 'C':0, 'D':0, 'E':0, 'F':0,
              'G':0, 'H':0, 'I':0, 'K':0, 'L':0,
              'M':0, 'N':0, 'P':0, 'Q':0, 'R':0,
              'S':0, 'T':0, 'V':0, 'W':0, 'Y':0}
    
    fasta_sequence = fasta_sequence.upper()
    file_error_bool = False
    #Count the amino acids. 
    for aa in fasta_sequence:
        if aa in aa_dic:
            aa_dic[aa]+=1
        else:
            if aa != "\n" and aa != "\t" and aa != " ":
                print("ERROR: unidentified char",aa,"in",file_name)
                print([fasta_sequence])
                if not file_error_bool:
                    file_error_bool = True
                    if file_name in exclusion_dict:
                        exclusion_dict[file_name]+=1
                    else:
                        exclusion_dict.update({file_name:1})
    return aa_dic


def get_residue_percentate(residue_str,aa_dic,entry_len):
    """
    This function takes a string of letters, a dictonary with single letter aa abreviateion keys 
    mapping to their occurence in a fasta entry and entry_len - an integer counting the total number of entires.
    in the fasta file.
    """
    residue_count = 0
    for aa in residue_str:
        residue_count+=aa_dic[aa]
    return float(residue_count)/entry_len


def get_molecular_weight(fasta_sequence):
    #print(fasta_sequence)
    fasta_sequence = fasta_sequence.upper()
    weight_dict = {
    "A":89.0935,"R":174.2017,"N":132.1184,"D":133.1032,"C":121.1590,
    "E":147.1299,"Q":146.1451,"G":75.0669,"H":155.1552,"I":131.1736,
    "L":131.1736,"K":146.1882,"M":149.2124,"F":165.1900,"P":115.1310,      
    "S":105.0930,"T":19.1197,"W":204.2262,"Y":181.1894,"V":117.1469    
    }
    
    total_weight = 0
    
    for aa_char in fasta_sequence:
        if aa_char in weight_dict:
            total_weight+=weight_dict[aa_char]
        else:
            print("ERROR:",aa_char,"not in standard amino acid dictionary.")
            print(fasta_sequence)
            print("EXITING")
    return total_weight#/len(fasta_sequence)
        
        
    
def physiochemical(fasta_sequence,file_name,max_mol_weight,min_mol_weight,max_len,min_len):
    global exclusion_dict
    #print(fasta_sequence)
    """
    1  Molecular weight of protein $
    2  Number of amino acids in the protein sequnece $
    3  % Composition of charged residues (DEKHR)
    4  % Composition of aliphatic residues (ILV)
    5  % Composition of Aromatic residues (FHWY)
    6  % Composition of Polar residues (DERKQN)
    7  % Composition of Neutral residues (AGHPSTY)
    8  % Composition of Hydrophobic residues (CVLIMFW)
    9  % composition of Positive charged residues (HKR)
    10 % Composition of Negative charged residues (DE)
    11 % Composition of tiny residues (ACDGST)*
    12 % Composition of Small residues (EHILKMNPQV)* and
    13 % Composition of Large residues (FRWY)*.
    """
    set_of_standard_amino_acids = set("ARNDCEQGHILKMFPSTWYV")
    
    fasta_sequence = fasta_sequence.upper()
    
    set_of_amino_acids_in_fasta = set(fasta_sequence)
    
    if set_of_standard_amino_acids >= set_of_amino_acids_in_fasta:
        
        seq_len = len(fasta_sequence)
        
        #For residue percentage calculations
        aa_dic = make_aacount_dict(fasta_sequence)
        out_list = []
        vector_dict = {}
               
        #Molecular weight       
        normal_molecular_weight =((get_molecular_weight(fasta_sequence) - min_mol_weight )/
                                   (max_mol_weight - min_mol_weight) )
        vector_dict.update({"a_molecular_weight":normal_molecular_weight })
        normal_seq_len =  ( (float(seq_len) - min_len )/
                                   (max_len - min_len) )    
        vector_dict.update({"b_numb_of_aas_in_prot_seq":float(normal_seq_len)})
        #% Composition of charged residues (DEKHR)
        vector_dict.update({"c_charged_residude_comp":get_residue_percentate("DEKHR",aa_dic,seq_len)})
        #% Composition of aliphatic residues (ILV)
        vector_dict.update({"d_aliphatic_residude_comp":get_residue_percentate("ILV",aa_dic,seq_len)})
        #5  % Composition of Aromatic residues (FHWY)
        vector_dict.update({"e_aromatic_residude_comp":get_residue_percentate("FHWY",aa_dic,seq_len)})
        #6  % Composition of Polar residues (DERKQN)
        vector_dict.update({"f_polar_residude_comp":get_residue_percentate("DERKQN",aa_dic,seq_len)})
        #7  % Composition of Neutral residues (AGHPSTY)
        vector_dict.update({"g_neutral_residude_comp":get_residue_percentate("AGHPSTY",aa_dic,seq_len)})
        #8  % Composition of Hydrophobic residues (CVLIMFW)
        vector_dict.update({"h_hydrophobic_residude_comp":get_residue_percentate("CVLIMFW",aa_dic,seq_len)})
        #9  % composition of Positive charged residues (HKR)
        vector_dict.update({"i_pos_charge_residude_comp":get_residue_percentate("HKR",aa_dic,seq_len)})
        #10 % Composition of Negative charged residues (DE)
        vector_dict.update({"j_neg_charged_residude_comp":get_residue_percentate("DE",aa_dic,seq_len)})
        #11 % Composition of tiny residues (ACDGST)*
        vector_dict.update({"k_tiny_residude_comp":get_residue_percentate("ACDGST",aa_dic,seq_len)})
        #12 % Composition of Small residues (EHILKMNPQV)* and
        vector_dict.update({"l_small_residude_comp":get_residue_percentate("EHILKMNPQV",aa_dic,seq_len)})
        #13 % Composition of Large residues (FRWY)*.
        vector_dict.update({"m_large_residude_comp":get_residue_percentate("FRWY",aa_dic,seq_len)})
        
        i=1
        for vd_el in sorted(list(vector_dict.keys())):
            out_list.append(str(i)+":"+'{number:.{digits}f}'.format(number=vector_dict[vd_el],digits=5))
            i+=1
        
        return " ".join(out_list) 





def convertotosvm(file_name,set_type,max_mol_weight,min_mol_weight,max_len,min_len):
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
                fasta_sequence = ''.join(fasta_data)
                set_of_standard_amino_acids = set("ARNDCEQGHILKMPHYSICO-CHEM_ORIGNAL_SPLIT_VECTORSFPSTWYV")
                
                fasta_sequence = fasta_sequence.upper()
                
                set_of_amino_acids_in_fasta = set(fasta_sequence)
                
                if set_of_standard_amino_acids >= set_of_amino_acids_in_fasta:
                    
                     seq_len = len(fasta_sequence)
                     SVM_vector = set_type+" "+physiochemical(''.join(fasta_data),file_name,max_mol_weight,min_mol_weight,max_len,min_len )+'\n' 
                     out_data.append(SVM_vector)
                else:
                    print("ERROR: Characters not in 20 standar amino acids detected.")
                    print(fasta_sequence)

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
    SVM_vector = set_type+" "+physiochemical(''.join(fasta_data),file_name,max_mol_weight,min_mol_weight,max_len,min_len )+'\n' 
    out_data.append(SVM_vector)
    #print(out_data)
    return out_data



def getmin(current_min,new_val):
    if current_min != None:
        if current_min > new_val:
            return new_val
        return current_min
    return new_val

def getmax(current_max,new_val):
    if current_max != None:
        if current_max < new_val:
            return new_val
        return current_max
    return new_val

def getmaxandminvalues(file_name,max_mol_weight,min_mol_weight,max_len,min_len):
    
    fasta_name = ''
    fasta_data = []
    
    set_of_standard_amino_acids = set("ARNDCEQGHILKMFPSTWYV")
    

    


        
    for line in open(file_name,"r"):

        if line[0] == '>':
            #If the start of a fasta entry enter data 
            if fasta_name != '':
                #Build fasta string
                tmp_fasta_seq = ''.join(fasta_data)
                #Operations for molecular weight.
                tmp_fasta_seq = tmp_fasta_seq.upper()
                set_of_amino_acids_in_fasta = set(tmp_fasta_seq)
        
                if set_of_standard_amino_acids >= set_of_amino_acids_in_fasta:
                
                    tmm_mol_weight = get_molecular_weight(tmp_fasta_seq) 
                    max_mol_weight = getmax(max_mol_weight,tmm_mol_weight)
                    min_mol_weight = getmin(min_mol_weight,tmm_mol_weight)
                    #Operations for sequence length.
                    tmp_len = len(tmp_fasta_seq)
                    max_len = getmax(max_len,tmp_len)
                    min_len = getmin(min_len,tmp_len)
                    
                    fasta_data = []
                    fasta_name = line
                else:
                    print("ERROR: Characters not in 20 standar amino acids detected.")
                    print(tmp_fasta_seq)
    
            else:
                fasta_name = line    
        else:
            fasta_data.append(line.strip())
    
    #Add data from final fasta entry. As there is no '>' char to trigger it's
    #addition. 
    #Build fasta string
    tmp_fasta_seq = ''.join(fasta_data)
    #Operations for molecular weight.
    tmp_fasta_seq = tmp_fasta_seq.upper()
    set_of_amino_acids_in_fasta = set(tmp_fasta_seq)

    if set_of_standard_amino_acids >= set_of_amino_acids_in_fasta:
    
        tmm_mol_weight = get_molecular_weight(tmp_fasta_seq) 
        max_mol_weight = getmax(max_mol_weight,tmm_mol_weight)
        min_mol_weight = getmin(min_mol_weight,tmm_mol_weight)
        #Operations for sequence length.
        tmp_len = len(tmp_fasta_seq)
        max_len = getmax(max_len,tmp_len)
        min_len = getmin(min_len,tmp_len)
        
        fasta_data = []
        fasta_name = line
    else:
        print("ERROR: Characters not in 20 standar amino acids detected.")
        print(tmp_fasta_seq)

    return max_mol_weight,min_mol_weight,max_len,min_len



#convertotosvm()

#for e in convertotosvm("/home/TWeirick/test_fast.faa",""):
#    print(e,end="")

#Normalize non-percentage based all should be betwee 0 and 1
#use_arg


#file_glob,set_type,output_file_name = getargs()
max_mol_weight,min_mol_weight,max_len,min_len = None,None,None,None

file_glob,set_type = getargs()



for file_name in file_glob:
    max_mol_weight,min_mol_weight,max_len,min_len = getmaxandminvalues(
                    file_name,max_mol_weight,min_mol_weight,max_len,min_len)

#print(max_mol_weight,min_mol_weight,max_len,min_len)




for file_name in file_glob:
     
    if set_type == "":
        #Use first part of file name 
        set_type = file_name.split(".")[0]
        svm_data = convertotosvm(file_name,set_type,max_mol_weight,min_mol_weight,max_len,min_len)
        set_type = ""
    else:
        #Use user specified.
        svm_data = convertotosvm(file_name,set_type,max_mol_weight,min_mol_weight,max_len,min_len)
    
    output_file_name = file_name+".phychm.vec" 
    
    #print(svm_data)
    print(output_file_name,len(svm_data))
    out_file = open(output_file_name,'w')
    out_file.write(''.join(svm_data))
    out_file.close()


#for name  in sorted(list(exclusion_dict)):
#    print(name,exclusion_dict[name])







