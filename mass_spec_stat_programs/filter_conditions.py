"""
This program filters conditions with too few replicates. 
"""



import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--file_name',
                   help='Input the name of the file to be processed. ')
parser.add_argument('--start_col_number',
                   help='The number of the colum where replicates start.',
                   default=1)
parser.add_argument('--end_col_number',
                   help='The number of the column where the repicates end.',
                   default=10)
parser.add_argument('--n_conds',
                   help='The min number of allowd conditions',
                   default=2)
args = parser.parse_args()
file_name = args.file_name
start_col = int(args.start_col_number) - 1
end_col   = int(args.end_col_number)    
#This controls the minimum amount of replicates.
#The program will accept integer values of replicates larger
#than the given value
n_conds = int(args.n_conds)
once_bool = False

assert n_conds >= 1, "Must have at least one replicate."
assert (end_col-start_col)%2 == 0,"replicate cols must be an equal number."
assert start_col >= 0,"--start_col_number must be greater or equal to 1."

mid_point = (end_col-start_col)/2
out_list = []
for line in open(file_name,'r'):

    sl = line.split("\t")
    if once_bool:
       once_bool = False
    else:
        population_heavy = []
        population_light = []

        for el_i in range(start_col,mid_point):
            l = float( sl[el_i] )
            h = float( sl[el_i+mid_point] )
            if h != 0.0 and l != 0.0:
                population_heavy.append(l)
                population_light.append(h)

        if len(population_heavy) >= n_conds and len(population_light) >= n_conds:
            out_list.append(line)

of = open(file_name+".filtered.txt",'w')
of.write("".join(out_list))
of.close()

