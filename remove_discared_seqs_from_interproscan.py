
'''
@author: Tyler Weirick
@date: 2013-08-25
==============================================================================
This is a q program to fix remove illegal sequences from interproscan.
==============================================================================
'''

import argparse

parser = argparse.ArgumentParser(
   description=open(__file__).read().split("'''")[1],
   formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('--interpro_scan_file',
help='''The name of a fasta formatted file. ''',
required=True)
parser.add_argument('--discared_fasta_file',
help='''The name of a fasta formatted file. ''',
required=True)
parser.add_argument('--min_aas',
help='''The name of a fasta formatted file. ''',
type=int,
default=62)

args = parser.parse_args()

fasta_file         = args.discared_fasta_file
interpro_scan_file = args.interpro_scan_file
min_aas            = args.min_aas

id_set = set()
for line in open(fasta_file,'r'):
    if line[0] == ">":
        seq_accession = line.split("|")[1]
        id_set.add(seq_accession)

out_list = []
for line in open(interpro_scan_file,'r'):
    sp_line = line.split()
    if not sp_line[0] in sp_line and int(sp_line[2]) > min_aas :
        out_list.append(line)

of = open(interpro_scan_file+".illegal_removed.tsv",'w')
of.write("".join(out_list))
of.close()

