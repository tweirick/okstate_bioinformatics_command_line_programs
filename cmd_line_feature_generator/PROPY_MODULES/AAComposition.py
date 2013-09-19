# -*- coding: utf-8 -*-
"""
###############################################################################
The module is used for computing the composition of amino acids, dipetide and 
3-mers (tri-peptide) for a given protein sequence. You can get 8420 descriptors 
for a given protein sequence. You can freely use and distribute it. If you hava 
any problem, you could contact with us timely!
References:
[1]: Reczko, M. and Bohr, H. (1994) The DEF data base of sequence based protein
fold class predictions. Nucleic Acids Res, 22, 3616-3619.
[2]: Hua, S. and Sun, Z. (2001) Support vector machine approach for protein
subcellular localization prediction. Bioinformatics, 17, 721-728.
[3]:Grassmann, J., Reczko, M., Suhai, S. and Edler, L. (1999) Protein fold class
prediction: new methods of statistical classification. Proc Int Conf Intell Syst Mol
Biol, 106-112.
Authors: Dongsheng Cao and Yizeng Liang.
Date: 2012.3.27
Email: oriental-cds@163.com
###############################################################################
"""

import re
from math import log10

AALetter = ["A", "R", "N", "D", "C", "E", "Q", "G", "H", "I", "L", "K", "M", "F", "P", "S", "T", "W", "Y", "V"]
#############################################################################################
def CalculateAAComposition(ProteinSequence, multiply_decimal_percentage_by=1.0,
                           round_to_n_decimal_places=0):

        """
    ########################################################################
    Calculate the composition of Amino acids 
    
    for a given protein sequence.
    
    Usage:
    
    result=CalculateAAComposition(protein)
    
    Input: protein is a pure protein sequence.
    
    Output: result is a dict form containing the composition of 
    
    20 amino acids.
    ########################################################################
        """
        LengthSequence = len(ProteinSequence)
        Result = {}
        for i in AALetter:
            if round_to_n_decimal_places > 0:
                Result[i] = round(
                float(ProteinSequence.count(i))/LengthSequence*multiply_decimal_percentage_by,
                round_to_n_decimal_places)
            else:
                Result[i] = float(ProteinSequence.count(i)/LengthSequence)*multiply_decimal_percentage_by
        return Result
    
def CalculateSplitAAComposition(ProteinSequence,multiply_decimal_percentage_by=1.0,
                                round_to_n_decimal_places=0,split_size=20):
    assert len(ProteinSequence) > split_size*2,"WARNING: Peptide length is"+len(ProteinSequence)+". Peptide must be longer than 2*split_size."
    
    n_terminus =  ProteinSequence[:split_size]
    middle     =  ProteinSequence[split_size:-split_size]
    c_terminus =  ProteinSequence[-split_size:]
    
    LengthSequence = len(ProteinSequence)
    Result = {}
    for i in AALetter:
        if round_to_n_decimal_places > 0:
            Result["n_terminus"+i] = round(float(n_terminus.count(i))/LengthSequence*multiply_decimal_percentage_by,round_to_n_decimal_places)
        else:
            Result["n_terminus"+i] = float(n_terminus.count(i)/LengthSequence)*multiply_decimal_percentage_by
    for i in AALetter:
        if round_to_n_decimal_places > 0:
            Result["middle"+i] = round(float(middle.count(i))/LengthSequence*multiply_decimal_percentage_by,round_to_n_decimal_places)
        else:
            Result["middle"+i] = float(middle.count(i)/LengthSequence)*multiply_decimal_percentage_by
    for i in AALetter:
        if round_to_n_decimal_places > 0:
            Result["c_terminus"+i] = round(float(c_terminus.count(i))/LengthSequence*multiply_decimal_percentage_by,round_to_n_decimal_places)
        else:
            Result["c_terminus"+i] = float(c_terminus.count(i)/LengthSequence)*multiply_decimal_percentage_by  
              
    return Result

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
        print(fasta_sequence)
        
    #Ensure sequence is upper case so the sequence elements can be recognized. 
    fasta_sequence = fasta_sequence.upper()

    #You may want to use a number differenct that 25 that was found to be best for the paper cited.
    split_sequence = [fasta_sequence[0:terminal_len],
                      fasta_sequence[terminal_len:-terminal_len],
                      fasta_sequence[-terminal_len:]]

    #Start with space as a space is added after each vector element but not 
    #for first case. 
    out_vector_list = [" "]
    out_vector_dict = {}
    #Use this in case you want to compound this calculation with others in the future. 
    i = start_counting_from
    part_numb  = 1
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
            out_vector_dict.update({key+str(part_numb):float(aa_dic[key])/float(len(sub_sequence))})
            i+=1
        part_numb+=1
    out_vector_list.append("\n")
    return out_vector_dict


