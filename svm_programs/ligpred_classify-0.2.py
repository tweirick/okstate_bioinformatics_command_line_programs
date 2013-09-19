'''
run_svm_learn.py
@author: Tyler Weirick
@Created on: 6/18/2012 Version 0.0 
@language:Python 3.2
@tags: svm classify local 
This program will classify a set of fasta files according to the model
files available
Input : fasta
Output: classifications by class. 
'''

from glob import glob
import argparse,tempfile,subprocess,re,os

from time import time

import AAIndex
import CTD
import AAComposition      as AAC
import QuasiSequenceOrder as SQO
import PseudoAAC          as PAAC
import Autocorrelation    as AUTOC

#=============================================================================
#                               Constants
#=============================================================================
#Folder where the model files are stored. Used by a glob to get a list 
#of model files. 
MODEL_FILES_PATH = "MODEL_FILES"

#=============================================================================
#                               Classes  
#=============================================================================

class DescriptorVector():    
    def __init__(self,vec_name,vec_type,vec_coords_str=False):
        self.unvectorizable = "unvectorizable"
        self.seq_name = vec_name.strip().replace(",",".")
        self.vec_type = vec_type
        #For dealing with illegal chars
        if vec_coords_str:
            self.vec_coords_str = vec_coords_str
        else:
            self.vec_coords_str = self.unvectorizable
        self.pred_dict = {}
        
    def getclassificationvec(self):
        if self.vec_coords_str == self.unvectorizable:
            return self.unvectorizable
        else:
            return "0 "+self.vec_coords_str

    def addpredicition(self,pred_model,pred_val):
        self.pred_dict.update({pred_model:pred_val})

    def getprediction(self):
        max_val_class = max(self.pred_dict, key=self.pred_dict.get)
        
        if self.pred_dict[max_val_class] > 0:
            return max_val_class
        else:
            return "UNKNOWN"
    
    def getpredictionvalues(self,join_char=","):
        out_list = []
        for dict_el in sorted(self.pred_dict):
            out_list.append(self.pred_dict[dict_el])
        return join_char.join([str(x) for x in out_list])
    
    def getpredclassandweight(self):
        z =  sorted(self.pred_dict, key=self.pred_dict.get) 
        max_val = self.pred_dict[z[-1]]
        min_val = self.pred_dict[z[0]]
        normal_1st = (self.pred_dict[z[-1]] - min_val)/(max_val - min_val)
        normal_2nd = (self.pred_dict[z[-2]] - min_val)/(max_val - min_val)
        if max_val > 0:
            return [z[-1],normal_1st-normal_2nd]
        else:
            return ["UNKNOWN",0.0]
    
    
    

        
        
        
#=============================================================================
#                               Functions 
#=============================================================================


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


def getargs(ver='%prog 0.0'):
    parser = argparse.ArgumentParser(description=getheadcomments())    
    parser.add_argument('--file_set',
                        help='Takes a string or regex (use quotes for regex).')
    #parser.add_argument('--model_files',default="MODEL_FILES",help='Takes a set of svm_light model files to use in classification.')
    possible_models = []
    for file_name in glob("MODEL_FILES/*"):
        model_re = re.compile(r'(?P<model>\.[\w \-* \w]+\.5f\.vec_)')
        ms = model_re.search(file_name)
        if ms:
            model_type = ms.group('model').split(".")[1]
            if not model_type in possible_models:
                possible_models.append(model_type)
    
    parser.add_argument('--descriptors'   ,
                        help='descriptor1,descriptor2,descriptor1-descriptor2. '+
                        ", ".join(possible_models))
    args = parser.parse_args()
    
    return glob(args.file_set),args.descriptors.split(",")


