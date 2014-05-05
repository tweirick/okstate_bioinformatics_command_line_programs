'''
Orf2121_1925028_1925396	K9DBF7	2e-23	102
Orf2122_1925444_1925908	F7QDW8	2e-19	89.7
Orf2123_1925905_1926579	F7QDW9	4e-54	195
Orf2124_1926637_1927542	A4BRW4	6e-64	217
Orf2125_1927795_1928727	A4BRW3	5e-163	471
Orf2126_1928681_1928995	A4BRW3	1e-24	104
Orf2127_1929214_1930731	A4BRW2	0.0	823
Orf2128_1930759_1931355	A4BRW1	3e-63	204
Orf2129_1931565_1932218	A4BRW0	3e-35	134
Orf2130_1932301_1933581	Q0A999	4e-121	370
'''


input_dict = {}
tsv_file = "orf_prots_top_hits.tsv"
for line in open(tsv_file,'r'):
    ac = line.split()[1]

    if ac in input_dict:
        input_dict[ac].append( line.strip() )
    else:
       input_dict[ac]=[line.strip()]

uniprot    = "/scratch/tweiric/LARGE_FILES/uniprot_trembl.dat"
uniprot    = "/scratch/tweiric/LARGE_FILES/uniprot_sprot.dat"
current_ac = ""
in_dict = False
prot_annotation = "None"
prot_gene_name  = "None"
ec_num          = "None"
for line in open(uniprot,'r'):
    if line[:2] == "AC":
            current_ac = line.split()[-2].strip(";")
            in_dict = current_ac in input_dict
    elif in_dict and line[:2] == "DE" and ('SubName:' in line or 'RecName:' in line):
        prot_annotation = line.split("Full=")[-1].strip().strip(";")
    elif in_dict and line[:2] == "DE" and 'EC=' in line:
        ec_num = line.split("EC=")[-1].strip().strip(";")
    elif in_dict and line[:2] == "GN" and 'SubName:' in line:
        prot_gene_name = line.split("Name=")[-1].split(";")[0].strip()
    elif in_dict and line[:2] == "//": 
        for orf_el in input_dict[current_ac]:
            print( orf_el+"\t"+prot_annotation+"\t"+prot_gene_name+"\t"+ec_num  )
        prot_annotation = "None"
        prot_gene_name  = "None"
        ec_num          = "None"
