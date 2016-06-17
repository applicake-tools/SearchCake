import os
import random
import glob
import platform
from applicake.base.apputils import dicts
import searchcake.pepidentWF as pepidentWF
import searchcake.libcreateWF as libcreateWF
import pandas as pd

from applicake.base import get_handler

def setup_windows():
    return '''
COMET_DIR=c:/users/wewol/prog/searchcake_binaries/Comet/windows/windows_64bit/
COMET_EXE=comet.exe
MYRIMATCH_DIR=c:/users/wewol/prog/searchcake_binaries/MyriMatch/windows/windows_64bit/
MYRIMATCH_EXE=myrimatch.exe
TPPDIR=c:/users/wewol/prog/searchcake_binaries/tpp/windows/windows_64bit/
'''

def spectrastParams():
    return '''
#Spectrast parameters
MS_TYPE=CID-QTOF
CONSENSUS_TYPE=consensus
DECOY=DECOY_
IPROB=0.1
'''

def netMHCParams():
    return '''
ALLELE_LIST=
'''

def setup_linux():
    return '''
COMET_DIR={systemhc}/searchcake_binaries/Comet/linux
COMET_EXE=comet.exe

MYRIMATCH_DIR={systemhc}/searchcake_binaries/MyriMatch/linux/linux_64bit
MYRIMATCH_EXE=myrimatch

TPPDIR={systemhc}/searchcake_binaries/tpp/ubuntu14.04/bin/
'''.format(systemhc=os.environ.get('SYSTEMHC'))


def setup_general():
    return """
LOG_LEVEL = DEBUG
COMMENT = bbWFTEST - newUPS TPP
"""


def setup_search():
    return '''
 # Search parameters
FDR_TYPE = iprophet-pepFDR
FRAGMASSERR = 0.5
FRAGMASSUNIT = Da
PRECMASSERR = 15
PRECMASSUNIT = ppm
MISSEDCLEAVAGE = 0
ENZYME = Nonspecific
STATIC_MODS =
VARIABLE_MODS = Oxidation (M)

## TPP
DECOY = DECOY_ 
IPROPHET_ARGS = MINPROB=0
MZXML =
DBASE =
    '''



def getTuberculosisData():
    return ['carone_20150801_QEp7_MiBa_SA_iRT_BCG_1.mzXML',
            'carone_20150801_QEp7_MiBa_SA_iRT_BCG_2.mzXML',
            'carone_20150801_QEp7_MiBa_SA_iRT_THP_1.mzXML',
            'carone_20150801_QEp7_MiBa_SA_iRT_THP_2.mzXML',
            'carone_Y150824_001_THP1_DDA.mzXML',
            'carone_Y150824_001_THP1_rBCG_DDA.mzXML'
            ]

def getMZXMLTub1():
    return ['PBMC1_Tubingen_120724_CB_Buffy18_W_20_Rep1_msms1_c.mzXML',
            'PBMC1_Tubingen_120724_CB_Buffy18_W_20_Rep2_msms2_c.mzXML',
            'PBMC1_Tubingen_120724_CB_Buffy18_W_20_Rep3_msms3_c.mzXML',
            'PBMC1_Tubingen_120724_CB_Buffy18_W_20_Rep4_msms4_c.mzXML',
            'PBMC1_Tubingen_120724_CB_Buffy18_W_20_Rep5_msms5_c.mzXML']

def getMZXMLTub2PBMC10():
    return ['PBMC10_Tubingen_130429_SKUG_Buffy83_W_1p25ug_20_50umx15cmColumn_60min3sDynExcl_3_msms4_c.mzXML',
            'PBMC10_Tubingen_130430_SKUG_Buffy83_W_1p25ug_20_15cm60min3sDynExcl_4_msms27_c.mzXML']

def getMZXMLTub3():
    return ['PBMC11_Tubingen_130510_SKUG_Buffy85_W_2p00ug_20_Rep_1_msms6_c.mzXML',
            'PBMC11_Tubingen_130510_SKUG_Buffy85_W_2p00ug_20_Rep_2_msms7_c.mzXML',
            'PBMC11_Tubingen_130510_SKUG_Buffy85_W_2p00ug_20_Rep_3_msms8_c.mzXML',
            'PBMC11_Tubingen_130510_SKUG_Buffy85_W_2p00ug_20_Rep_4_msms9_c.mzXML',
            'PBMC11_Tubingen_130510_SKUG_Buffy85_W_2p00ug_20_Rep_5_msms10_c.mzXML']


def getDB():
    return '{systemhc}/SysteMHC_Data/fasta/CNCL_05640_2015_09_DECOY.fasta'.format(systemhc=os.environ.get('SYSTEMHC'))

def getTubercoDB():
    return '{systemhc}/SysteMHC_Data/fasta/mycBovis.fasta'.format(systemhc=os.environ.get('SYSTEMHC'))


def getHumanTubercoDB():
    return '{systemhc}/SysteMHC_Data/fasta/Mycobacterium_bovis_BCG_str_ATCC_35733_PATRIC_decoy_uniprot_20209_reviewed_canonical_irt_reverse_140724.fasta'.format(systemhc=os.environ.get('SYSTEMHC'))



def write_ini(ini, dest="."):
    print 'Starting from scratch by creating new input.ini'
    with open(os.path.join(dest,"input.ini"), 'w+') as f:
        f.write(ini)



def remove_ini_log():
    for fl in glob.glob("*.ini*"):
        os.remove(fl)
    for fl in glob.glob("*.log*"):
        os.remove(fl)


def peptidesearch_overwriteInfo(overwrite):
    inifile = overwrite['INPUT']
    ih = get_handler(inifile)
    fileinfo = ih.read(inifile)
    info = dicts.merge(overwrite, fileinfo)
    ih.write(info,'input.ini')
    return info

def getMzXMLFiles(path,extension="mzXML"):
    import glob
    dd = path + "*." + extension
    print (dd)
    return glob.glob(dd)


def run(files, alleles, workDir):
    remove_ini_log()
    tmp = setup_general() + setup_search()
    if platform.system() == 'Linux':
        tmp += setup_linux()
    else:
        tmp += setup_windows()
    print(tmp)
    write_ini(tmp)
    peptidesearch_overwriteInfo( {'INPUT' : "input.ini", 'MZXML': files, 'DBASE' : getDB(),'OUTPUT' : 'output.ini', 'JOB_ID':workDir, 'ALLELE_LIST':alleles})
    libcreateWF.run_libcreate_WF(nrthreads= 2)


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
        processByBatch(files,sample , df)


if __name__ == '__main__':
    res = os.environ.get('SYSTEMHC')

    if res == None:
        print "SYSTEMHC not set"
        exit(1)
    files = getMzXMLFiles("/mnt/Systemhc/Data/PXD001872/")
    processAllBatches(files)
    #run(files, "dummydir" + str(random.randint(1000,9999)))



#pipeline_printout_graph ('flowchart.png','png',[copy2dropbox],no_key_legend = False) #svg
