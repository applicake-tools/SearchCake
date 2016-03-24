#!/usr/bin/env python
import sys

from multiprocessing import freeze_support
from ruffus import *

from searchcake.libcreate.spectrast2tsv import Spectrast2TSV
from searchcake.libcreate.spectrastrtcalib import SpectrastRTcalib


@files("input.ini", "rtcalib.ini")
def rtcalib(infile, outfile):
    sys.argv = ['--INPUT', infile, '--OUTPUT', outfile]
    SpectrastRTcalib.main()


@follows(rtcalib)
@files("rtcalib.ini", "totsv.ini")
def totsv(infile, outfile):
    sys.argv = ['--INPUT', infile, '--OUTPUT', outfile]
    Spectrast2TSV.main()

def run_libcreate_WF():
    freeze_support()
    pipeline_run([totsv])


if __name__ == '__main__':
    remove_ini_log()
    tmp = swi.setup_general() + swi.setup_search()
    if platform.system() == 'Linux':
        tmp += swi.setup_linux()
    else:
        tmp += swi.setup_windows()
    write_ini(tmp)

    path = '/home/witold/prog/SysteMHC_Data/mzXML/'
    files = swi.getMZXMLTub2PBMC10();
    files = map(lambda x : os.path.join(path, x), files)
    print (files)
    peptidesearch_overwriteInfo({'INPUT' : "input.ini", 'MZXML': files, 'DBASE' : swi.getDB(),'OUTPUT' : 'output.ini'})

    pepidentWF.run_peptide_WF()

    #ini file voodoo

    run_libcreate_WF()