#############################################################################################
def CalculateDipeptideComposition(prot_seq,
                                  multiply_decimal_by=1,
                                  round_to_n_decimal_places=0):
    """
    ########################################################################
    Calculate the composition of dipeptidefor a given protein sequence.
    
    Usage: 
    
    result=CalculateDipeptideComposition(protein)
    
    Input: protein is a pure protein sequence.
    
    Output: result is a dict form containing the composition of 
    
    400 dipeptides.
    ########################################################################
    """
    
    seq_len = len(prot_seq)
    Result = {}
    
    for char1 in AALetter:
        for char2 in AALetter:
            dipeptide = char1+char2
            dipep_count = prot_seq.count(dipeptide)
            percentage = dipep_count/(seq_len-1)*multiply_decimal_by
            
            if round_to_n_decimal_places > 0:
                Result[dipeptide] = round(percentage,
                round_to_n_decimal_places)
            else:
                Result[dipeptide] = percentage
    return Result



#############################################################################################
def CalculateTripeptideComposition(prot_seq,
                                  multiply_decimal_by=1,
                                  round_to_n_decimal_places=0):
    """
    ########################################################################
    Calculate the composition of dipeptidefor a given protein sequence.
    
    Usage: 
    
    result=CalculateDipeptideComposition(protein)
    
    Input: protein is a pure protein sequence.
    
    Output: result is a dict form containing the composition of 
    
    400 dipeptides.
    ########################################################################
    """
    
    seq_len = len(prot_seq)
    Result = {}
    
    for char1 in AALetter:
        for char2 in AALetter:
            for char3 in AALetter:
                dipeptide = char1+char2+char3
                dipep_count = prot_seq.count(dipeptide)
                percentage = dipep_count/(seq_len-1)*multiply_decimal_by
                
                if round_to_n_decimal_places > 0:
                    Result[dipeptide] = round(percentage,
                    round_to_n_decimal_places)
                else:
                    Result[dipeptide] = percentage
    return Result



#############################################################################################
def Getkmers():
    """
    ########################################################################
    Get the amino acid list of 3-mers. 
    Usage: 
    result=Getkmers()
    Output: result is a list form containing 8000 tri-peptides.
    
    ########################################################################
    """
    kmers = list()
    for i in AALetter:
        for j in AALetter:
            for k in AALetter:
                kmers.append(i + j + k)
    return kmers

#############################################################################################
def GetSpectrumDict(proteinsequence):
    """
    ########################################################################
    Calcualte the spectrum descriptors of 3-mers for a given protein.
    
    Usage: 
    
    result=GetSpectrumDict(protein)
    
    Input: protein is a pure protein sequence.
    
    Output: result is a dict form containing the composition values of 8000
    
    3-mers.
    ########################################################################
    """
    result = {}
    kmers = Getkmers()
    for i in kmers:
        result[i] = len(re.findall(i, proteinsequence))
    return result

#############################################################################################
def CalculateAADipeptideComposition(ProteinSequence):

    """
    ########################################################################
    Calculate the composition of AADs, dipeptide and 3-mers for a 
    
    given protein sequence.
    
    Usage:
    
    result=CalculateAADipeptideComposition(protein)
    
    Input: protein is a pure protein sequence.
    
    Output: result is a dict form containing all composition values of 
    
    AADs, dipeptide and 3-mers (8420).
    ########################################################################
    """

    result = {}
    result.update(CalculateAAComposition(ProteinSequence))
    result.update(CalculateDipeptideComposition(ProteinSequence))
    result.update(GetSpectrumDict(ProteinSequence))

    return result

#############################################################################################

def get_residue_percentate(residue_str,ProteinSequence,entry_len):
    """
    This function takes a string of letters, a dictonary with single letter aa abreviateion keys 
    mapping to their occurence in a fasta entry and entry_len - an integer counting the total number of entires.
    in the fasta file.
    """
    residue_count = 0
    for aa in residue_str:
        residue_count+=ProteinSequence.count(aa)
    return float(residue_count)/float(entry_len)

def get_molecular_weight(fasta_sequence):
    #print(fasta_sequence)
    
    oxygen = 15.999
    hydrogen = 1.008
    
    fasta_sequence = fasta_sequence.upper()
    weight_dict = {
    "A":89.0935,"R":174.2017,"N":132.1184,"D":133.1032,"C":121.1590,
    "E":147.1299,"Q":146.1451,"G":75.0669,"H":155.1552,"I":131.1736,
    "L":131.1736,"K":146.1882,"M":149.2124,"F":165.1900,"P":115.1310,      
    "S":105.0930,"T":119.1197,"W":204.2262,"Y":181.1894,"V":117.1469    
    }
    
    total_weight = 0

    for i in range(0,len(fasta_sequence)):

        #aa_char in fasta_sequence:
        if fasta_sequence[i] in weight_dict:
            if i == 0:
                total_weight+=weight_dict[fasta_sequence[i]] - oxygen - hydrogen
            elif i == len(fasta_sequence)-1:
                total_weight+=weight_dict[fasta_sequence[i]] - hydrogen
            else:
                total_weight+=weight_dict[fasta_sequence[i]] - oxygen - hydrogen*2
        else:
            print("ERROR:",fasta_sequence[i],"not in standard amino acid dictionary.")
            print(fasta_sequence)
            print("EXITING")
    return total_weight#/len(fasta_sequence)



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



