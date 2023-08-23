#import fileinput

if __name__ == "__main__":
    allFiles = open("input.txt", "r")

    for process in range(36):
    	template = open("/home/akobert/CMSSW_11_1_0_pre7/src/RData/2016/Xqq_Test/nano_Sample.py", "r")
        newFile = open("GJ100to200_" + str(process) + ".py", "a+")
       	readLine = allFiles.readline()
	oldline1 = "files = [\"/cms/xaastorage/NanoAOD/2018/JUNE19/UL/EGamma_RunA/branch_present/jetToolbox_dataA2018_0.root\", str(1.0), 1]"
	newline1 = "files = [\""+str(readLine[:-1])+"\", str(16.81 * 9238000.0/10003194.0), 1, \"GJ\"]"
	
	oldline2 = "fname = \"DataA_present_UL_0\""
	newline2 = "fname = \"GJ100to200_UL_nano_"+str(process)+"\""

	for line in template:
		newFile.write(line.replace(oldline1, newline1).replace(oldline2, newline2))
 
	newFile.close()
	template.close()
