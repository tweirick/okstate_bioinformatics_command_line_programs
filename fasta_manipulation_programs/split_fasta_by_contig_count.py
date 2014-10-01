'''
The purpose of this program is to split fasta files into smaller files 
based of a maximum number of contigs. It is designed to work as itterativly as 
possible to handle very large files. 
'''
import sys

#@TODO: add command line input options
#Get the head comments.
#parser = argparse.ArgumentParser(description=desc,formatter_class=argparse.RawDescriptionHelpFormatter)
#parser.add_argument('--psiblast_file_set',help='''Accepts single files or regexs''')

file_glob   = sys.argv[1:]
#This varible controls the max number of contigs in the output files. 
max_contigs = 500000

for file_name in file_glob:
    contig_count  = 0
    file_name_cnt = 1 
    out_file_obj = open(file_name+"."+str(file_name_cnt)+".fasta",'w')
	for line in open(file_name):

        if line[0] == ">": 
            if contig_count >= max_contigs:
                file_name_cnt+=1 
                contig_count = 0
                out_file_obj.close()
                out_file_obj = open(file_name+"."+str(file_name_cnt)+".fasta",'w')
            contig_count+=1
        out_file_obj.write(line)
        #out_file.flush()

out_file_obj.close()