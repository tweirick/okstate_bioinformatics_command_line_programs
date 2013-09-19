from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Alphabet import generic_dna

file_list = ["switchgrass_454AllContigs.fna"] #"all_switchgrass_transcripts1.fna"]
for file_name in file_list:
    input_seq_iterator = SeqIO.parse( open(file_name, "rU"), "fasta")
    for seq_el in input_seq_iterator:
        
        seq_el.alphabet=generic_dna        
        print(seq_el)
        print(seq_el.alphabet)
        print(seq_el.seq)
        print(seq_el.seq.translate())
        print(seq_el.seq[1:].translate())
        print(seq_el.seq[2:].translate())
        
    
