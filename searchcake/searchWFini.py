def setup_windows():
    return '''
COMET_DIR=c:/users/wewol/prog/SearchCake_Binaries/Comet/windows/windows_64bit/
COMET_EXE=comet.exe
MYRIMATCH_DIR=c:/users/wewol/prog/SearchCake_Binaries/MyriMatch/windows/windows_64bit/
MYRIMATCH_EXE=myrimatch.exe
TPPDIR=c:/users/wewol/prog/SearchCake_Binaries/tpp/windows/windows_64bit/
'''


def setup_linux():
    return '''
COMET_DIR=/home/witold/prog/SearchCake_Binaries/Comet/linux
COMET_EXE=comet.exe

MYRIMATCH_DIR=/home/witold/prog/SearchCake_Binaries/MyriMatch/linux/linux_64bit
MYRIMATCH_EXE=myrimatch

TPPDIR=/home/witold/prog/SearchCake_Binaries/tpp/ubuntu14.04/bin/
'''


def setup_general():
    return """
LOG_LEVEL = DEBUG
COMMENT = WFTEST - newUPS TPP
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
DECOY = reverse_
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
    return '/home/witold/prog/SysteMHC_Data/fasta/CNCL_05640_2015_09_DECOY.fasta'

def getTubercoDB():
    return '/home/witold/prog/SysteMHC_Data/fasta/mycBovis.fasta'

def getHumanTubercoDB():
    return '/home/witold/prog/SysteMHC_Data/fasta/Mycobacterium_bovis_BCG_str_ATCC_35733_PATRIC_decoy_uniprot_20209_reviewed_canonical_irt_reverse_140724.fasta'

