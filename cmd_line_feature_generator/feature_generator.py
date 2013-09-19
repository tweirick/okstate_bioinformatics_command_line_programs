'''
@author: Tyler Weirick 
@Created on: 11/15/2012
@language:Python 3.2
@tags: descriptors vectors
This program can generate various descriptor vector types and composite 
descriptor types. It accepts a set of amino acid fasta files. Pass vectors as 
choises from the list below where a single vectors are separated by commas 
and composites separated by dashes.
'''

from sys import hexversion

#Propy modules.
from PROPY_MODULES import AAIndex
from PROPY_MODULES import AAComposition
from PROPY_MODULES import QuasiSequenceOrder
from PROPY_MODULES import PseudoAAC
from PROPY_MODULES import CTD
from PROPY_MODULES import Autocorrelation

#Other modules.
from time import gmtime, strftime

from glob import glob

#=============================================================================
#                                 Constants
#=============================================================================

VECTOR_TYPES = ["AACOMP","DIPEP","TRIPEP","SPLITAA","PSYCHM","PSYCHM15","PSYCHM18",
                "MoreauBroto","Moran","Geary",
                "C","T","D",
                "QuasiSequenceOrder","SequenceOrderCouplingNumberTotal",
                "PLPredPhysChem","PLpredPhysChem20_no_normal",
                "PLPredPhysChem22_nolog","PLPredPhysChem22"]


OUTPUT_TYPES = ["SVM_LIGHT", "SPACED_VALS", "EL_DESC_VAL"]

LINE_NAME_FORMAT_TYPES = ["CLASS_NAME", "FASTA_NAME", "NONE"]

#=============================================================================
#                                 Functions
#=============================================================================
py_version = hex(hexversion)

if py_version > "0x30200f0":

    import argparse

    def getargs(ver='%prog 0.0'):
        '''
        This function handles the command line arguments. 
        '''

        parser = argparse.ArgumentParser(
            #Get the head comments.
            description=open(__file__).read().split("'''")[1],
            formatter_class=argparse.RawDescriptionHelpFormatter)    

        parser.add_argument('--file_set', 
            help='''Accepts single files or regex used "" for regexes ex: --file_set "*.faa" ''')

        parser.add_argument('--vectors_to_generate', 
            help='''Sepatate sets of output with commas "," and link composite vectors 
            swith dashes "-". EX: --vectors_to_generate "AACOMP,SPLITAA-PSYCHM"
            The following vectors can be generated: '''+", ".join(VECTOR_TYPES)+".")

        parser.add_argument('--output_format', 
            help='''accepts: '''+", ".join(OUTPUT_TYPES)+".",
            default=OUTPUT_TYPES[0])

        parser.add_argument('--line_name_format', 
            help='''accepts: '''+", ".join(LINE_NAME_FORMAT_TYPES)+".",
            default=LINE_NAME_FORMAT_TYPES[0])
        
        parser.add_argument('--approximate_naturalization', 
            help='''Set to true for naturalization based on preset bound values.''',
            default=False)
        
        args = parser.parse_args()
        sorted_file_glob = sorted(glob(args.file_set))
        vecs_to_gen      = args.vectors_to_generate
        output_format    = args.output_format
        line_name_format = args.line_name_format
        approximate_naturalization = args.approximate_naturalization

        #Test for unsupported vector types.
        assert set(vecs_to_gen.replace("-",",").split(",")
        ).issubset(set(VECTOR_TYPES)),vecs_to_gen
        
        #Test for unsupported format types.
        assert set(output_format.replace("-",",").split(",")
        ).issubset(set(OUTPUT_TYPES)),output_format

        #Test for unsupported format types.
        assert set(line_name_format.replace("-",",").split(",")
        ).issubset(set(LINE_NAME_FORMAT_TYPES)),output_format

        print("Total input files     :",len(sorted_file_glob))
        print("Converting Files      :",sorted_file_glob)
        print("To vectors            :",vecs_to_gen)
        print("Using format          :",output_format)
        print("Using line name format:",output_format)
        return sorted_file_glob,vecs_to_gen,output_format,line_name_format,approximate_naturalization
