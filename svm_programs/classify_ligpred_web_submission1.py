#!/usr/local/bin/python3.3 -u

import sys, os, subprocess
from time import time,ctime
from copy import deepcopy
import cgi
from glob import glob
import tempfile
import AAIndex
import AAComposition as AAC
import QuasiSequenceOrder
import PseudoAAC
from PseudoAAC import *
import CTD
import Autocorrelation
t1 = time()
    
#=============================================================================
#                          Constants and Varibles
#=============================================================================
prediction_in_progress_page_name = "refresh.html"
DEBUG            = False 
MODEL_FILE_PATH  = "/var/www/cgi-bin/ligpred/MODEL_DIPEP_COMP/"
TEMP_DIR         = '/var/www/html/ligpred/LIGPRED_TMP/'#Needs web server ownership
prog_result         = {}
vector_str          = ""
fasta_data_is_valid = False
score_matrix = []
print_value = "Running Predictions. "
log_file_list  = []
input_data_txt = []

#=============================================================================
#                             Functions
#=============================================================================


def make_name_seq_2D_Listand_names(fasta_data_str):
    """
    Input : file name string
    Output: collection of SVM formatted strings
    
    This function separates each fasta from the file and passes it to
    the function aapercentages to be converted into svm format.
    It also collects and assembles the multiple lines of svm formatted
    output into a string.
    """
    fasta_data_str = fasta_data_str.strip()
    name_seq_list = []
    fasta_data = []
    fasta_name = ''
    names_list = []
    out_name_list = []
    i=1
    for line in fasta_data_str.split("\n"):
        #Read through line by line. This is done iteratively to allow for very
        #large files. 
        #for line in open(file_name,"r"):
        if line[0] == '>':
            #If the start of a fasta entry enter data 
            if fasta_name != '':
                name_seq_list.append([fasta_name,''.join(fasta_data)])
                fasta_data = []
            fasta_name = line    
            names_list.append([str(i),fasta_name])
            i+=1
            out_name_list.append([fasta_name.replace(",",".")])
        else:
            fasta_data.append(line.strip())
    """
    Add data from final fasta entry. As there is no '>' char to trigger it's
    addition. 
    """
    name_seq_list.append([fasta_name,''.join(fasta_data)])
    return name_seq_list,names_list,out_name_list 


def isvalidatefasta(fasta_txt,only_20_AAs=True,validate_protein=True):
    
     return True
     aa_set = {'A','C','D','E','F',
               'G','H','I','K','L',
               'M','N','P','Q','R',
               'S','T','V','W','Y'}
     illegal_fasta_name_chars_set = {}
     line_number  = 0
     
     for line in fasta_txt.split("\n"):
         line_number+=1
         if line[0] == ">":
             if False:#set( line.strip() ).difference(aa_set) == set():
                 return False
         else:
             if set( line.strip() ).difference(aa_set) == set():
                 return False
     return True


def getfastanames(fasta_seqs):
    split_fasta_data = fasta_seqs.split("\n")
    fasta_names = []
    for line in split_fasta_data:
        if line[0] == ">":
            fasta_names.append(line)
    return fasta_names


def writerefreshpage(temp_page_name,text_to_add):
    #Note: prefix must end in /
    #makepredictingpage(prediction_in_progress_page_name,"/var/www/html/ligpred/jobs/"+saved_data_url)
    file = open("refresh.html")
    html_text = file.read().replace('<div id="progress"></div>',text_to_add)
    file.close()
    out_html_file = open("/var/www/html/ligpred/jobs/"+temp_page_name,"w")
    out_html_file.write(html_text)
    out_html_file.close()
    


