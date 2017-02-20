#!/usr/bin/env python
import sys

# identification workflow for systeMHC

from ruffus import *
from applicake2.apps.flow.jobid import Jobid
from applicake2.apps.flow.merge import Merge
from applicake2.apps.flow.split import Split
from applicake2.base import BasicApp
from applicake2.base.coreutils import IniInfoHandler
from searchengines.comet import Comet
from searchengines.iprophetpepxml2csv import IprohetPepXML2CSV
from searchengines.myrimatch import Myrimatch
from searchengines.xtandem import Xtandem
from prophets.interprophet import InterProphet
from prophets.peptideprophet import PeptideProphetSequence

from multiprocessing import freeze_support


@files("input.ini", "jobid.ini")
def jobid(infile, outfile):
    sys.argv = ['--INPUT', infile, '--OUTPUT', outfile]
    Jobid.main()


@follows(jobid)
@split("jobid.ini", "split.ini_*")
def split_dataset(infile, unused_outfile):
    sys.argv = ['--INPUT', infile, '--SPLIT', 'split.ini', '--SPLIT_KEY', 'MZXML']
    Split.main()


###################################################################################

@transform(split_dataset, regex("split.ini_"), "rawmyri.ini_")
def myri(infile, outfile):
    sys.argv = ['--INPUT', infile, '--OUTPUT', outfile, '--THREADS', '4']
    Myrimatch.main()


@transform(myri, regex("rawmyri.ini_"), "myrimatch.ini_")
def peppromyri(infile, outfile):
    sys.argv = ['--INPUT', infile, '--OUTPUT', outfile, '--NAME', 'pepmyri']
    PeptideProphetSequence.main()


### TANDEM ###################################################################

@transform(split_dataset, regex("split.ini_"), "rawtandem.ini_")
def tandem(infile, outfile):
    sys.argv = ['--INPUT', infile, '--OUTPUT', outfile, '--THREADS', '4']
    Xtandem.main()


@transform(tandem, regex("rawtandem.ini_"), "tandem.ini_")
def pepprotandem(infile, outfile):
    sys.argv = ['--INPUT', infile, '--OUTPUT', outfile, '--NAME', 'peptandem']
    PeptideProphetSequence.main()


###################################################################################

@transform(split_dataset, regex("split.ini_"), "rawcomet.ini_")
def comet(infile, outfile):
    sys.argv = ['--INPUT', infile, '--OUTPUT', outfile, '--THREADS', '4']
    Comet.main()


@transform(comet, regex("rawcomet.ini_"), "comet.ini_")
def pepprocomet(infile, outfile):
    sys.argv = ['--INPUT', infile, '--OUTPUT', outfile, '--NAME', 'pepcomet']
    PeptideProphetSequence.main()

############################# TAIL: PARAMGENERATE ##################################

@merge([pepprocomet, peppromyri], "ecollate.ini")
def merge_datasets(unused_infiles, outfile):
    sys.argv = ['--MERGE', 'comet.ini', '--MERGED', outfile]
    Merge.main()


@follows(merge_datasets)
@files("ecollate.ini_0", "datasetiprophet.ini")
def datasetiprophet(infile, outfile):
    sys.argv = ['--INPUT', infile, '--OUTPUT', outfile]
    InterProphet.main()


@follows(datasetiprophet)
@files("datasetiprophet.ini", "convert2csv.ini")
def convert2csv(infile, outfile):
    sys.argv = ['--INPUT', infile, '--OUTPUT', outfile]
    IprohetPepXML2CSV.main()


def run_peptide_WF(nrthreads=2):
    freeze_support()
    pipeline_run([convert2csv], multiprocess=nrthreads)


class PepidentWF(BasicApp):
    def add_args(self):
        #return #Myrimatch().add_args() + \
               #Xtandem().add_args() + \
               #Comet().add_args() + \
               #PeptideProphetSequence().add_args() + \
               #InterProphet().add_args() + \
        return IprohetPepXML2CSV().add_args()

    def run(self,log, info):
        ih = IniInfoHandler()
        ih.write(info,"pepinput.ini")
        run_peptide_WF()
        info = ih.read("convert2csv.ini")
        return info

if __name__ == "__main__":
    PepidentWF.main()
