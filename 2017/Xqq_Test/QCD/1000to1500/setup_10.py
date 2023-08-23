#import fileinput

if __name__ == "__main__":
    allFiles = open("input.txt", "r")

    for process in range(43):
    	template = open("/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/NanoTool_UL_btag_percentage/nano_Sample_10.py", "r")
        newFile = open("QCD1000to1500_" + str(process) + "_10.py", "a+")
       	readLine = allFiles.readline()
	oldline1 = "files = [\"/cms/xaastorage/NanoAOD/2018/JUNE19/UL/EGamma_RunA/branch_present/jetToolbox_dataA2018_0.root\", str(1.0), 1]"
	newline1 = "files = [\""+str(readLine[:-1])+"\", str(41.48 * 1207000.0/14491736.0), 1, \"QCD\"]"
	
	oldline2 = "fname = \"DataA_present_UL_0\""
	newline2 = "fname = \"QCD1000to1500_UL_nano_"+str(process)+"_10\""

	for line in template:
		newFile.write(line.replace(oldline1, newline1).replace(oldline2, newline2))
 
	newFile.close()
	template.close()