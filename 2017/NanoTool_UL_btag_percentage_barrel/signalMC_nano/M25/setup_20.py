#import fileinput

if __name__ == "__main__":
    allFiles = open("input.txt", "r")

    for process in range(3):
    	template = open("/home/akobert/CMSSW_11_1_0_pre7/src/RData/2017/NanoTool_UL_btag_percentage_barrel/nano_Sample_20.py", "r")
        newFile = open("M25_" + str(process) + "_20.py", "a+")
       	readLine = allFiles.readline()
	oldline1 = "files = [\"/cms/xaastorage/NanoAOD/2018/JUNE19/UL/EGamma_RunA/branch_present/jetToolbox_dataA2018_0.root\", str(1.0), 1]"
	newline1 = "files = [\""+str(readLine[:-1])+"\", str(41.48 * 13290.0/495785.0), 1, \"mc\"]"
	
	oldline2 = "fname = \"DataA_present_UL_0\""
	newline2 = "fname = \"M25_UL_nano_"+str(process)+"_20\""

	for line in template:
		newFile.write(line.replace(oldline1, newline1).replace(oldline2, newline2))
 
	newFile.close()
	template.close()
