from glob import glob

import argparse

parser = argparse.ArgumentParser(
   description=open(__file__).read().split("'''")[1],
   formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('--file_set',
help=''' ''',
required=True)

args = parser.parse_args()

for file_name in sorted(glob(args.file_set)):
    prev_len = None
    for line in open(file_name,'r'):
        if prev_len == None:
            prev_len = len(line.split())
            prev_set = set(line.split())
        else:
           if prev_len !=  len(line.split()):
               print(file_name,"ERROR",prev_len,len(line.split()))
               #print(  set(line.split()) - prev_set  )

               #exit()

    print("OK",file_name,"",prev_len)
