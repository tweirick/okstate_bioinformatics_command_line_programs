'''
@author: Tyler Weirick
@date: 2013-08-14
==============================================================================
This program downloads fasta entries from uniprot. It is intended for use with
large sets of fastas, i.e. larger than a single batch download will allow.
Although if you have a very large number of sequences or files other options
may be faster. 
Input: 
- a flat text file with one uniprot accesion file per line. 
Output: 
- a fasta file corresponding to each flat file read in. Name as the input
file name + .faa 
==============================================================================
'''
#http://www.uniprot.org/batch/?query=P13368%20P20806%20Q9UM73%20P97793%20Q17192&format=fasta
from time import sleep
import urllib,urllib2
from glob import glob
import argparse

parser = argparse.ArgumentParser(
   description=open(__file__).read().split("'''")[1],
   formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('--file_set',
                   help='File name or regex.')

args = parser.parse_args()
file_glob = glob(args.file_set)

url = 'http://www.uniprot.org/batch/'
for file_name in file_glob:
    id_set = set()
    for line in open(file_name,'r'):
        id_set.add(line.strip())
    cnt=0
    out_str = []
    print(file_name)
    for i in range(0,len(id_set),500):
        #params = {
        #'format':'fasta',
        #'query': " ".join(list(id_set)[i:i+500])
        #}
        #data = urllib.urlencode(params)
        #request = urllib2.Request(url, data)
        params = {
        'format':'fasta',
        'query': " ".join(list(id_set)[i:i+500])
        }
        data    = urllib.urlencode(params)
        request = urllib2.Request(url, data)
        # Please set your email address here to help us debug in case of problems.
        contact = "example@example.com" 
        request.add_header('User-Agent', 'Python %s' % contact)
        response = urllib2.urlopen(request)
        page = response.read()
        out_str.append(page)
        #print("http://www.uniprot.org/batch/?query="+" ".join(list(id_set)[i:i+500])+"&format=fasta")  
        print(cnt,i,i+500,len(list(id_set)[i:i+500]))
        cnt+=1
        sleep(2.0)
    of = open(file_name+".faa",'w')
    of.write("\n".join(out_str))
    of.close()

