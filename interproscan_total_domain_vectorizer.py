"""
  
14086411a2cdf1c4cba63020e1622579        
3418    
Pfam    
PF09103 BRCA2, oligonucleotide/oligosaccharide-binding, domain 
1        
2670    
2799    
7.9E-43 T       
15-03-2013
"""
#P51587  14086411a2cdf1c4cba63020e1622579        3418    ProSiteProfiles PS50138 BRCA2 repeat profile.   1002    1036    0.0     T       18-03-2013      IPR002093       BRCA2 repeat    GO:0005515|GO:0006302
#P51587  14086411a2cdf1c4cba63020e1622579        3418    Gene3D  G3DSA:2.40.50.140    

from glob import glob
#P51587
#=============================================================================
#                                Constants
#=============================================================================



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
    MAX_EVAL_EXP    = 500.0
    

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
        if base_domain_name in new_peptide_dict:
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
            assert domain_score_exp+domain_score_num <= MAX_EVAL_EXP
        else:
            norm_domain_score = 0.0

        main_dict.update({base_domain_name         :1.0})
        main_dict.update({base_domain_name+"-start":f_normal_start}) 
        main_dict.update({base_domain_name+"-stop" :f_normal_stop})
        main_dict.update({base_domain_name+"-score":norm_domain_score}) 

    return main_dict

def addinfosourcestodict(input_dict,info_vals_dict):

    print()

def convertToSVMLigthFormat(descriptor_vector_dict,i):
    vector_list = []
    for dict_key in sorted(descriptor_vector_dict):
        vector_list.append(str(i)+":"+('{number:.{digits}f}'.format(
            number=(descriptor_vector_dict[dict_key]),digits=5)))
        i+=1
    return " ".join(vector_list)
#=============================================================================
#                                Main Program
#=============================================================================




#For reading tsv files. 
current_sequence_domain_dict_dict = {}
#Read through file once and extract 
total_domains_dict = {}
last_line_peptide_id = None
main_dict = {}
file_glob = glob("/home/tyler/Desktop/2013-7-17-15.38_inital_blastclusted_renamed_fastas_split_into_90_and_10_percent/*.tsv")#["test_proteins.fasta.tsv"]

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
            new_peptide_dict = {}
        last_line_peptide_id = peptide_id
    main_dict = addtomaindict(main_dict,new_peptide_dict)
    print(file_name,len(id_set))

    
#print(main_dict)
#output_dict = {}
#for key_el in sorted(main_dict.keys()):
 #   print(key_el)
    #output_dict.update( { key_el: 0.0 } )
    #for ac_key_el in sorted(main_dict[key_el].keys()):
    #    output_dict.update( { key_el+"-"+ac_key_el:str(main_dict[key_el][ac_key_el]) } )
#




for file_name in file_glob:
    output_list = []    
    last_line_peptide_id = None
    seq_vec_dict = main_dict.copy()
    class_name = file_name.split("/")[-1].split("_")[0]
    for line in open(file_name,'r'):

        peptide_id = line.split("\t")[0]

        if last_line_peptide_id == peptide_id: 
            seq_vec_dict = interpro_tab_delim_line_to_vec(
                line=line,
                main_dict=seq_vec_dict,
                make_base_vector=False)
        else:
            #This is a new peptide
            if last_line_peptide_id != None:
                output_list.append(class_name+" "+convertToSVMLigthFormat(seq_vec_dict,1) )
                #output_list.append(seq_vec_dict)
            seq_vec_dict = main_dict.copy()

        last_line_peptide_id = peptide_id
    output_list.append(class_name+" "+convertToSVMLigthFormat(seq_vec_dict,1) )
    out_file = open(file_name+"domain.vec",'w')
    out_file.write("\n".join(output_list))
    out_file.close()



