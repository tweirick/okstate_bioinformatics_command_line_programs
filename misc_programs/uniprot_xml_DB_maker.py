
#!/opt/python3/bin/python3.2
'''
.py
@author: Tyler Weirick
@Created on: 5/3/2012 Version 0.0 
@language:Python 3.2
@tags: uniprot ID map 

'''

def getargs():
    
    parser = argparse.ArgumentParser(description='Process some integers.')
    
    #parser.add_argument('integers', metavar='N', type=int, nargs='+',
    #               help='an integer for the accumulator')
    parser.add_argument('--ID_file_name', 
                        #action='store_const',
                        #const=sum, 
                        #default=max,
                        help='')
    
    parser.add_argument('--translator_file_name', 
                        default="",
                        help='')   

    parser.add_argument('--DB_name', 
                        #action='store_const',
                        #const=sum, 
                        default="",
                        help='')
    
    args = parser.parse_args()
    
    return args.ID_file_name, args.DB_name, args.translator_file_name