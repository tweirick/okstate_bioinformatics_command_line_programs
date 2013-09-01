import rpy2.rpy_classic as rpy
from rpy2 import *
import rpy2.robjects as R
rpy.set_default_mode(rpy.NO_CONVERSION)
rpy.set_default_mode(rpy.BASIC_CONVERSION)

once_bool = True
file_name = ""

file_name = "17DMAG_2013-05-08.filtered.txt"
file_name = "AUY922_2013-05-08.filtered.txt"  
#file_name = "AUY922_normalized_HandL_intensities_08092013.txt.filtered.txt"

replicate_list = [
['Normalized intensity L AUY_BR1',[]],
['Normalized intensity L AUY_BR2',[]],
['Normalized intensity L AUY_BR3',[]],
['Normalized intensity L AUY_BR4',[]],
['Normalized intensity L AUY_BR5',[]],
['Normalized intensity H AUY_BR1',[]],  
['Normalized intensity H AUY_BR2',[]],  
['Normalized intensity H AUY_BR3',[]],  
['Normalized intensity H AUY_BR4',[]], 
['Normalized intensity H AUY_BR5',[]]]

start_col = 0
end_col   = 9

for line in open(file_name,'r'):
    sl = line.split("\t")
    
    population_heavy = []
    population_light = []

    for el_i in range(start_col,end_col,1):

        if float( sl[el_i] ) != 0.0:
            replicate_list[el_i][1].append( float( sl[el_i] ) )

print(file_name)
for replicate in replicate_list:
    rep_stats = rpy.r.shapiro_test( R.FloatVector(replicate[1]) )
    print(replicate[0])
    print("# non-zero elements: "+str(len(replicate[1])))
    print("statistic          : "+str(rep_stats["statistic"][0]))
    print("p-value            : "+str(rep_stats["p.value"][0]))




