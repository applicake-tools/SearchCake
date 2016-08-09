#!/usr/bin/env python
import sys

# identification workflow for systeMHC

from ruffus import *
from applicake.apps.flow.jobid import Jobid
from applicake.apps.flow.merge import Merge
from applicake.apps.flow.split import Split
from searchengines.comet import Comet
from searchengines.iprophetpepxml2csv import IprohetPepXML2CSV
from searchengines.myrimatch import Myrimatch
from searchengines.xtandem import Xtandem
from prophets.interprophet import InterProphet
from prophets.peptideprophet import PeptideProphetSequence
from libcreate.spectrast import Spectrast
from multiprocessing import freeze_support
from systemhccake.netMHC import NetMHC
from systemhccake.netMHC2 import NetMHC2
from systemhccake.gibbscluster import GibbsCluster


@files("input.ini", "jobid.ini")
def jobid(infile, outfile):
    sys.argv = ['--INPUT', infile, '--OUTPUT', outfile]
    Jobid.main()


@follows(jobid)
@split("jobid.ini", "split.ini_*")
def split_dataset(infile, unused_outfile):
    sys.argv = ['--INPUT', infile, '--SPLIT', 'split.ini', '--SPLIT_KEY', 'MZXML']
    Split.main()


####################################################################
@transform(split_dataset, regex("split.ini_"), "rawmyri.ini_")
def myri(infile, outfile):
    sys.argv = ['--INPUT', infile, '--OUTPUT', outfile, '--THREADS', '4']
    Myrimatch.main()


@transform(myri, regex("rawmyri.ini_"), "myrimatch.ini_")
def peppromyri(infile, outfile):
    sys.argv = ['--INPUT', infile, '--OUTPUT', outfile, '--NAME', 'pepmyri']
    PeptideProphetSequence.main()


####### TANDEM NOT YET THERE ########################################
@transform(split_dataset, regex("split.ini_"), "rawtandem.ini_")
def tandem(infile, outfile):
    sys.argv = ['--INPUT', infile, '--OUTPUT', outfile, '--THREADS', '4']
    Xtandem.main()


@transform(tandem, regex("rawtandem.ini_"), "tandem.ini_")
def pepprotandem(infile, outfile):
    sys.argv = ['--INPUT', infile, '--OUTPUT', outfile, '--NAME', 'peptandem']
    PeptideProphetSequence.main()

####################################################################
@transform(split_dataset, regex("split.ini_"), "rawcomet.ini_")
def comet(infile, outfile):
    sys.argv = ['--INPUT', infile, '--OUTPUT', outfile, '--THREADS', '4']
    Comet.main()


@transform(comet, regex("rawcomet.ini_"), "comet.ini_")
def pepprocomet(infile, outfile):
    sys.argv = ['--INPUT', infile, '--OUTPUT', outfile, '--NAME', 'pepcomet']
    PeptideProphetSequence.main()


############################# TAIL: PARAMGENERATE ##################
@merge([pepprocomet], "ecollate.ini")
def merge_datasets(unused_infiles, outfile):
    sys.argv = ['--MERGE', 'comet.ini', '--MERGED', outfile]
    Merge.main()

############################## RunProphets #########################
@follows(merge_datasets)
@files("ecollate.ini_0", "datasetiprophet.ini")
def datasetiprophet(infile, outfile):
    sys.argv = ['--INPUT', infile, '--OUTPUT', outfile]
    InterProphet.main()


########################## MERGE ALL DATASETS ######################
@follows(datasetiprophet)
@files("datasetiprophet.ini", "convert2csv.ini")
def convert2csv(infile, outfile):
    sys.argv = ['--INPUT', infile, '--OUTPUT', outfile]
    IprohetPepXML2CSV.main()


####################### Spectrast ###################################
@follows(convert2csv)
@files("datasetiprophet.ini", "spectrast.ini")
def pepxml2spectrast(infile, outfile):
    sys.argv = ['--INPUT', infile, '--OUTPUT', outfile]
    Spectrast.main()

#################### GIBBS ########################################
@follows(pepxml2spectrast)
@files("convert2csv.ini", "Gibbs.ini")
def runGIBBS(infile, outfile):
    sys.argv = ['--INPUT', infile, "--OUTPUT", outfile]
    GibbsCluster.main()

################################ NETMHC #############################
@follows(runGIBBS)
@files("convert2csv.ini", "netMHC.ini")
def runNetMHC(infile, outfile):
    sys.argv = ['--INPUT', infile, "--OUTPUT", outfile]
    NetMHC.main()


@follows(pepxml2spectrast)
@files("convert2csv.ini", "netMHC.ini")
def runNetMHC2(infile, outfile):
    sys.argv = ['--INPUT', infile, "--OUTPUT", outfile]
    NetMHC2.main()

def run_libcreate_withNetMHC_WF(nrthreads=2):
    freeze_support()
    pipeline_run([runNetMHC], multiprocess=nrthreads)

def run_libcreate_WF(nrthreads=2):
    freeze_support()
    pipeline_run([pepxml2spectrast], multiprocess=nrthreads)

def run_libcreate_withNetMHC2_WF(nrthreads=2):
    freeze_support()
    pipeline_run([runNetMHC2], multiprocess=nrthreads)