else:

    from optparse import OptionParser

    def getargs(ver='%prog 0.0'):
        '''
        This function handles the command line arguments. 
        '''
        parser = OptionParser(
            description=open(__file__).read().split("'''")[1]
            )

        parser.add_option(
            '--file_set', 
            help='''Accepts single files or regex used "" for regexes ex: --file_set "*.faa" ''')

        parser.add_option('--vectors_to_generate', 
            help='''Sepatate sets of output with commas "," and link composite vectors 
            swith dashes "-". EX: --vectors_to_generate "AACOMP,SPLITAA-PSYCHM"
            The following vectors can be generated: '''+", ".join(VECTOR_TYPES)+".")

        parser.add_option('--output_format', 
            help='''accepts: '''+", ".join(OUTPUT_TYPES)+".",
            default=OUTPUT_TYPES[0])

        parser.add_option('--line_name_format', 
            help='''accepts: '''+", ".join(LINE_NAME_FORMAT_TYPES)+".",
            default=LINE_NAME_FORMAT_TYPES[0])
        
        parser.add_option('--approximate_naturalization', 
            help='''Set to true for naturalization based on preset bound values.''',
            default=False)
        
        args = parser.parse_args()
        sorted_file_glob = sorted(glob(args.file_set))
        vecs_to_gen      = args.vectors_to_generate
        output_format    = args.output_format
        line_name_format = args.line_name_format
        approximate_naturalization = args.approximate_naturalization

        #Test for unsupported vector types.
        assert set(vecs_to_gen.replace("-",",").split(",")
        ).issubset(set(VECTOR_TYPES)),vecs_to_gen
        
        #Test for unsupported format types.
        assert set(output_format.replace("-",",").split(",")
        ).issubset(set(OUTPUT_TYPES)),output_format

        #Test for unsupported format types.
        assert set(line_name_format.replace("-",",").split(",")
        ).issubset(set(LINE_NAME_FORMAT_TYPES)),output_format

        print("Total input files     :",len(sorted_file_glob))
        print("Converting Files      :",sorted_file_glob)
        print("To vectors            :",vecs_to_gen)
        print("Using format          :",output_format)
        print("Using line name format:",output_format)
        return sorted_file_glob,vecs_to_gen,output_format,line_name_format,approximate_naturalization


def convertToSVMLigthFormat(descriptor_vector_dict,i):
    vector_list = []
    for dict_key in sorted(descriptor_vector_dict):
        vector_list.append(str(i)+":"+('{number:.{digits}f}'.format(
            number=(descriptor_vector_dict[dict_key]),digits=5)))
        i+=1
    return " ".join(vector_list)


def convertToSpacedValuesFormat(descriptor_vector_dict):
    vector_list = []
    for dict_key in sorted(descriptor_vector_dict):
        vector_list.append(  (   '{number:.{digits}f}'.format(number=(descriptor_vector_dict[dict_key]),digits=5)   )  )
    return " ".join(vector_list)


def convertToElementDesciptionandValuesFormat(descriptor_vector_dict):
    vector_list = []
    for dict_key in sorted(descriptor_vector_dict):
        vector_list.append(dict_key+":"+('{number:.{digits}f}'.format(
            number=(descriptor_vector_dict[dict_key]),digits=5)))
    return " ".join(vector_list)