def PLPredPhysChem22(ProteinSequence):
    vector_dict = {}
    fasta_sequence = ProteinSequence.upper()
    seq_len = len(fasta_sequence)
    #1 Molecular weight       
    vector_dict.update({"a_molecular_weight":  log10(get_molecular_weight(fasta_sequence))/7.0})
    #2 Number of Amino Acids in the sequence. 
    vector_dict.update({"b_numb_of_aas_in_prot_seq": log10(float(seq_len))/5.0 })
    #1 % charged residues (DEKHR)
    vector_dict.update({"a_charged_residudes_DREKH":get_residue_percentate("DREKH",fasta_sequence,seq_len)})
    #2 % Hydrophilic and Neutral (ILV)
    vector_dict.update({"b_hydrophillic_and_neutral_NQSTY":get_residue_percentate("NQSTY",fasta_sequence,seq_len)})
    #3 % Basic polar or Positively charged H,K,R
    vector_dict.update({"c_basic_polar_or_positivly_charged_HKR":get_residue_percentate("HKR",fasta_sequence,seq_len)})
    #4 % Acidic polar or Negatively charged DE
    vector_dict.update({"d_acidic_or_negativly_charged_DE":get_residue_percentate("DE",fasta_sequence,seq_len)})
    #5 % Aliphatic A,G,I,L,V 
    vector_dict.update({"e_aliphatic_AGILV":get_residue_percentate("AGILV",fasta_sequence,seq_len)})
    #6 % Aromatic F,W,Y
    vector_dict.update({"f_aromatic_FWY":get_residue_percentate("FWY",fasta_sequence,seq_len)})
    #7 % Small T, D, N
    vector_dict.update({"g_small_DNT":get_residue_percentate("TDN",fasta_sequence,seq_len)})
    #8 % Tiny 
    vector_dict.update({"h_tiny_AGPS":get_residue_percentate("GASP",fasta_sequence,seq_len)})
    #9 % Large
    vector_dict.update({"i_large_FRWY":get_residue_percentate("FRWY",fasta_sequence,seq_len)})
    #10 % Hydrophobic (non-polar) and aromatic
    vector_dict.update({"j_hydrophobic_and_aromatic_WF":get_residue_percentate("WF",fasta_sequence,seq_len)})
    #11 % Hydrophobic (non-polar) and neutral
    vector_dict.update({"k_hydrophobic_and_neutral_ACGILMFPWV":get_residue_percentate("ACGILMFPWV",fasta_sequence,seq_len)})
    #12 % Amidic (contains amide group) N, Q
    vector_dict.update({"l_amidic_NQ":get_residue_percentate("NQ",fasta_sequence,seq_len)})
    #13 % Cyclic 
    vector_dict.update({"m_cyclic_P":get_residue_percentate("P",fasta_sequence,seq_len)})
    #14 % Hydroxylic 
    vector_dict.update({"n_hydroxylic_ST":get_residue_percentate("ST",fasta_sequence,seq_len)})
    #15 % Sulfur-containing 
    vector_dict.update({"o_contains_sulfer_CM":get_residue_percentate("CM",fasta_sequence,seq_len)})
    #16 % H-bonding
    vector_dict.update({"p_hbonding_CWNQSTYKRHDE":get_residue_percentate("CWNQSTYKRHDE",fasta_sequence,seq_len)})
    #17 % Acidic and their Amide
    vector_dict.update({"q_acidic_and_amide_DENQ":get_residue_percentate("DENQ",fasta_sequence,seq_len)})
    #18 % Ionizable
    vector_dict.update({"r_ionizable_DEHCYKR":get_residue_percentate("DEHCYKR",fasta_sequence,seq_len)})
    #19 %  Forms covalent cross-link (disulfide bond)
    vector_dict.update({"s_sulfer_bonding_C":get_residue_percentate("C",fasta_sequence,seq_len)})
    #20 % Theoretical PI
    vector_dict.update({"t_pI": peptideisoelectripoint(fasta_sequence)/14.0  })
    #1 Molecular weight       
    vector_dict.update({"u_molecular_weight":  log10(get_molecular_weight(fasta_sequence))/6.6021})
    #2 Number of Amino Acids in the sequence. 
    vector_dict.update({"v_numb_of_aas_in_prot_seq": log10(float(seq_len))/4.57978 })
    return vector_dict


