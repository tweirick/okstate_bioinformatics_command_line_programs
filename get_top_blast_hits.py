'''
Orf2333_2128205_2128900 tr|E1SW70|E1SW70_FERBD  43.10   232     124     5       1       226     1       230     5e-48    168
Orf2333_2128205_2128900 tr|A3Y7E8|A3Y7E8_9GAMM  38.79   232     128     4       1       225     1       225     2e-46    164
Orf2333_2128205_2128900 tr|L8WCJ5|L8WCJ5_9GAMM  36.25   240     144     3       1       231     1       240     6e-45    161
Orf2333_2128205_2128900 tr|L8W3B1|L8W3B1_9GAMM  35.65   230     143     3       1       225     1       230     1e-44    160
Orf2333_2128205_2128900 tr|Q5WUJ3|Q5WUJ3_LEGPL  35.34   232     142     4       1       226     1       230     1e-41    152
Orf2333_2128205_2128900 tr|I7HTU1|I7HTU1_LEGPN  35.34   232     142     4       1       226     1       230     1e-41    151
Orf2333_2128205_2128900 tr|Q5ZTB3|Q5ZTB3_LEGPH  34.63   231     145     3       1       226     1       230     2e-41    151
Orf2333_2128205_2128900 tr|M4SR25|M4SR25_LEGPN  34.63   231     145     3       1       226     1       230     2e-41    151
Orf2333_2128205_2128900 tr|I7HRR0|I7HRR0_LEGPN  34.63   231     145     3       1       226     1       230     2e-41    151
'''


from glob import glob

file_glob = glob("haloAminoAcids.faa.*of50.fasta.blastp-on-uniprot")

for file_name in file_glob: 
    members_set = set()
    for line in open(file_name,'r'):
        orf_id = line.split()[0]
        if not orf_id in members_set:  
            ac    = line.split()[1].split("|")[1]
            eval  = line.split()[-2]
            bit   = line.split()[-1]
            print(orf_id+"\t"+ac+"\t"+eval+"\t"+bit)
            members_set.add(orf_id)