def getcompositevector(fasta_seq,vec_comb_list):
    """
    Returns one composite vector made from one fasta entry.
    """
    i=1
    tmp_list     = []
    out_vec_list = []
    for vec_type in vec_comb_list.split("-"):

        if   vec_type == "AACOMP": 
            descrip_vec_dict = AAC.CalculateAAComposition(fasta_seq) 
        elif vec_type == "DIPEP":  
            descrip_vec_dict = AAC.CalculateDipeptideComposition(fasta_seq)
        elif vec_type == "TRIPEP": 
            descrip_vec_dict = AAC.CalculateTripeptideComposition(fasta_seq)
        elif vec_type == "SPLITAA":
            descrip_vec_dict = AAC.splitaminoacidcomposition(fasta_seq)            
        elif vec_type == "PSYCHM": 
            descrip_vec_dict = AAC.CalculatePhysicoChemicalProperties(fasta_seq)
        elif vec_type == "MoreauBroto":
            descrip_vec_dict = AUTOC.CalculateNormalizedMoreauBrotoAutoTotal(fasta_seq)
        elif vec_type == "Moran":
            descrip_vec_dict = AUTOC.CalculateMoranAutoTotal(fasta_seq)
        elif vec_type == "Geary":
            descrip_vec_dict = AUTOC.CalculateGearyAutoTotal(fasta_seq)
        elif vec_type == "SequenceOrderCouplingNumberTotal":
            descrip_vec_dict = SQO.GetSequenceOrderCouplingNumberTotal(fasta_seq)
        elif vec_type == "QuasiSequenceOrder":
            descrip_vec_dict = SQO.GetQuasiSequenceOrder(fasta_seq)
        elif vec_type == "CTD":
            descrip_vec_dict = CTD.CalculateCTD(fasta_seq)
        elif vec_type == "C":
            descrip_vec_dict = CTD.CalculateC(fasta_seq)
        elif vec_type == "T": 
            descrip_vec_dict = CTD.CalculateT(fasta_seq)
        elif vec_type == "D":
            descrip_vec_dict = CTD.CalculateD(fasta_seq)
        elif vec_type == "PseudoAAC":
            descrip_vec_dict = PAAC.GetPseudoAAC(fasta_seq,AAP=[PseudoAAC._Hydrophobicity])
        elif vec_type == "APseudoAAC":
            descrip_vec_dict = PAAC.GetAPseudoAAC(fasta_seq)#AAP=[PseudoAAC._Hydrophobicity]       
        else:
            print("ERROR:",vec_type,"is not a supported vector.")
        #Number dictionary elements. 
        vector_list = []
        #Python dicts are unordered so need to sort for consistency
        for d_key in sorted(descrip_vec_dict):#
            vector_list.append(str(i)+":"+('{number:.{digits}f} '.format(number=(descrip_vec_dict[d_key]),digits=5)))
            i+=1        
        tmp_list.append(" ".join(vector_list))
    return " ".join(tmp_list)


def get2Dnamesequencelist(fasta_fileobj_or_str):
    """
    Input : String of fasta entries or file object
    Output: 2D list of fasta names and sequences [[fasta_name,MACTGRT..],..]
    
    This function separates each fasta from the file and passes it to
    the function aapercentages to be converted into svm format.
    It also collects and assembles the multiple lines of svm formatted
    output into a string.
    """
    
    if type(fasta_fileobj_or_str) == str:
        fasta_iter = fasta_data_str.strip().split("\n")
    else:
        fasta_iter = fasta_fileobj_or_str
    #Is a file object 
    i=1
    name_seq_list = []
    fasta_data    = []
    fasta_name    = ''
    for line in fasta_iter:
        #Read through line by line. This is done iteratively to allow for very
        #large files. 
        if line[0] == '>':
            #If the start of a fasta entry enter data 
            if fasta_name != '':
                if len(''.join(fasta_data)) > 60:
                    name_seq_list.append([fasta_name,''.join(fasta_data)])
                    i+=1
                else:
                    print("WARNING: Seqs smallers than 60bp found, ignoring")
                fasta_data = []
            fasta_name = line    
        else:
            fasta_data.append(line.strip())
    if len(fasta_data) > 60:
        name_seq_list.append([fasta_name,''.join(fasta_data)])
    else:
        print("WARNING: Seqs smallers than 60bp found, ignoring")
    """
    Add data from final fasta entry. As there is no '>' char to trigger it's
    addition. 
    """
    return name_seq_list



