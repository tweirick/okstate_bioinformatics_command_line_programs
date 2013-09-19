

def tabformat(file_name):
    last_prot_ac = None
    for line in open(file_name):
        """
        The TSV format presents the match data in columns as follows:

        0 Protein Accession (e.g. P51587)
        1 Sequence MD5 digest (e.g. 14086411a2cdf1c4cba63020e1622579)
        2 Sequence Length (e.g. 3418)
        3 Analysis (e.g. Pfam / PRINTS / Gene3D)
        4 Signature Accession (e.g. PF09103 / G3DSA:2.40.50.140)
        5 Signature Description (e.g. BRCA2 repeat profile)
        6 Start location
        7 Stop location
        8 Score - is the e-value of the match reported by member database method (e.g. 3.1E-52)
        9 Status - is the status of the match (T: true)
        10 Date - is the date of the run
         (InterPro annotations - accession (e.g. IPR002093) - optional column; only displayed if -iprscan option is switched on)
         (InterPro annotations - description (e.g. BRCA2 repeat) - optional column; only displayed if -iprscan option is switched on)
         (GO annotations (e.g. GO:0005515) - optional column; only displayed if --goterms option is switched on)
         (Pathways annotations (e.g. REACT_71) - optional column; only displayed if --pathways option is switched on)
        
        P51587  14086411a2cdf1c4cba63020e1622579        3418    Pfam    PF09103 BRCA2, oligonucleotide/oligosaccharide-binding, domain 1        2670    2799    7.9E-43 T       15-03-2013
        P51587  14086411a2cdf1c4cba63020e1622579        3418    ProSiteProfiles PS50138 BRCA2 repeat profile.   1002    1036    0.0     T       18-03-2013      IPR002093       BRCA2 repeat    GO:0005515|GO:0006302
        P51587  14086411a2cdf1c4cba63020e1622579        3418    Gene3D  G3DSA:2.40.50.140               2966    3051    3.1E-52 T       15-03-2013
        ...

        """
        sp_line = line.strip().split()

        prot_ac      = sp_line[0]
        domain_start = 
        domain_end   = 

        score        = sp_line[8]
        

        if prot_ac == last_prot_ac:
            #More domains from the same protein. 
            ac_dict.update()
        else:
            if total_domains_dict != {}:
                total_domains_dict.update({prot_ac:})
            #New entry
            #Make new entry dict 
            ac_dict = {:{}}
            