def getcompositevector(fasta_seq,vec_comb_list):
    """
    Returns one composite vector made from one fasta entry.
    """
    i=1
    tmp_list     = []
    out_vec_list = []
    for vec_type in vec_comb_list.split("-"):

        if   vec_type == "AACOMP": descrip_vec_dict = AAC.CalculateAAComposition(fasta_seq) 
        elif vec_type == "DIPEP":  descrip_vec_dict = AAC.CalculateDipeptideComposition(fasta_seq)
        elif vec_type == "TRIPEP": descrip_vec_dict = AAC.CalculateTripeptideComposition(fasta_seq)
        elif vec_type == "SPLITAA":descrip_vec_dict = AAC.splitaminoacidcomposition(fasta_seq)            
        elif vec_type == "PSYCHM": descrip_vec_dict = AAC.CalculatePhysicoChemicalProperties(fasta_seq)
        elif vec_type == "MoreauBroto":descrip_vec_dict = Autocorrelation.CalculateNormalizedMoreauBrotoAutoTotal(fasta_seq)
        elif vec_type == "Moran":descrip_vec_dict = Autocorrelation.CalculateMoranAutoTotal(fasta_seq)
        elif vec_type == "Geary":descrip_vec_dict = Autocorrelation.CalculateGearyAutoTotal(fasta_seq)
        elif vec_type == "SequenceOrderCouplingNumberTotal":descrip_vec_dict = QuasiSequenceOrder.GetSequenceOrderCouplingNumberTotal(fasta_seq)
        elif vec_type == "QuasiSequenceOrder":descrip_vec_dict = QuasiSequenceOrder.GetQuasiSequenceOrder(fasta_seq)
        elif vec_type == "CTD":descrip_vec_dict = CTD.CalculateCTD(fasta_seq)
        elif vec_type == "C":  descrip_vec_dict = CTD.CalculateC(fasta_seq)
        elif vec_type == "T":  descrip_vec_dict = CTD.CalculateT(fasta_seq)
        elif vec_type == "D":  descrip_vec_dict = CTD.CalculateD(fasta_seq)
        elif vec_type == "PseudoAAC":descrip_vec_dict = PseudoAAC.GetPseudoAAC(fasta_seq,AAP=[PseudoAAC._Hydrophobicity])
        elif vec_type == "APseudoAAC":descrip_vec_dict = PseudoAAC.GetAPseudoAAC(fasta_seq)#AAP=[PseudoAAC._Hydrophobicity]       
        else:print("ERROR:",vec_type,"is not a supported vector.")

        #Number dictionary elements. 
        vector_list = []
        #Python dicts are unordered so need to sort for consistency
        for d_key in sorted(descrip_vec_dict):#
            vector_list.append(str(i)+":"+('{number:.{digits}f} '.format(number=(descrip_vec_dict[d_key]),digits=5)))
            i+=1        
        tmp_list.append(" ".join(vector_list))

    return " ".join(tmp_list)


def allStandardChars(fasta_sequence):
    nonstandard_char_set = set(fasta_sequence) - set("ARNDCEQGHILKMFPSTWYV")
    #lsprint(nonstandard_char_set)
    if nonstandard_char_set == set():
        return True
    return False


#=============================================================================
#                             Main Program
#=============================================================================

#Get form data.
form_data  = cgi.FieldStorage()
b1 = '<a href="http://bioinfo.okstate.edu/ligpred/jobs/'
b2 = '" title="http://bioinfo.okstate.edu/ligpred/jobs/'
b3 = '" class="bookmark">Click here to bookmark this page.</a>'
model_progress = []
d1 = "<div style='text-align: left;padding-left:80px;'>"
d2 = "</div>"
#Validate input data.
if "fasta_data" in form_data:
    saved_data_url = form_data.getvalue("saved_data_url")
    predictor_list = form_data.getvalue("pred_str").split(",")
    bookmark_link = b1+saved_data_url+b2+saved_data_url+b3
    
    model_progress.append(
        "<br/><br/>Data received. "+ctime(time())+"<br/>Waiting for classification using descriptors:<br/>"+
        "<br/>".join(predictor_list))
    log_file_list.append("Data received. "+ctime(time())+"\nWaiting for classification using descriptors:")
    log_file_list.append(" ".join(predictor_list))
    
    writerefreshpage(saved_data_url,bookmark_link+d1+"".join(model_progress)+d2)
    fasta_seqs     = form_data.getvalue("fasta_data").strip()
    
else:
    bookmark_link = ""
    predictor_list = ["AACOMP"]#,,"Geary"
    seqs_file = open("/var/www/html/ligpred/text_fastas.html","r")
    fasta_seqs= seqs_file.read()
    saved_data_url  = "duy5Bek5.html"
    



out_dict = {} 