def PLPredPhysChem22_nolog(ProteinSequence):
    vector_dict = {}
    fasta_sequence = ProteinSequence.upper()
    seq_len = len(fasta_sequence)
    #1 Molecular weight       
    vector_dict.update({"a_molecular_weight":  log10(get_molecular_weight(fasta_sequence))/7.0})
    #2 Number of Amino Acids in the sequence. 
    vector_dict.update({"b_numb_of_aas_in_prot_seq": log10(float(seq_len))/5.0 })
    #1 % charged residues (DEKHR)
    vector_dict.update({"a_charged_residudes_DREKH":get_residue_percentate("DREKH",fasta_sequence,seq_len)})
    #2 % Hydrophilic and Neutral (ILV)
    vector_dict.update({"b_hydrophillic_and_neutral_NQSTY":get_residue_percentate("NQSTY",fasta_sequence,seq_len)})
    #3 % Basic polar or Positively charged H,K,R
    vector_dict.update({"c_basic_polar_or_positivly_charged_HKR":get_residue_percentate("HKR",fasta_sequence,seq_len)})
    #4 % Acidic polar or Negatively charged DE
    vector_dict.update({"d_acidic_or_negativly_charged_DE":get_residue_percentate("DE",fasta_sequence,seq_len)})
    #5 % Aliphatic A,G,I,L,V 
    vector_dict.update({"e_aliphatic_AGILV":get_residue_percentate("AGILV",fasta_sequence,seq_len)})
    #6 % Aromatic F,W,Y
    vector_dict.update({"f_aromatic_FWY":get_residue_percentate("FWY",fasta_sequence,seq_len)})
    #7 % Small T, D, N
    vector_dict.update({"g_small_DNT":get_residue_percentate("TDN",fasta_sequence,seq_len)})
    #8 % Tiny 
    vector_dict.update({"h_tiny_AGPS":get_residue_percentate("GASP",fasta_sequence,seq_len)})
    #9 % Large
    vector_dict.update({"i_large_FRWY":get_residue_percentate("FRWY",fasta_sequence,seq_len)})
    #10 % Hydrophobic (non-polar) and aromatic
    vector_dict.update({"j_hydrophobic_and_aromatic_WF":get_residue_percentate("WF",fasta_sequence,seq_len)})
    #11 % Hydrophobic (non-polar) and neutral
    vector_dict.update({"k_hydrophobic_and_neutral_ACGILMFPWV":get_residue_percentate("ACGILMFPWV",fasta_sequence,seq_len)})
    #12 % Amidic (contains amide group) N, Q
    vector_dict.update({"l_amidic_NQ":get_residue_percentate("NQ",fasta_sequence,seq_len)})
    #13 % Cyclic 
    vector_dict.update({"m_cyclic_P":get_residue_percentate("P",fasta_sequence,seq_len)})
    #14 % Hydroxylic 
    vector_dict.update({"n_hydroxylic_ST":get_residue_percentate("ST",fasta_sequence,seq_len)})
    #15 % Sulfur-containing 
    vector_dict.update({"o_contains_sulfer_CM":get_residue_percentate("CM",fasta_sequence,seq_len)})
    #16 % H-bonding
    vector_dict.update({"p_hbonding_CWNQSTYKRHDE":get_residue_percentate("CWNQSTYKRHDE",fasta_sequence,seq_len)})
    #17 % Acidic and their Amide
    vector_dict.update({"q_acidic_and_amide_DENQ":get_residue_percentate("DENQ",fasta_sequence,seq_len)})
    #18 % Ionizable
    vector_dict.update({"r_ionizable_DEHCYKR":get_residue_percentate("DEHCYKR",fasta_sequence,seq_len)})
    #19 %  Forms covalent cross-link (disulfide bond)
    vector_dict.update({"s_sulfer_bonding_C":get_residue_percentate("C",fasta_sequence,seq_len)})
    #20 % Theoretical PI
    vector_dict.update({"t_pI": peptideisoelectripoint(fasta_sequence)/14.0  })
    #1 Molecular weight       
    vector_dict.update({"u_molecular_weight":  float(get_molecular_weight(fasta_sequence)/4000000.0) })
    #2 Number of Amino Acids in the sequence. 
    vector_dict.update({"v_numb_of_aas_in_prot_seq": float(seq_len)/38000.0 })
    return vector_dict


