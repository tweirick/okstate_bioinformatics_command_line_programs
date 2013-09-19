
file_name = "4CL_pt4.faa.0.9.faa"
for line in open(file_name,'r'):
    if len(line)>0:

        if line[0] == ">":
            print(line.split()[0])
        else:
            print(line,end="")


