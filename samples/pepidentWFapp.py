import os
import platform
import searchcake.libcreateWF as libcreateWF
import pandas as pd

import pepidentWFconfig as pwconf



def run(files, alleles, workDir):
    pwconf.remove_ini_log()
    tmp = pwconf.setup_general() + pwconf.setup_search()
    if platform.system() == 'Linux':
        tmp += pwconf.setup_linux()
    else:
        tmp += pwconf.setup_windows()
    print(tmp)
    pwconf.write_ini(tmp)
    pwconf.peptidesearch_overwriteInfo({'INPUT': "input.ini",
                                        'MZXML': files,
                                        'DBASE': pwconf.getDB(),
                                        'OUTPUT': 'output.ini',
                                        'JOB_ID': workDir,
                                        'ALLELE_LIST': alleles})

    libcreateWF.run_libcreate_withNetMHC_WF(nrthreads= 4)


def processByBatch(allMzXMLs, sample, df):
    import ntpath
    tmp = df[df["SampleID"] == sample]
    filesIds = tmp['FileName']
    res = list()
    for i in filesIds:
        res  += [x for x in allMzXMLs if ntpath.basename(x) == i]
    if(len(res)==0):
        print("no files for sample" + sample)
        return 1
    alleles = tmp['MHCAllele'].unique().tolist()
    if len(alleles) != 1:
        print "There are more than one allele set for this sample : {}".format(";".join(alleles))
    alleles = alleles[0].split(",")
    run(res, alleles, sample)

def processAllBatches(files):
    path = "{}/SysteMHC_Data/annotation/cleanedTable_id.csv".format(
        os.environ.get('SYSTEMHC'))
    df = pd.read_csv(path)
    #processByBatch(files,"Kowalewskid_160207_Rammensee_Germany_PBMC_Buffy83" , df)
    #return 0
    for sample in df["SampleID"].unique():
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{}<<<<<<<<<<<<<<<<<<<<<<<<<<<<<".format(sample)
        print "\n\n\n\n"
        processByBatch(files, sample, df)


if __name__ == '__main__':
    res = os.environ.get('SYSTEMHC')

    if res == None:
        print "SYSTEMHC not set"
        exit(1)
    files = pwconf.getMzXMLFiles("/mnt/Systemhc/Data/PXD001872/")
    processAllBatches(files)
    #run(files, "dummydir" + str(random.randint(1000,9999)))



#pipeline_printout_graph ('flowchart.png','png',[copy2dropbox],no_key_legend = False) #svg