def PLPredPhysChem(ProteinSequence):
    """#####################################################################
    @author: Tyler Weirick
    @Created on: 2013-7-1 for PLpred
    ########################################################################
    """
    vector_dict = {}
    fasta_sequence = ProteinSequence.upper()
    seq_len = len(fasta_sequence)
    #1 % charged residues (DEKHR)
    vector_dict.update({"a_charged_residudes_DREKH":get_residue_percentate("DREKH",fasta_sequence,seq_len)})
    #2 % Hydrophilic and Neutral (ILV)
    vector_dict.update({"b_hydrophillic_and_neutral_NQSTY":get_residue_percentate("NQSTY",fasta_sequence,seq_len)})
    #3 % Basic polar or Positively charged H,K,R
    vector_dict.update({"c_basic_polar_or_positivly_charged_HKR":get_residue_percentate("HKR",fasta_sequence,seq_len)})
    #4 % Acidic polar or Negatively charged DE
    vector_dict.update({"d_acidic_or_negativly_charged_DE":get_residue_percentate("DE",fasta_sequence,seq_len)})
    #5 % Aliphatic A,G,I,L,V 
    vector_dict.update({"e_aliphatic_AGILV":get_residue_percentate("AGILV",fasta_sequence,seq_len)})
    #6 % Aromatic F,W,Y
    vector_dict.update({"f_aromatic_FWY":get_residue_percentate("FWY",fasta_sequence,seq_len)})
    #7 % Small T, D, N
    vector_dict.update({"g_small_DNT":get_residue_percentate("TDN",fasta_sequence,seq_len)})
    #8 % Tiny 
    vector_dict.update({"h_tiny_AGPS":get_residue_percentate("GASP",fasta_sequence,seq_len)})
    #9 % Large
    vector_dict.update({"i_large_FRWY":get_residue_percentate("FRWY",fasta_sequence,seq_len)})
    #10 % Hydrophobic (non-polar) and aromatic
    vector_dict.update({"j_hydrophobic_and_aromatic_WF":get_residue_percentate("WF",fasta_sequence,seq_len)})
    #11 % Hydrophobic (non-polar) and neutral
    vector_dict.update({"k_hydrophobic_and_neutral_ACGILMFPWV":get_residue_percentate("ACGILMFPWV",fasta_sequence,seq_len)})
    #12 % Amidic (contains amide group) N, Q
    vector_dict.update({"l_amidic_NQ":get_residue_percentate("NQ",fasta_sequence,seq_len)})
    #13 % Cyclic 
    vector_dict.update({"m_cyclic_P":get_residue_percentate("P",fasta_sequence,seq_len)})
    #14 % Hydroxylic 
    vector_dict.update({"n_hydroxylic_ST":get_residue_percentate("ST",fasta_sequence,seq_len)})
    #15 % Sulfur-containing 
    vector_dict.update({"o_contains_sulfer_CM":get_residue_percentate("CM",fasta_sequence,seq_len)})
    #16 % H-bonding
    vector_dict.update({"p_hbonding_CWNQSTYKRHDE":get_residue_percentate("CWNQSTYKRHDE",fasta_sequence,seq_len)})
    #17 % Acidic and their Amide
    vector_dict.update({"q_acidic_and_amide_DENQ":get_residue_percentate("DENQ",fasta_sequence,seq_len)})
    #18 % Ionizable
    vector_dict.update({"r_ionizable_DEHCYKR":get_residue_percentate("DEHCYKR",fasta_sequence,seq_len)})
    #19 %  Forms covalent cross-link (disulfide bond)
    vector_dict.update({"s_sulfer_bonding_C":get_residue_percentate("C",fasta_sequence,seq_len)})
    #20 % Theoretical PI
    vector_dict.update({"t_pI": peptideisoelectripoint(fasta_sequence)/14.0  })

    
    return vector_dict


def PLpredPhysChem20_no_normal(ProteinSequence):
    """#####################################################################
    @author: Tyler Weirick
    @Created on: 2013-7-1 for PLpred
    ########################################################################
    """
    vector_dict = {}
    fasta_sequence = ProteinSequence.upper()
    seq_len = 1
    #1 % charged residues (DEKHR)
    vector_dict.update({"a_charged_residudes_DREKH":get_residue_percentate("DREKH",fasta_sequence,seq_len)})
    #2 % Hydrophilic and Neutral (ILV)
    vector_dict.update({"b_hydrophillic_and_neutral_NQSTY":get_residue_percentate("NQSTY",fasta_sequence,seq_len)})
    #3 % Basic polar or Positively charged H,K,R
    vector_dict.update({"c_basic_polar_or_positivly_charged_HKR":get_residue_percentate("HKR",fasta_sequence,seq_len)})
    #4 % Acidic polar or Negatively charged DE
    vector_dict.update({"d_acidic_or_negativly_charged_DE":get_residue_percentate("DE",fasta_sequence,seq_len)})
    #5 % Aliphatic A,G,I,L,V 
    vector_dict.update({"e_aliphatic_AGILV":get_residue_percentate("AGILV",fasta_sequence,seq_len)})
    #6 % Aromatic F,W,Y
    vector_dict.update({"f_aromatic_FWY":get_residue_percentate("FWY",fasta_sequence,seq_len)})
    #7 % Small T, D, N
    vector_dict.update({"g_small_DNT":get_residue_percentate("TDN",fasta_sequence,seq_len)})
    #8 % Tiny 
    vector_dict.update({"h_tiny_AGPS":get_residue_percentate("GASP",fasta_sequence,seq_len)})
    #9 % Large
    vector_dict.update({"i_large_FRWY":get_residue_percentate("FRWY",fasta_sequence,seq_len)})
    #10 % Hydrophobic (non-polar) and aromatic
    vector_dict.update({"j_hydrophobic_and_aromatic_WF":get_residue_percentate("WF",fasta_sequence,seq_len)})
    #11 % Hydrophobic (non-polar) and neutral
    vector_dict.update({"k_hydrophobic_and_neutral_ACGILMFPWV":get_residue_percentate("ACGILMFPWV",fasta_sequence,seq_len)})
    #12 % Amidic (contains amide group) N, Q
    vector_dict.update({"l_amidic_NQ":get_residue_percentate("NQ",fasta_sequence,seq_len)})
    #13 % Cyclic 
    vector_dict.update({"m_cyclic_P":get_residue_percentate("P",fasta_sequence,seq_len)})
    #14 % Hydroxylic 
    vector_dict.update({"n_hydroxylic_ST":get_residue_percentate("ST",fasta_sequence,seq_len)})
    #15 % Sulfur-containing 
    vector_dict.update({"o_contains_sulfer_CM":get_residue_percentate("CM",fasta_sequence,seq_len)})
    #16 % H-bonding
    vector_dict.update({"p_hbonding_CWNQSTYKRHDE":get_residue_percentate("CWNQSTYKRHDE",fasta_sequence,seq_len)})
    #17 % Acidic and their Amide
    vector_dict.update({"q_acidic_and_amide_DENQ":get_residue_percentate("DENQ",fasta_sequence,seq_len)})
    #18 % Ionizable
    vector_dict.update({"r_ionizable_DEHCYKR":get_residue_percentate("DEHCYKR",fasta_sequence,seq_len)})
    #19 %  Forms covalent cross-link (disulfide bond)
    vector_dict.update({"s_sulfer_bonding_C":get_residue_percentate("C",fasta_sequence,seq_len)})
    #20 % Theoretical PI
    vector_dict.update({"t_pI": peptideisoelectripoint(fasta_sequence) })

    return vector_dict



