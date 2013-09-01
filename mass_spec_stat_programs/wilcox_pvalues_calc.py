import rpy2.rpy_classic as rpy
rpy.set_default_mode(rpy.NO_CONVERSION)
rpy.set_default_mode(rpy.BASIC_CONVERSION)

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

args = parser.parse_args()
file_name = args.file_name
#The number of the fisrt column -1 of the number of the column in excel.
start_col = int(args.start_col_number)-1
#The number of the last column -1 of the number of the column in excel.
end_col   = int(args.end_col_number)

assert start_col >= 0
assert end_col > start_col
assert (end_col-start_col)%2 == 0 

mid_point = (end_col-start_col)/2

out_list  = []
for line in open(file_name,'r'):
    sl = line.split("\t")
    population_heavy = []
    population_light = []
    for el_i in range(start_col,mid_point):

        l = float( sl[el_i] )
        h = float( sl[el_i+mid_point] )
        if l != 0.0 and h != 0.0:
            population_light.append(l)       
            population_heavy.append(h)

    test_dict = rpy.r.wilcox_test(population_heavy,population_light)
    out_list.append(str(test_dict['p.value'][0]))

of = open(file_name+".wilcox-pvals.txt",'w')
of.write("\n".join(out_list))
of.close()