def makedescriptorvectorlist(fasta_2D_list,descrip_name):
    out_vectors_list = []

    desciptors_unable_to_handle_error_chars = ["PSYCHM","MoreauBroto","Moran","Geary"]
    
    for fasta_2D_el in fasta_2D_list:

        name = fasta_2D_el[0]
        seq  = fasta_2D_el[1]
        
        if not descrip_name in desciptors_unable_to_handle_error_chars: 
            #Generate descriptor vector 
            tmp_vec = getcompositevector(seq,descrip_name)
            #Add to DescriptorVector class
            des_vec_tmp = DescriptorVector(name,descrip_name,tmp_vec) 
            
        else:
            #Add to DescriptorVector class, but in this case the descriptor
            #cannot properly describe the fasta sequence due to non-standard 
            #amino acids. So name vec string as N/A
            des_vec_tmp = DescriptorVector(name,descrip_name,) 
        out_vectors_list.append(des_vec_tmp)
    return out_vectors_list


def multiclassclassification(DescriptorVector_list,model_file_glob):
    #DescriptorVector
    zero_labled_vector_list = []
    for desc_vec in DescriptorVector_list:
         zero_labled_vector_list.append(desc_vec.getclassificationvec())
    
    unknown_file = tempfile.NamedTemporaryFile(mode='w')#, prefix=TEMP_DIR#Note: prefix must end in /
    unknown_file.write("\n".join(zero_labled_vector_list))
    unknown_file.flush()

    #print(model_file_glob)
    for model_file_name in model_file_glob:
        predictions_file = tempfile.NamedTemporaryFile(mode='r')#,prefix=TEMP_DIR,delete=False
        output = subprocess.call("./svm_classify "+
                                 unknown_file.name+" "+
                                 model_file_name  +" "+
                                 predictions_file.name,
                                 shell=True,stdout=open(os.devnull, 'w'), timeout=None) 
        predictions_list = predictions_file.readlines()
        predictions_file.close()
        pred_model = model_file_name.split("/")[-1].split(".")[0]
        try:
            for i in range(0,len(DescriptorVector_list)):
                DescriptorVector_list[i].addpredicition(pred_model,float(predictions_list[i]))
        except:
            print(DescriptorVector_list)
            
            """
                    self.seq_name = vec_name.strip().replace(",",".")
        self.vec_type = vec_type
        #For dealing with illegal chars
        if vec_coords_str:
            self.vec_coords_str = vec_coords_str
        else:
            self.vec_coords_str = self.unvectorizable
        self.pred_dict = {}
        
            """
            
            print("DescriptorVector_list",len(DescriptorVector_list))
            print("predictions_list",len(predictions_list))
            print("pred_model",pred_model)
            
    return DescriptorVector_list


def makepredictionsoutput(composite_classification):
    
    composite_predictions_csv = []
    prediction_values_csv = []
    for i in range(0,len(composite_classification[0])):
        values_csv = [] 
        prediction_values_row = []
        for classif in composite_classification:
            seq_name = classif[i].seq_name
            classif[i].getprediction()
            prediction_values_row.append(classif[i].getpredictionvalues())
            values_csv.append(classif[i].getpredclassandweight())
        
        count_dict = {}
        for e in values_csv:
            if e[0] in count_dict:
                count_dict[e[0]]+=e[1]
            else:
                count_dict.update({e[0]:e[1]})    
        #composite_prediction = 
        composite_predictions_csv.append(seq_name+","+max(count_dict, key=count_dict.get))      
        prediction_values_csv.append(seq_name+","+",".join(prediction_values_row))

    return composite_predictions_csv,prediction_values_csv


