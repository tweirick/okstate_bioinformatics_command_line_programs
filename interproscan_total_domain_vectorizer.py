'''
@author: Tyler Weirick 
@date: 2013-08-21
===============================================================================
This program takes a set of interproscan tsv files are generates a vector 
that can describe the domains, evalues, start, and stop positions. 
 
===============================================================================
14086411a2cdf1c4cba63020e1622579        3418    Pfam    
PF09103 BRCA2, oligonucleotide/oligosaccharide-binding, domain 
1        2670    2799    7.9E-43 T       15-03-2013
'''

from glob import glob
import argparse
#=============================================================================
#                                Constants
#=============================================================================

DELIM = "\t"

#=============================================================================
#                                Functions
#=============================================================================

def addtomaindict(main_dict,sub_dict):
    """
    This function adds keys,value pairs not in the main dict to the main 
    dict. The main reason for this is to find to max occurences of domains 
    within the peptides being examined and make a list of all peptides 
    within the datasets. 
    """
    for sd_key in sub_dict:
        if not sd_key in main_dict:
            main_dict.update( {sd_key:sub_dict[sd_key]})
    return main_dict


def addvaluetomaindict(main_dict,sub_dict):
    for sd_key in sub_dict:
            if sd_key in main_dict:
                main_dict[sd_key] = sub_dict[sd_key]  
            else:
                print("ERROR")
    return main_dict


def interpro_tab_delim_line_to_vec(line,main_dict,make_base_vector=False):
    """
    Convert one tab delimited line to a dict representing a vector. 

    line  - the tab delimited line to convert 
    ac_id - There can be multiple instances of the same domain in a peptide,  
            so an underscore and count number are added to repeats. ac_id 
            will allow use of the ac_corredted for name.
    make_base_vector - Causes the values of the returned dict to be set to 
                       zero. This is for building the original 
    """
    MAX_PEPTIDE_LEN = 40000.0
    MAX_EVAL_EXP    = 1000.0
    sp_line       = line.split("\t")
    line_id       = sp_line[0] #Protein Accession (e.g. P51587)
    mda5_hash     = sp_line[1] #Sequence MD5 digest (e.g. 14086411a2cdf1c4cba63020e1622579)
    seq_len       = sp_line[2] #Sequence Length (e.g. 3418)
    domain_source = sp_line[3] #Analysis (e.g. Pfam / PRINTS / Gene3D)
    domain_ac     = sp_line[4] #Signature Accession (e.g. PF09103 / G3DSA:2.40.50.140)
    domain_desc   = sp_line[5] #Signature Description (e.g. BRCA2 repeat profile)
    domain_start  = sp_line[6] #Start location
    domain_stop   = sp_line[7] #Stop location
    domain_score  = sp_line[8] #Score - is the e-value of the match reported by member database method (e.g. 3.1E-52)
    domain_status = sp_line[9] #Status - is the status of the match (T: true)
    run_date      = sp_line[10] #Date - is the date of the run

    i=0
    base_domain_name = domain_ac
   
    while True: 
        i+=1
        if base_domain_name in main_dict:
            base_domain_name = domain_ac+"_"+str(i)
        else:
            break

    if make_base_vector:
        main_dict.update({base_domain_name        :0.0})
        main_dict.update({base_domain_name+"-start":0.0}) 
        main_dict.update({base_domain_name+"-stop" :0.0})
        main_dict.update({base_domain_name+"-score":0.0}) 
    else:
        seq_len = float(seq_len)
        f_normal_start = float(domain_start)/seq_len
        f_normal_stop  = float(domain_stop)/seq_len
        #40,000 is a few thousand more than the largest known protein titan. 
        f_normal_len      = seq_len/MAX_PEPTIDE_LEN
        #So should be safe from most applications. 
        assert seq_len <= MAX_PEPTIDE_LEN
        #SVM values are rounded to five decimal places so we cannot use them 
        #as is. The numerator will allways be in scientific notaton so the 
        #value will be 0 < val < 10 if we divide this by 10 we can round up 
        #or down to 0 or 1 and add that to the exponent. Finally divide by 
        #500, a value arbitrarily larger than the largest exponent possible 
        #for an evalue, but small enough that it will not be rounded out when
        #rounding to 5 decimal places. 
        #Get exponent ex: 1.3E-30
        if domain_score != "-":
            domain_score_exp  = float(domain_score.split("E-")[-1])
            #Get and round numerator
            domain_score_num  = round(float(domain_score.split("E-")[0])/10.0)
            norm_domain_score = (domain_score_exp+domain_score_num)/MAX_EVAL_EXP
            assert domain_score_exp+domain_score_num <= MAX_EVAL_EXP, domain_score_exp+domain_score_num
        else:
            norm_domain_score = 0.0

        main_dict.update({base_domain_name         :1.0})
        main_dict.update({base_domain_name+"-start":f_normal_start}) 
        main_dict.update({base_domain_name+"-stop" :f_normal_stop})
        main_dict.update({base_domain_name+"-score":norm_domain_score}) 

    return main_dict


