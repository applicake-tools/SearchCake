import sys
from ruffus import *

from applicake2.base import BasicApp
from applicake2.base.coreutils import IniInfoHandler
from searchcake.pepidentWF import PepidentWF
from searchcake.prophets.proteinprophet import ProteinProphet
from multiprocessing import freeze_support

@files("input.ini", "pepwf.ini")
def peptidewf(infile, outfile):
    sys.argv = ['--INPUT', infile, '--OUTPUT', outfile]
    PepidentWF.main()


@files("pepwf.ini","protprophet.ini")
def proteinprophet(infile, outfile):
    sys.argv = ['--INPUT', infile, '--OUTPUT', outfile]
    ProteinProphet.main()

def run_pepprot_WF(nrthreads=2):
    freeze_support()
    pipeline_run([proteinprophet], multiprocess=nrthreads)

class Protid(BasicApp):
    def add_args(self):
        return PepidentWF().add_args() + \
               ProteinProphet().add_args()

    def run(self,log, info):
        ih = IniInfoHandler()
        ih.write(info,"input.ini")
        run_pepprot_WF()
        info = ih.read("protprophet.ini")
        return info

if __name__ == "__main__":
    Protid.main()