def getcompositevector(fasta_sequence,vec_comb_list,output_format,approximate_naturalization):
    """
    Returns one composite vector made from one fasta entry.
    """
    out_vector_list = []
    i=1
    tmp_list = []
    for vec_type in vec_comb_list.split("-"):

        if vec_type == "AACOMP":
            descriptor_vector_dict = AAComposition.CalculateAAComposition(fasta_sequence) 
        elif vec_type == "DIPEP":
            descriptor_vector_dict = AAComposition.CalculateDipeptideComposition(fasta_sequence)
        elif vec_type == "TRIPEP":
            descriptor_vector_dict = AAComposition.CalculateTripeptideComposition(fasta_sequence)
        elif vec_type == "SPLITAA":
            descriptor_vector_dict = AAComposition.CalculateSplitAAComposition(fasta_sequence)            
        elif vec_type == "PSYCHM":
            descriptor_vector_dict = AAComposition.CalculatePhysicoChemicalProperties(fasta_sequence,approximate_naturalization)
        elif vec_type == "PSYCHM15":
            descriptor_vector_dict = AAComposition.Calculate15PhysicoChemicalProperties(fasta_sequence)
        elif vec_type == "PSYCHM18":
            descriptor_vector_dict = AAComposition.Calculate18PhysicoChemicalProperties(fasta_sequence)
        elif vec_type == "PLPredPhysChem":
            descriptor_vector_dict = AAComposition.PLPredPhysChem(fasta_sequence)
        elif vec_type == "PLpredPhysChem20_no_normal":
            descriptor_vector_dict = AAComposition.PLpredPhysChem20_no_normal(fasta_sequence)
        elif vec_type == "PLPredPhysChem22_nolog":
            descriptor_vector_dict = AAComposition.PLPredPhysChem22_nolog(fasta_sequence)
        elif vec_type == "PLPredPhysChem22":
            descriptor_vector_dict = AAComposition.PLPredPhysChem22(fasta_sequence)
        elif vec_type == "MoreauBroto":
            descriptor_vector_dict = Autocorrelation.CalculateNormalizedMoreauBrotoAutoTotal(fasta_sequence)
        elif vec_type == "Moran":
            descriptor_vector_dict = Autocorrelation.CalculateMoranAutoTotal(fasta_sequence)
        elif vec_type == "Geary":
            descriptor_vector_dict = Autocorrelation.CalculateGearyAutoTotal(fasta_sequence)
        elif vec_type == "SequenceOrderCouplingNumberTotal":
            descriptor_vector_dict = QuasiSequenceOrder.GetSequenceOrderCouplingNumberTotal(fasta_sequence)
        elif vec_type == "QuasiSequenceOrder":
            descriptor_vector_dict = QuasiSequenceOrder.GetQuasiSequenceOrder(fasta_sequence)
        elif vec_type == "CTD":
            descriptor_vector_dict = CTD.CalculateCTD(fasta_sequence)
        elif vec_type == "C":
            descriptor_vector_dict = CTD.CalculateC(fasta_sequence)
        elif vec_type == "T":
            descriptor_vector_dict = CTD.CalculateT(fasta_sequence)
        elif vec_type == "D":
            descriptor_vector_dict = CTD.CalculateD(fasta_sequence)

        elif vec_type == "PseudoAAC":
            descriptor_vector_dict = PseudoAAC.GetPseudoAAC(
            fasta_sequence,AAP=[PseudoAAC._Hydrophobicity])
        elif vec_type == "APseudoAAC":
            #AAP=[PseudoAAC._Hydrophobicity] 
            descriptor_vector_dict = PseudoAAC.GetAPseudoAAC(fasta_sequence)  
                 
        else:
            print("ERROR:",vec_type,"is not a supported vector.")
            exit()

        #fasta_sequence,vec_comb,file_name
        #It is important to sort by name, as python dictionaries are unordered.
        if output_format == "SVM_LIGHT":
            tmp_list.append(convertToSVMLigthFormat(descriptor_vector_dict,i))
        elif output_format == "SPACED_VALS":
            tmp_list.append(convertToSpacedValuesFormat(descriptor_vector_dict))
        elif output_format == "EL_DESC_VAL":
            tmp_list.append(convertToElementDesciptionandValuesFormat(descriptor_vector_dict))
        else:
            print("ERROR: Unknown output type.",[output_format])
            exit()

        i = i+len(descriptor_vector_dict)
        
    return " ".join(tmp_list)
    

#=============================================================================
#                              Main Programs
#=============================================================================

#Get arguments from command line.
#Validation of input is also handled by this function.  
file_glob,vecs_to_generate,output_format,line_name_format,approximate_naturalization = getargs()
#file_glob - a list of file name or list of file names returned from a regex
#vectors_to_generate - List of vectors or compositve vectors to generate.
#output_format - The format vectors will be output in. 


for vector_name in vecs_to_generate.split(","):    
    for file_name in file_glob:
        vector_output_list = []
        #Get the base name for each class.
        vec_name = file_name.split(".")[0].upper()
        #Handle files in other directories. 
        if "/" in vec_name:vec_name = vec_name.split("/")[-1]

        #Read the fastas from the file and convert them one by one. 
        fasta_name = None
        fasta_file = open(file_name,'r')
        while True:             
            line = fasta_file.readline()
            if len(line) == 0 or line[0] == ">":

                if fasta_name != None:
                    fasta_sequence = "".join(fasta_data)        
                    #Generate vector and append to list for output.  
                    if   line_name_format == "CLASS_NAME":
                        title = vec_name+" "
                    elif line_name_format == "FASTA_NAME":
                        title = fasta_name+" "
                    elif line_name_format == "NONE":
                        title = ""
                    else:
                        print("ERROR: unknown line name type.",line_name_format)
                        exit()

                    vector_output_list.append(
                      title+getcompositevector(
                         fasta_sequence,
                         vector_name,
                         output_format,
                         approximate_naturalization
                      )
                    )
                    
                if len(line) == 0:break
                fasta_sequence = ""          #Redundancy, just in case.
                fasta_name     = line.strip()#Get new name
                fasta_data     = []          #Reset fasta data.
            else:
                fasta_data.append(line.strip())   
        fasta_file.close()

        #Output a vector file.
        output_file_name = file_name+"."+vector_name+"."+output_format+".vec"
        print(file_name,"->",output_file_name, strftime("%Y:%b:%d:%H:%M:%S", gmtime()))
        out_file = open(output_file_name,"w")
        out_file.write("\n".join(vector_output_list)+"\n")
        vector_output_list = []
        out_file.close()
    
