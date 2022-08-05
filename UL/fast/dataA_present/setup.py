#import fileinput

if __name__ == "__main__":
    allFiles = open("input.txt", "r")

    for process in range(2850):
    	template = open("dataSample.py", "r")
        newFile = open("dataA_present" + str(process) + ".py", "a+")
       	readLine = allFiles.readline()
	oldline1 = "files = [\"/cms/xaastorage/NanoAOD/2018/JUNE19/UL/EGamma_RunA/branch_present/jetToolbox_dataA2018_0.root\", str(1.0), 1]"
	newline1 = "files = [\""+str(readLine[:-1])+"\", str(1.0), 1]"
	
	oldline2 = "fname = \"DataA_present_UL_0\""
	newline2 = "fname = \"DataA_present_UL_"+str(process)+"\""

	for line in template:
		newFile.write(line.replace(oldline1, newline1).replace(oldline2, newline2))
 
	newFile.close()
	template.close()
