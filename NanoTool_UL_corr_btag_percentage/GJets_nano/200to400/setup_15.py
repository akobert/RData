#import fileinput

if __name__ == "__main__":
    allFiles = open("input.txt", "r")

    for process in range(409):
    	template = open("/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr_btag_percentage/nano_Sample_15.py", "r")
        newFile = open("GJ200to400_" + str(process) + "_15.py", "a+")
       	readLine = allFiles.readline()
	oldline1 = "files = [\"/cms/xaastorage/NanoAOD/2018/JUNE19/UL/EGamma_RunA/branch_present/jetToolbox_dataA2018_0.root\", str(1.0), 1]"
	newline1 = "files = [\""+str(readLine[:-1])+"\", str(59.9 * 2183000.0/19755305.0), 1, \"mc\"]"
	
	oldline2 = "fname = \"DataA_present_UL_0\""
	newline2 = "fname = \"GJ200to400_UL_nano_"+str(process)+"_15\""

	for line in template:
		newFile.write(line.replace(oldline1, newline1).replace(oldline2, newline2))
 
	newFile.close()
	template.close()