def getpredclassandweight(pred_dict):
    z =  sorted(pred_dict, key=pred_dict.get) 
    max_val = pred_dict[z[-1]]
    min_val = pred_dict[z[0]]
    normal_1st = (pred_dict[z[-1]] - min_val)/(max_val - min_val)
    normal_2nd = (pred_dict[z[-2]] - min_val)/(max_val - min_val)
    if max_val > 0:
        return z[-1],normal_1st-normal_2nd
    else:
        return "UNKNOWN",0.0



 


def classifyfastasequences(fasta_names_list,fasta_seq_list,descriptors_list,model_files_path):
    prediction_dict = {}
    pred_val_dict   = {} 
    pred_cnt_dict   = {} 
    
    fasta_names_list_and_preds = []
    prediction_dict_list = []
    pred_val_dict_list   = [] 
    pred_cnt_dict_list   = [] 
    for fasta_name_entry in fasta_names_list:
        fasta_names_list_and_preds.append([fasta_name_entry,{}])        
        pred_cnt_dict_list.append([fasta_name_entry,{}])
        pred_val_dict_list.append([fasta_name_entry,{}])
        prediction_dict_list.append(fasta_name_entry.strip())
        
    for descriptor in descriptors_list:
        fasta_vec_list = []
        for fasta in fasta_seq_list:
            fasta_vec_list.append("0 "+getcompositevector(fasta,descriptor)+"\n")
                    
        unknown_file = tempfile.NamedTemporaryFile(mode='w')#, prefix=TEMP_DIR#Note: prefix must end in /
        unknown_file.write( "".join(fasta_vec_list) )
        unknown_file.flush()
        
        descriptor_classifications_dict = {}
        
        for model_file_name in glob(model_files_path+"/*."+descriptor+".*.model"):
            #print(model_file_name)
            prot_class_name = model_file_name.split("/")[-1].split(".")[0]
            predictions_file = tempfile.NamedTemporaryFile(mode='r')
            output = subprocess.call("./svm_classify "+
                                     unknown_file.name+" "+
                                     model_file_name  +" "+
                                     predictions_file.name,
                                     shell=True,stdout=open(os.devnull, 'w')) 
            
            preds = predictions_file.readlines()
            for pred_line_cnt in range(0,len(preds)):
                fasta_names_list_and_preds[pred_line_cnt][-1].update({prot_class_name:float(preds[pred_line_cnt])})
            predictions_file.close()
        
        
        for fnlap_cnt in range(0,len(fasta_names_list_and_preds)):
            #print(fasta_names_list_and_preds[fnlap_cnt][-1])
            class_pred,weight = getpredclassandweight(fasta_names_list_and_preds[fnlap_cnt][-1])

            if class_pred in pred_val_dict_list[fnlap_cnt][-1]:
                pred_val_dict_list[fnlap_cnt][-1][class_pred]+=weight
            else:
                pred_val_dict_list[fnlap_cnt][-1].update({class_pred:weight})
                
            if class_pred in pred_cnt_dict_list[fnlap_cnt][-1]:
                pred_cnt_dict_list[fnlap_cnt][-1][class_pred]+=1
            else:
                pred_cnt_dict_list[fnlap_cnt][-1].update({class_pred:1})
            
    final_out_list = []
    for fnlap_cnt in range(0,len(fasta_names_list_and_preds)):
        out_line_tmp = [ "".join(prediction_dict_list[fnlap_cnt]) ]
        for dict_el in pred_val_dict_list[fnlap_cnt][-1]:
            out_line_tmp.append(dict_el+"`"+str(pred_cnt_dict_list[fnlap_cnt][-1][dict_el])+"`"+str(pred_val_dict_list[fnlap_cnt][-1][dict_el]))
        
        final_out_list.append("`".join(out_line_tmp))
    

    #for fnlap_cnt in range(0,len(fasta_names_list_and_preds)):
    #    
    #    max_val_class = sorted( pred_val_dict_list[fnlap_cnt][-1], key= pred_val_dict_list[fnlap_cnt][-1].get)
    #    max_cnt_class = sorted( pred_cnt_dict_list[fnlap_cnt][-1], key= pred_cnt_dict_list[fnlap_cnt][-1].get)       
    #
    #    if max_cnt_class[0] == "UNKNOWN":
    #        final_out_list.append("".join(prediction_dict_list[fnlap_cnt])+"`"+max_cnt_class[0])
    #    else:
    #        final_out_list.append("".join(prediction_dict_list[fnlap_cnt])+"`"+max_val_class[0])
     
            
    return "\n".join(final_out_list)


