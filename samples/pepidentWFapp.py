import os
import platform
import searchcake.libcreateWF as libcreateWF
import pandas as pd
import ntpath

import pepidentWFconfig as pwconf


def run(files, alleles, organism, massspec, MHC_class, workDir):
    pwconf.remove_ini_log()
    tmp = pwconf.setup_general() + pwconf.setup_search(massspec)
    if platform.system() == 'Linux':
        tmp += pwconf.setup_linux()
    else:
        tmp += pwconf.setup_windows()
    print(tmp)
    pwconf.write_ini(tmp)
    pwconf.peptidesearch_overwriteInfo({'INPUT': "input.ini",
                                        'MZXML': files,
                                        'DBASE': pwconf.getDB(organism),
                                        'OUTPUT': 'output.ini',
                                        'JOB_ID': workDir,
                                        'ALLELE_LIST': alleles})

    if MHC_class == 'class I':
        libcreateWF.run_libcreate_withNetMHC_WF(nrthreads=4)
    else:
        libcreateWF.run_libcreate_WF(nrthreads=4)


def processByBatch(allMzXMLs, sample, df):
    tmp = df[df["SampleID"] == sample]
    filesIds = tmp['ConvertedFileName']
#    print " ".format(filesIds)
    files = list()
    for i in filesIds:
        files  += [x for x in allMzXMLs if ntpath.basename(x) == i]
    if(len(files)==0):
        print("no files for sample" + sample)
        return 1
    #alleles = tmp['MHCAllele'].unique().tolist()
    alleles = tmp['MHCAllele_netMHCcons'].unique().tolist()
    if len(alleles) != 1:
        print "There are more than one allele set for this sample : {}".format(";".join(alleles))
    alleles = alleles[0].split(",")

    organism = tmp['Organism'].unique().tolist()
    if len(organism) != 1:
        print "There are more than one organism for this sample : {}".format(";".join(organism))
    organism = organism[0]

    massspec = tmp['MassSpectrometer'].unique().tolist()
    if len(massspec) != 1:
        print "There are more than one mass spec for this sample : {}".format(";".join(massspec))
    massspec = massspec[0]

    MHC_class = tmp['MHCClass'].unique().tolist()
    if len(MHC_class) != 1:
        print "There are more than one MHC class for this sample : {}".format(";".join(MHC_class))
    MHC_class = MHC_class[0]

    run(files, alleles, organism, massspec, MHC_class, sample)

def process_all_batches(files):
    path = "/mnt/Systemhc/Data/data_annotation_20170201.csv"
    df = pd.read_csv(path)

    cwd = os.getcwd()
    for sample in df["SampleID"].unique():
        dir = "{}/{}".format(cwd, sample)
        if not os.path.exists(dir):
            os.makedirs(dir)
        os.chdir(dir)
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{}<<<<<<<<<<<<<<<<<<<<<<<<<<<<<".format(sample)
        print "\n\n\n\n"
        processByBatch(files, sample, df)


if __name__ == '__main__':
    res = os.environ.get('SYSTEMHC')

    if res == None:
        print "SYSTEMHC not set"
        exit(1)
    files = pwconf.getMzXMLFiles("/mnt/Systemhc/data/SYSMHC00001/")
    process_all_batches(files)



