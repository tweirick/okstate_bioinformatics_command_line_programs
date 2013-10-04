'''
This program will return lists of IDs found in PSIBLAST results.  
'''

from sys import hexversion
from glob import glob

py_version = hex(hexversion)
FORMATS_SUPPORTED = ["0","7"]

#Accept comand line arguments 
#The optparse libary has been depreciated so check the version of python and
#choose which to use accordingly. 
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
        
       parser.add_argument('--psiblast_file_set',
            help='''Accepts single files or regexs''')
       #parser.add_argument('--fasta_file_set',
       #     help='''Accepts single files or regexs''')
       parser.add_argument('--psiblast_format',
            help='Number used to control output format. ex tabbed = 7, normal = 0',
            default=FORMATS_SUPPORTED[0])

       args = parser.parse_args()
       psiblast_glob   = glob(args.psiblast_file_set)
       #fasta_glob      = glob(args.fasta_file_set)
       psiblast_format = args.psiblast_format 
       return psiblast_glob, psiblast_format
else:
    from optparse import OptionParser
    def getargs(ver='%prog 0.0'):
        '''
        This function handles the command line arguments.
        '''
        desc=open(__file__).read().split("'''")[1]
        parser = OptionParser(description=desc)

        parser.add_option(
            '--psiblast_file_set',
            help='''Accepts single files or regex used "" for regexes ex: --file_set "*.faa" ''')

        #parser.add_option('--fasta_file_set',
        #    help='Accepts single files or regexs' )

        parser.add_option('--psiblast_format',
            help='Number used to control output format.',
            default=FORMATS_SUPPORTED[0])

        args = parser.parse_args()
        psiblast_glob   = glob(args.psiblast_file_set)
        #fasta_glob      = glob(args.fasta_file_set)
        psiblast_format = args.psiblast_format 
        return psiblast_glob,psiblast_format





def parseformat0(file_name):

    file_queries_dict     = {}
    set_of_unique_queires = []
    name_of_last_query    = None
    READ_SEQUENCE_IDS     = False

    query_cnt             = 0
    query_ID              = ""
    query_to_save         = ""
    for line in open(file_name,"r"):
        #print(line)
        if line != "\n":
            if QUERY in line:
                #This indicates the start of a query or round of a query.
                #ex:Query= sp|P35510|PAL1_ARATH Phenylalanine ammonia-lyase 1 OS=Arabidopsis
                if line != name_of_last_query and name_of_last_query != None:
                    #New query, save collected data. 
                    query_cnt+=1
                    try:
                        query_ID = line.split("|")[1]
                    except:
                        query_ID = line.strip()
                        print(query_ID)
                    for query_to_save in query_results:
                         if query_to_save in file_queries_dict:
                             file_queries_dict[query_to_save].append(query_ID)
                         else:
                             file_queries_dict.update({query_to_save:[query_ID]})
                name_of_last_query = line
                query_results      = []
                READ_SEQUENCE_IDS = True
            elif len(line) > 0 and line[0] == ">":
                READ_SEQUENCE_IDS = False
            else:
                if READ_SEQUENCE_IDS and line.count("|") >= 2:
                    #assert line.count("|") == 2,line
                    ID = line.split("|")[1]
                    query_results.append(ID)
    #Get Last Round
    for query_to_save in query_results:
        if query_to_save in file_queries_dict:
            file_queries_dict[query_to_save].append(query_ID)
        else:
            file_queries_dict.update({query_to_save:[query_ID]})
    query_results = []

    #print(file_queries_dict)

    out_list = ["Number of unique sequence IDs found:"+str(len(file_queries_dict))]
    out_list.append("Number of sequences in query:"+str(query_cnt))
    flat_list = []
    for qkey in file_queries_dict:
        flat_list.append(qkey)
        out_list.append(qkey+" "+str(len(file_queries_dict[qkey]))+" "+" ".join(file_queries_dict[qkey]))
    file_queries_dict = {}

    return flat_list

def parseformat7(file_name):
    """
    
    """
    get_name = False
    title = ["Iteration Number","query db", "query id", "subject db", "subject id", 
             "% identity", "alignment length", "mismatches", "gap opens", "q. start", 
             "q. end", "s. start", "s. end", "evalue", "bit score"]
 
    flat_list = []
    iteration_number = ""
    for line in open(file_name,'r'):
        line = line.strip()
        if len(line.strip()) > 0:
            if "# Iteration: 1" in line:
                get_name = True
                iteration_number = line.strip().split("# Iteration: ")[0]
            elif get_name:
                get_name = False
                query_name = line.split("|")[1]
            if line[0] != "#" and not "Search has CONVERGED!" in line:
                
                split_line = line.split()
                #split_line[0] = split_line[0].split("|")[1]
                #split_line[1] = split_line[1].split("|")[1]
                 
                seq_id = split_line[1].split("|")[1]

                #split_line.insert(1,split_line[1].split("|")[0])                
                #split_line.insert(0,split_line[0].split("|")[0])
                #split_line.insert(0,iteration_number)

                if not seq_id in flat_list:
                    flat_list.append( seq_id  )
    return flat_list

psiblast_glob,psiblast_format = getargs()

for psiblast_name in psiblast_glob:
   
    #Parse
    if psiblast_format == "0":
        flat_list = parseformat0(psiblast_name)
    elif psiblast_format == "7":
        flat_list = parseformat7(psiblast_name)
    else: 
        print("ERROR: unsupported format.")
    print(psiblast_name)
    out_file = open(psiblast_name+".acflat","w")
    out_file.write("\n".join(flat_list))
    out_file.close()




