#=============================================================================
#                            Main Program
#=============================================================================

#Get Command Line Arguments
file_name_list,descriptor_list = getargs()
""" 
file_name_list - A list of fasta formatted files containing data
                 to be classified, can be a single name or a collection of 
                 names described by a regular expression. 
model_file_name_list - a single file or regex of model files to be used in 
                       classification.
descriptors_list - a list of the descriptors for the fasta data and to be 
                   converted to and classified with models of the same 
                   descriptor type. Use commas to separate descriptors
                   and dases "-" to create composite vectors.  
"""  
print("Classifying data found in files.",file_name_list)
print("Using descriptors",descriptor_list)


#For each file do a separate prediction. 
for file_name in file_name_list:
    
    #Make sure new files are empty. 
    #preds_csv_file = open(file_name+".preds.csv","w")
    #preds_csv_file.write("")
    #preds_csv_file.close()
    #Values returned from SVM
    #vals_csv_file = open(file_name+".pred_vals.csv","w")
    #vals_csv_file.write("")
    #vals_csv_file.close()  
    
    fasta_name = ""
    file = open(file_name,"r")
    fasta_seqs_list  = []
    fasta_names_list = []
    fasta_data = [] 
    
    fasta_nub_cnt=0
    t1 = time()
    while True:
        line = file.readline()
        #print(line)
        #Read through line by line. This is done iteratively to allow for very
        #large files. 
        if line == "" or line[0] == '>': #If the start of a fasta entry enter data 
            if fasta_name != '':
                fasta_seq = ''.join(fasta_data)
                fasta_nub_cnt+=1
                if len(fasta_seq) > 60:
                        fasta_seqs_list.append(fasta_seq)
                        fasta_names_list.append(fasta_name.strip())

                    #print(fasta_name.strip()+"`"+classifyfastasequences(fasta_seq,descriptor_list,"/var/www/cgi-bin/ligpred/MODEL_FILES")[0])
                else:
                    print("WARNING: Seqs smallers than 60bp found, ignoring")
                    
            if len(fasta_seqs_list) > 20000 or line == "":
                
                print(classifyfastasequences(fasta_names_list,fasta_seqs_list,descriptor_list,"MODEL_FILES"))
                print(time()-t1)
                t1 = time()
                fasta_seqs_list  = []
                fasta_names_list = []
            if line == "":
                break
            fasta_data = []
            fasta_name = line    
        else:
            fasta_data.append(line.strip())  
      

        
file.close()
        
"""    
    for descriptor in descriptor_list:
        #Convert fastas to descriptor vectors
        DescVector_list = makedescriptorvectorlist(fasta_2D_list,descriptor)
                
        #Classify each vector with each model. 
        classifd_DescVec_list = multiclassclassification(DescVector_list,
                                glob(MODEL_FILES_PATH+"/*."+descriptor+".*"))
        
        #for e in classifd_DescVec_list:
        #    print(e.getpredclassandweight())
        
        composite_classification.append(classifd_DescVec_list)
        
    #Interpret data.
    compos_preds_csv,pred_vals_csv = makepredictionsoutput(
                                                    composite_classification)
    
    #Output predictions.
    #Predictions only
    preds_csv_file = open(file_name+".preds.csv","w")
    preds_csv_file.write("\n".join(compos_preds_csv))
    preds_csv_file.close()
    #Values returned from SVM
    vals_csv_file = open(file_name+".pred_vals.csv","w")
    vals_csv_file.write("\n".join(pred_vals_csv))
    vals_csv_file.close()  
"""








