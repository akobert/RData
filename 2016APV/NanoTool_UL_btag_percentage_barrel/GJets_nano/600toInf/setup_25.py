#import fileinput

if __name__ == "__main__":
    allFiles = open("input.txt", "r")

    for process in range(6):
    	template = open("/home/akobert/CMSSW_11_1_0_pre7/src/RData/2016APV/NanoTool_UL_btag_percentage_barrel/nano_Sample_25.py", "r")
        newFile = open("GJ600toInf_" + str(process) + "_25.py", "a+")
       	readLine = allFiles.readline()
	oldline1 = "files = [\"/cms/xaastorage/NanoAOD/2018/JUNE19/UL/EGamma_RunA/branch_present/jetToolbox_dataA2018_0.root\", str(1.0), 1]"
	newline1 = "files = [\""+str(readLine[:-1])+"\", str(19.5 * 93460.0/4661194.0), 1, \"GJ\"]"
	
	oldline2 = "fname = \"DataA_present_UL_0\""
	newline2 = "fname = \"GJ600toInf_UL_nano_"+str(process)+"_25\""

	for line in template:
		newFile.write(line.replace(oldline1, newline1).replace(oldline2, newline2))
 
	newFile.close()
	template.close()