if isvalidatefasta(fasta_seqs):# Validate format of received fasta data.     
    
    #Need to write this file fast. 
    model_progress.append("</br> Starting classification. "+ctime(time())+"<br/>")
    log_file_list.append("Starting classification. "+ctime(time()))
    writerefreshpage(saved_data_url,bookmark_link+d1+"".join(model_progress)+d2)
    
    fasta_names_seqs_list,main_names_list,out_name_list_1 = make_name_seq_2D_Listand_names(fasta_seqs)
    csv_file_list     = out_name_list_1
    progress_list     = []
    csv_thing         = []
    add_fasta_to_csv  = True
    csv_title         =  ["Sequence Name"]

    for predictor in sorted(predictor_list):
        
        fasta_names          = []
        vector_file_txt_list = []
        
        for name_and_seq in fasta_names_seqs_list:
            fasta_name     = name_and_seq[0]
            fasta_sequence = name_and_seq[1]
            if add_fasta_to_csv:
                csv_thing.append([name_and_seq[0],[]])
            fasta_names.append([fasta_name,{"pred_value":"N/A","pred_name":"UNKNOWN"}])
            if "PSYCHM" in predictor or "MoreauBroto" in predictor or "Moran" in predictor or "Geary" in predictor:
                #These cannot handle ambiguous chars outside of the 20 amino acids. 
                if allStandardChars(fasta_sequence):
                    vector_file_txt_list.append("0 "+getcompositevector(fasta_sequence,predictor)+"\n")
                else:
                    #Use these to keep track of spacing 
                    vector_file_txt_list.append("")#Empty String 
            else:    
                vector_file_txt_list.append("0 "+getcompositevector(fasta_sequence,predictor)+"\n")
        add_fasta_to_csv = False

        unknown_file = tempfile.NamedTemporaryFile(mode='w')#, prefix=TEMP_DIR#Note: prefix must end in /
        unknown_file.write("".join(vector_file_txt_list))
        unknown_file.flush()
        model_count = 0

        sorted_model_file_glob = sorted(glob(MODEL_FILE_PATH+"*."+predictor+".*model"))

        classification_start_time = time()
        for model_file_name in sorted_model_file_glob:
            model_count+=1
            class_name = model_file_name.split(".")[0].split("/")[-1]   
            
            if predictor == "Geary":
               classification_prog = ("Classifying with "+predictor+" "+str(model_count)+"/"+str(len(sorted_model_file_glob))+
                                     " (This may take a while.).")
            else:
               classification_prog = ("Classifying with "+predictor+" "+str(model_count)+"/"+str(len(sorted_model_file_glob))+".")
            
     
            #Need to write this file fast. 
            #model_progress.append("</br> Starting classification. "+ctime(time())+"<br/>")
            writerefreshpage(saved_data_url,bookmark_link+d1+"".join(model_progress)+classification_prog+d2)
            log_file_list.append(classification_prog+" "+ctime(time()))     
                    
            predictions_file = tempfile.NamedTemporaryFile(mode='r')#,prefix=TEMP_DIR,delete=False
            output = subprocess.call("/var/www/cgi-bin/ligpred/./svm_classify "+
                                     unknown_file.name+" "+model_file_name+" "+predictions_file.name,
                                     shell=True,stdout=open(os.devnull, 'w'), timeout=None) 
            
            predictions_lines_list = predictions_file.readlines()
            predictions_file.close()


            true_line_cnt      = 0
            pred_file_line_cnt = 0
            csv_title.append(predictor+":"+class_name)
            for unknown_seq in vector_file_txt_list:

                if vector_file_txt_list[pred_file_line_cnt] != "" and predictions_lines_list != []:
                    
                    prediction_val = predictions_lines_list[pred_file_line_cnt].strip()
                    csv_val = prediction_val
                    pred_float = float(prediction_val)
                    
                    if pred_float > 0 and fasta_names[pred_file_line_cnt][1]["pred_value"] == "N/A":
                        fasta_names[pred_file_line_cnt][1]["pred_value"] = pred_float
                        fasta_names[pred_file_line_cnt][1]["pred_name"]  = class_name
                    elif pred_float > 0 and fasta_names[pred_file_line_cnt][1]["pred_value"] < pred_float:
                        fasta_names[pred_file_line_cnt][1]["pred_value"] = pred_float
                        fasta_names[pred_file_line_cnt][1]["pred_name"]  = class_name
                    elif fasta_names[pred_file_line_cnt][1]["pred_value"] == pred_float:
                        fasta_names[pred_file_line_cnt][1]["pred_name"] = "UNKNOWN"
                    pred_file_line_cnt+=1
                else:
                    csv_val = "ERR CHR"
                    fasta_names[true_line_cnt][1]["pred_name"] = "ERR CHR"
                csv_thing[true_line_cnt][1].append(csv_val)  
                true_line_cnt+=1
            
            #writerefreshpage(saved_data_url,bookmark_link+"<br/>"+"values parsed"+"\n".join(progress_list)+"<br/>"+model_progress)
        
        #We are done with this set of vectors close unknown vectors file. 
        unknown_file.close()
        model_progress.append("Classification of "+predictor+" complete. "+ctime(time())+"<br/>")
        log_file_list.append("Classification of "+predictor+" complete. "+ctime(time()))
        writerefreshpage(saved_data_url,bookmark_link+d1+"".join(model_progress)+d2)
                
        for i in range(0,len(main_names_list)):
            assert fasta_names[i][0] == main_names_list[i][1],fasta_names[i][1]+" "+main_names_list[i][1]
            main_names_list[i].append(fasta_names[i][1]["pred_name"])

    out_str_list = []
    prediction_only_csv = []
    #Make a composite score and make out strings
    for i in range(0,len(main_names_list)):
        print(main_names_list[i])
        count_dict = {}
        for e in main_names_list[i][2:]:
            if e in count_dict:count_dict[e]+=1
            else:count_dict.update({e:1})
        main_names_list[i].append(sorted(count_dict, key=count_dict.get)[-1])
        prediction_only_csv.append(",".join(main_names_list[i]))
        main_names_list[i][1] = main_names_list[i][1][:20]
        out_str_list.append("<td class='fastaID'>"+ "</td><td class='fastaID'>".join(main_names_list[i])+"</td>")
    
    cout_list = []
    for cccc in csv_thing:
        cout_list.append(cccc[0].replace(",",".")+","+",".join(cccc[1]))
    total_csv_p_name = saved_data_url.strip(".html")+".txt"
    file = open("/var/www/html/ligpred/jobs/"+total_csv_p_name,"w")
    file.write(",".join(csv_title)+ "\n" + "\n".join(cout_list))
    file.close()

        
    log_p_name = saved_data_url.replace(".html",".log")
    file = open("/var/www/html/ligpred/jobs/"+log_p_name,"w")
    file.write("\n".join(log_file_list))
    file.close()
    

    input_data_p_name = saved_data_url.replace(".html",".faa")
    file = open("/var/www/html/ligpred/jobs/"+input_data_p_name,"w")
    file.write(fasta_seqs)
    file.close()
    
    title = ["Input Order"]+["Input Sequence ID"]+sorted(predictor_list)+["Prediction"]
        
    pred_csv_p_name = saved_data_url.replace(".html","_pred.txt")
    file = open("/var/www/html/ligpred/jobs/"+pred_csv_p_name,"w")
    file.write(",".join(title)+"\n"+"\n".join(prediction_only_csv))
    file.close()
    
    
    out_table_head = "<thead> <tr><th class='fastaID'>"+ "</th><th class='fastaID'>".join(title)+"</th></tr></thead> "
    out_table_body = "<tbody> <tr>"+"</tr><tr>".join(out_str_list)+"</tr></tbody>"
    out_table_str ="<table id='myTable' class='tablesorter'>"+out_table_head+out_table_body+"</table>"
    html_file = open("index_temp.html","r")
    html_txt = html_file.read()
    out_table_str = html_txt.replace('<div id="classification_results"></div>',
        bookmark_link+'<br/><br/><br/><div style="text-align:left;">'+
         #'<a href="http://bioinfo.okstate.edu/ligpred/jobs/'+saved_data_url.strip(".html")+'.csv"'+'>Download CSV of Predictions</a>'+
         ' <a style="margin-right: 10px;" href="http://bioinfo.okstate.edu/ligpred/jobs/'+input_data_p_name+'">View Submitted Data</a>'+
         ' <a style="margin-right: 10px;" href="http://bioinfo.okstate.edu/ligpred/jobs/'+log_p_name+       '">View Log File</a>'+
         ' <a style="margin-right: 10px;" href="http://bioinfo.okstate.edu/ligpred/jobs/'+total_csv_p_name+'" >View Raw Values as CSV</a>'+
         ' <a style="margin-right: 10px;" href="http://bioinfo.okstate.edu/ligpred/jobs/'+pred_csv_p_name+'" >View Predictions as CSV</a>'+
         ' </div><div id="classification_results">'+
          out_table_str+'</div><br/>')
    
    html_file.close()
    file = open("/var/www/html/ligpred/jobs/"+saved_data_url,"w")
    file.write(out_table_str)
    file.close()
    

else:
    #Need to write this file fast. 
    writerefreshpage(saved_data_url,bookmark_link+
                 "<br/>Waiting for classification using "+
                 "\n".join(predictor_list)+" descriptors to start.")
    