def Calculate15PhysicoChemicalProperties(ProteinSequence):
    """
    ########################################################################
    @author: Tyler Weirick
    @Created on: 12/9/2011 Version 0.0 
    @language:Python 3.2
    @tags: physico-chemical physico chemcial properties composition vector 
    
    This program takes a set of fasta files as input and for each file in the 
    set outputs a vector file containg vectors correcsponding to the 
    physico-chemical properties of each fasta entry. The vector will be of the 
    same for used by COPid http://www.imtech.res.in/raghava/copid/help.html.
    It will contain:
        1  Molecular weight of protein in kilodaltons
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

        
    ########################################################################
    """
    vector_dict = {}

    fasta_sequence = ProteinSequence.upper()
    seq_len = len(fasta_sequence)
    #1 % Composition of charged residues (DEKHR)
    vector_dict.update({"c_charged_residude_comp":get_residue_percentate("DEKHR",fasta_sequence,seq_len)})
    #2 % Composition of aliphatic residues (ILV)
    vector_dict.update({"d_aliphatic_residude_comp":get_residue_percentate("ILV",fasta_sequence,seq_len)})
    #3  % Composition of Aromatic residues (FHWY)
    vector_dict.update({"e_aromatic_residude_comp":get_residue_percentate("FHWY",fasta_sequence,seq_len)})
    #4  % Composition of Polar residues (DERKQN)
    vector_dict.update({"f_polar_residude_comp":get_residue_percentate("DERKQN",fasta_sequence,seq_len)})
    #5  % Composition of Neutral residues (AGHPSTY)
    vector_dict.update({"g_neutral_residude_comp":get_residue_percentate("AGHPSTY",fasta_sequence,seq_len)})
    #6  % Composition of Hydrophobic residues (CVLIMFW)
    vector_dict.update({"h_hydrophobic_residude_comp":get_residue_percentate("CVLIMFW",fasta_sequence,seq_len)})
    #7  % composition of Positive charged residues (HKR)
    vector_dict.update({"i_pos_charge_residude_comp":get_residue_percentate("HKR",fasta_sequence,seq_len)})
    #8 % Composition of Negative charged residues (DE)
    vector_dict.update({"j_neg_charged_residude_comp":get_residue_percentate("DE",fasta_sequence,seq_len)})
    #9 % Composition of tiny residues (ACDGST)*
    vector_dict.update({"k_tiny_residude_comp":get_residue_percentate("ACDGST",fasta_sequence,seq_len)})
    #10 % Composition of Small residues (EHILKMNPQV)* and
    vector_dict.update({"l_small_residude_comp":get_residue_percentate("EHILKMNPQV",fasta_sequence,seq_len)})
    #11 % Composition of Large residues (FRWY)*.
    vector_dict.update({"m_large_residude_comp":get_residue_percentate("FRWY",fasta_sequence,seq_len)})
    #12 pI as float
    vector_dict.update({"n_pI": peptideisoelectripoint(fasta_sequence)/14.0 })
    #13 % Hydrophopbic and aromatic. set("CVLIMFW") & set("FHWY")
    vector_dict.update({"p_hydrophobic_and_aromatic":get_residue_percentate("WF",fasta_sequence,seq_len)}) 
    #14 Hydrophilic and acidic.  NQSTYDERHK
    vector_dict.update({"q_hydrphilic_and_acidic":get_residue_percentate("NQSTYDERHK",fasta_sequence,seq_len)})
    #15 Polar uncharged.
    vector_dict.update({"t_polar_uncharged":get_residue_percentate("NQSTY",fasta_sequence,seq_len)})
    
    return vector_dict