def convertToSVMLigthFormat(descriptor_vector_dict,i):
    vector_list = []
    for dict_key in sorted(descriptor_vector_dict):
        vector_list.append(str(i)+":"+('{number:.{digits}f}'.format(
            number=(descriptor_vector_dict[dict_key]),digits=5)))
        i+=1
    return " ".join(vector_list)


def convertToNameValFormat(descriptor_vector_dict):
    vector_list = []
    #print( sorted( descriptor_vector_dict.keys() ) )
    for dict_key in sorted( descriptor_vector_dict.keys() ):
        vector_list.append(dict_key+":"+('{number:.{digits}f}'.format(
            number=(descriptor_vector_dict[dict_key]),digits=5)))
    return " ".join(vector_list)

def getargs(): 

    parser = argparse.ArgumentParser(
        description=open(__file__).read().split("'''")[1],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--file_set',help='''Accepts single files or regex used "" for regexes. ''',
                       default=None)
    parser.add_argument('--comma_delimited_file_names',
                       help='''Should be in EL_DESC_VAL format, 
                       takes presidence over vec_file_set if given.''',
                       default=None)
    args = parser.parse_args()
    file_glob                  = args.file_set
    comma_delimited_file_names = args.comma_delimited_file_names

    if file_glob != None:
        file_name_set =  glob(file_glob)
    if comma_delimited_file_names != None:
        file_name_set = comma_delimited_file_names.split(",")
    return file_name_set


def makesbasevector(file_glob):
    main_dict = {}
    last_line_peptide_id = None
    for file_name in file_glob:
        id_set = set()
        for line in open(file_name,'r'):
            peptide_id = line.split("\t")[0]
            id_set.add(peptide_id)

            if last_line_peptide_id == peptide_id:
                new_peptide_dict = interpro_tab_delim_line_to_vec(
                    line=line,
                    main_dict=new_peptide_dict,
                    make_base_vector=True)
            else:
                #This is a new peptide
                if last_line_peptide_id != None:
                    #Add dict contents to main vector dict. 
                    #out_vec = class_name+" "+convertToSVMLigthFormat(descriptor_vector_dict,i)
                    main_dict = addtomaindict(main_dict,new_peptide_dict)
                    #if "G3DSA:3.10.129.10" in line:
                    #    print(main_dict["G3DSA:3.10.129.10"])

                new_peptide_dict = {}
                new_peptide_dict = interpro_tab_delim_line_to_vec(
                    line=line,
                    main_dict=new_peptide_dict,
                    make_base_vector=True)
                

            last_line_peptide_id = peptide_id
        main_dict = addtomaindict(main_dict,new_peptide_dict)
    return main_dict


 
    
#=============================================================================
#                                Main Program
#=============================================================================

file_glob = getargs()

#Generate a dict containing the names of domains as keys. The max amount of 
#repeated domains found in a given pepdite will also be added with and
#underscore and the count appended to the end of the domain name. 
#ex: domain_name , domain_name_1
base_dict = makesbasevector(file_glob)
base_dict_len = len(base_dict)
#For reading tsv files. 
#Read through file once and extract 
last_line_peptide_id = None

for file_name in file_glob:
    #print(file_name)
    output_list = []    
    last_line_peptide_id = None
    sub_vec_dict = {} #main_dict.copy()
    class_name = file_name.split("/")[-1].split("_")[0]
    
    file = open(file_name,'r')
    while True:
        line = file.readline()
        peptide_id = line.split("\t")[0]
        if last_line_peptide_id != peptide_id and last_line_peptide_id != None:
            #An entry has been read completly, add it to the output list 
            #before re-instanciating the vec dict 
            #Map the sub dict to the main dict
            total_el_dict = base_dict.copy()                
            for sd_key in sub_vec_dict:
                if sd_key in base_dict:
                    total_el_dict[sd_key] = sub_vec_dict[sd_key]
                else:
                    print("ERROR:",file_name,sd_key)

            #total_el_dict = addvaluetomaindict( base_dict.copy(),sub_vec_dict,)
            assert len(total_el_dict) == base_dict_len
            #print(len(main_dict.keys())   ,len(total_el_dict.keys()))
            output_list.append( last_line_peptide_id+DELIM+convertToNameValFormat(  total_el_dict ) )
            #When no lines remain in file. 
            sub_vec_dict = {}
            if line == "": break    
         
        #Add the domain to the main vector.  
        #When set to False values will be added to the dict keys. 
        seq_vec_dict = interpro_tab_delim_line_to_vec(
                line=line,
                main_dict=sub_vec_dict,
                make_base_vector=False)
        #print(line.split()[0],len(seq_vec_dict),base_dict_len)
        assert len(seq_vec_dict) <= base_dict_len
        #if len(seq_vec_dict) == base_dict_len:
        #    print("WARNING main dict and sub dict are the same length, this is unlikly",file_name,line)
        #    #print(seq_vec_dict)
        last_line_peptide_id = peptide_id

    out_file = open(file_name+".domain.EL_DESC_VAL.vec",'w')
    out_file.write("\n".join(output_list))
    out_file.close()

