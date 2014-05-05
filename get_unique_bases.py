f = 'potex.fna'

f_set = set()
for line in open(f,'r'):
    if line[0] != ">":
        f_set.update(line)

print(f_set)