def Calculate18PhysicoChemicalProperties(ProteinSequence):
    """
    ########################################################################
    @author: Tyler Weirick
    @Created on: 12/9/2011 Version 0.0 
    @language:Python 3.2
    @tags: physico-chemical physico chemcial properties composition vector 
    
    This program takes a set of fasta files as input and for each file in 
    the set outputs a vector file containg vectors correcsponding to the 
    physico-chemical properties of each fasta entry.  
    Most of the elemenst come from COPid (
    http://www.imtech.res.in/raghava/copid/help.html.) and the rest are take 
    from "Identification of protein functions using a machine-learning 
    approach based on sequence-derived properties."

    The protein mass, length, and pI were modified so that values would 
    be normalized between 0 and 1. Normalizaiton has been shown to increase
    the accuracy of SVM classificaiton. See "Improved Support Vector Machine 
    Generalization Using Normalized Input Space"   

    pI is base on pH so division by 14.0 should be sufficent. 

    The upper bounds were determined for weight and length based on the 
    longest protein in TrEMBL and a the upper bound was a bit furhter beyond 
    the largest known value. A length of 40,000 was chosen. An mass of 
    40,000*204.23(mass of tryptophan) These could probably calculated with 
    (val-min)/(max-min) normalization, however, log10 give us a more 
    generalized idea of size and is might be better. Will need to compare 
    both.  
 
        1  Log10 of the Molecular weight of the protein divided by 7.0.
        2  Log10 of the number of amino acids divided by 5.0.
           
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
        14 theoretical pI divided by 14.0
        15 % composition of 2 Positive charged residues (KR)
        16 % Hydrophopbic and aromatic. (WF)
        17 % Hydrophilic and acidic.  (NQSTYDERHK)
        18 % Polar uncharged. (NQSTY)

        
    ########################################################################
    """
    vector_dict = {}

    fasta_sequence = ProteinSequence.upper()
    seq_len = len(fasta_sequence)
    #1 Molecular weight       
    vector_dict.update({"a_molecular_weight":  log10(get_molecular_weight(fasta_sequence))/7.0})
    #2 Number of Amino Acids in the sequence. 
    vector_dict.update({"b_numb_of_aas_in_prot_seq": log10(float(seq_len))/5.0 })
    #3 % Composition of charged residues (DEKHR)
    vector_dict.update({"c_charged_residude_comp":get_residue_percentate("DEKHR",fasta_sequence,seq_len)})
    #4 % Composition of aliphatic residues (ILV)
    vector_dict.update({"d_aliphatic_residude_comp":get_residue_percentate("ILV",fasta_sequence,seq_len)})
    #5  % Composition of Aromatic residues (FHWY)
    vector_dict.update({"e_aromatic_residude_comp":get_residue_percentate("FHWY",fasta_sequence,seq_len)})
    #6  % Composition of Polar residues (DERKQN)
    vector_dict.update({"f_polar_residude_comp":get_residue_percentate("DERKQN",fasta_sequence,seq_len)})
    #7  % Composition of Neutral residues (AGHPSTY)
    vector_dict.update({"g_neutral_residude_comp":get_residue_percentate("AGHPSTY",fasta_sequence,seq_len)})
    #8  % Composition of Hydrophobic residues (CVLIMFW)
    vector_dict.update({"h_hydrophobic_residude_comp":get_residue_percentate("CVLIMFW",fasta_sequence,seq_len)})
    #9  % composition of Positive charged residues (HKR)
    vector_dict.update({"i_pos_charge_residude_comp":get_residue_percentate("HKR",fasta_sequence,seq_len)})
    #10 % Composition of Negative charged residues (DE)
    vector_dict.update({"j_neg_charged_residude_comp":get_residue_percentate("DE",fasta_sequence,seq_len)})
    #11 % Composition of tiny residues (ACDGST)*
    vector_dict.update({"k_tiny_residude_comp":get_residue_percentate("ACDGST",fasta_sequence,seq_len)})
    #12 % Composition of Small residues (EHILKMNPQV)* and
    vector_dict.update({"l_small_residude_comp":get_residue_percentate("EHILKMNPQV",fasta_sequence,seq_len)})
    #13 % Composition of Large residues (FRWY)*.
    vector_dict.update({"m_large_residude_comp":get_residue_percentate("FRWY",fasta_sequence,seq_len)})
    #14 pI as float
    vector_dict.update({"n_pI":peptideisoelectripoint(fasta_sequence)/14.0})
    #15 % composition of Positive charged residues (KR)
    vector_dict.update({"o_pos_charge_residude_comp":get_residue_percentate("KR",fasta_sequence,seq_len)})
    #16 % Hydrophopbic and aromatic. set("CVLIMFW") & set("FHWY")
    vector_dict.update({"p_hydrophobic_and_aromatic":get_residue_percentate("WF",fasta_sequence,seq_len)}) 
    #17 Hydrophilic and acidic.  NQSTYDERHK
    vector_dict.update({"q_hydrphilic_and_acidic":get_residue_percentate("NQSTYDERHK",fasta_sequence,seq_len)})
    #18 Polar uncharged.
    vector_dict.update({"r_polar_uncharged":get_residue_percentate("NQSTY",fasta_sequence,seq_len)})
    
    return vector_dict




