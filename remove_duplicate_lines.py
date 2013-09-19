'''
@author: Tyler Weirick
@date: 2013-08-25
==============================================================================
This is a quick fix program to fix remove illegal sequences from interproscan.
==============================================================================
'''


import argparse

parser = argparse.ArgumentParser(
   description=open(__file__).read().split("'''")[1],
   formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('--file1',
help='''The name of a fasta formatted file. ''',
required=True)
parser.add_argument('--file2',
help='''The name of a fasta formatted file. ''',required=True)
parser.add_argument('--out_file',
help='''A file name for the output to be written too. 
If none give output will be printed.''',
default=None)



#file_name = "../VDH_homologylevel.faa.global.vec"
file_name = "../VDH_homologylevel_negset.faa.global.vec"

file_name = "/home/tyler/repositories/data/VDH_DESC_VECS/VDH_homologylevel.faa.pruneBJXZ.fasta.greaterthan61chars.faa.TRIPEP.EL_DESC_VAL.vec"
file_name = "/home/tyler/repositories/data/VDH_DESC_VECS/VDH_homologylevel.faa.on.VDH_SwissProtnegativeset.faa.psiblastout.uniqueids.faa.pruneBJXZ.fasta.greaterthan61chars.faa.TRIPEP.EL_DESC_VAL.vec"

line_dict = {}
out_lines = []
overlap_cnt = 0
for line in open(file_name,'r'):
    if not line in line_dict:
        line_dict.update({line:""})
        out_lines.append(line)
    else:
        overlap_cnt+=1
of = open(file_name+".fix",'w')
of.write("".join(out_lines))
of.close()

print(overlap_cnt)