#############################################################################################
def CalculatePhysicoChemicalProperties(ProteinSequence, multiply_decimal_percentage_by=1.0,
                           round_to_n_decimal_places=0,approximate_normalization=False):

    """
    ########################################################################
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
    ########################################################################
    """
    
    max_len  = 15000.0
    min_len  = 1.0
    max_mass = 3749261.826
    min_mass = 1000.00
    
    fasta_sequence = ProteinSequence.upper()
    seq_len = len(fasta_sequence)
    #For residue percentage calculations
    vector_dict = {}
    #Molecular weight       
    #normal_molecular_weight =((get_molecular_weight(fasta_sequence) - min_mol_weight )/(max_mol_weight - min_mol_weight) )
    if approximate_normalization:
        vector_dict.update({"a_molecular_weight":(get_molecular_weight(fasta_sequence)-min_mass)/(max_mass-min_mass)})
    else:
        vector_dict.update({"a_molecular_weight":get_molecular_weight(fasta_sequence)  })
        
    #normal_seq_len =  ( (float(seq_len) - min_len )/(max_len - min_len) )   
    if approximate_normalization:
        vector_dict.update({"b_numb_of_aas_in_prot_seq": (float(seq_len)-min_len)/(max_len-min_len) })
    else:
        vector_dict.update({"b_numb_of_aas_in_prot_seq":float(seq_len)})
         
    #% Composition of charged residues (DEKHR)
    vector_dict.update({"c_charged_residude_comp":get_residue_percentate("DEKHR",fasta_sequence,seq_len)})
    #% Composition of aliphatic residues (ILV)
    vector_dict.update({"d_aliphatic_residude_comp":get_residue_percentate("ILV",fasta_sequence,seq_len)})
    #5  % Composition of Aromatic residues (FHWY)
    vector_dict.update({"e_aromatic_residude_comp":get_residue_percentate("FHWY",fasta_sequence,seq_len)})
    #6  % Composition of Polar residues (DERKQN)
    vector_dict.update({"f_polar_residude_comp":get_residue_percentate("DERKQN",fasta_sequence,seq_len)})
    #7  % Composition of Neutral residues (AGHPSTY)
    vector_dict.update({"g_neutral_residude_comp":get_residue_percentate("AGHPSTY",fasta_sequence,seq_len)})
    #8  % Composition of Hydrophobic residues (CVLIMFW)
    vector_dict.update({"h_hydrophobic_residude_comp":get_residue_percentate("CVLIMFW",fasta_sequence,seq_len)})
    #9  % composition of Positive charged residues (HKR)
    vector_dict.update({"i_pos_charge_residude_comp":get_residue_percentate("HKR",fasta_sequence,seq_len)})
    #10 % Composition of Negative charged residues (DE)
    vector_dict.update({"j_neg_charged_residude_comp":get_residue_percentate("DE",fasta_sequence,seq_len)})
    #11 % Composition of tiny residues (ACDGST)*
    vector_dict.update({"k_tiny_residude_comp":get_residue_percentate("ACDGST",fasta_sequence,seq_len)})
    #12 % Composition of Small residues (EHILKMNPQV)* and
    vector_dict.update({"l_small_residude_comp":get_residue_percentate("EHILKMNPQV",fasta_sequence,seq_len)})
    #13 % Composition of Large residues (FRWY)*.
    vector_dict.update({"m_large_residude_comp":get_residue_percentate("FRWY",fasta_sequence,seq_len)})



    return vector_dict








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
        print(fasta_sequence)
        

    #Ensure sequence is upper case so the sequence elements can be recognized. 
    fasta_sequence = fasta_sequence.upper()

    #You may want to use a number differenct that 25 that was found to be best for the paper cited.
    split_sequence = [fasta_sequence[0:terminal_len],
                      fasta_sequence[terminal_len:-terminal_len],
                      fasta_sequence[-terminal_len:]]

    #Start with space as a space is added after each vector element but not 
    #for first case. 
    out_vector_list = [" "]
    out_vector_dict = {}
    #Use this in case you want to compound this calculation with others in the future. 
    i = start_counting_from
    part_numb  = 1
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
            #print('{number:.{digits}f} '.format(number=(average_float),digits=5))
            out_vector_dict.update({key+str(part_numb):float(aa_dic[key])/float(len(sub_sequence))})
            i+=1
        part_numb+=1
    out_vector_list.append("\n")
    return out_vector_dict





#############################################################################################
if __name__ == "__main__":

    protein = "ADGCGVGEGTGQGPMCNCMCMKWVYADEDAADLESDSFADEDASLESDSFPWSNQRVFCSFADEDAS"

    AAC = CalculateAAComposition(protein)
    print(AAC)
    DIP = CalculateDipeptideComposition(protein)
    print(DIP)
    spectrum = GetSpectrumDict(protein)
    print(spectrum)
    res = CalculateAADipeptideComposition(protein)
    print(len(res))
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    

