#!/usr/bin/env python
import os
import sys

from applicake.base.app import WrappedApp
from applicake.base.apputils import validation
from applicake.base.coreutils.arguments import Argument
from applicake.base.coreutils.keys import Keys, KeyHelp


class Spectrast(WrappedApp):
    """
    Create raw text library with iRT correction and without DECOYS_ from pepxml
    """
    def make_sysmlinks(self, info, log):
        if isinstance(info[Keys.MZXML], list):
            mzxmlslinks = info[Keys.MZXML]
        else:
            mzxmlslinks = [info[Keys.MZXML]]
        for f in mzxmlslinks:
            dest = os.path.join(info[Keys.WORKDIR], os.path.basename(f))
            print("------------------------")
            print('create symlink [%s] -> [%s]' % (f, dest))
            log.debug('create symlink [%s] -> [%s]' % (f, dest))
            os.symlink(f, dest)

    def add_args(self):
        return [
            Argument(Keys.WORKDIR, KeyHelp.WORKDIR),
            Argument(Keys.PEPXML, KeyHelp.PEPXML),
            Argument(Keys.MZXML, KeyHelp.MZXML),
            Argument('TPPDIR','tpp directory', default=''),
            Argument('MS_TYPE', 'ms instrument type', default="CID-QTOF"),
            Argument('CONSENSUS_TYPE', 'consensus type : consensus/best replicate',default='consensus'),
            Argument('DECOY', 'Decoy pattern', default='DECOY_'),
            Argument('IPROB', 'Probability to include', default ='0.8'),
            Argument('SPECTRASTDIR', 'spectrast utility directory', default='')
        ]

    def prepare_run(self, log, info):
        # symlink the pepxml and mzxml files first into a single directory
        pepxml = info[Keys.PEPXML]
        #peplink = os.path.join(info[Keys.WORKDIR], os.path.basename(info[Keys.PEPXML]))

        self.make_sysmlinks(info, log)

        info['SPLOG'] = os.path.join(info[Keys.WORKDIR], 'spectrast.log')
        # get iProb corresponding FDR for IDFilter

        consensustype = ""
        if info['CONSENSUS_TYPE'] == "consensus":
            consensustype = "C"
        elif info['CONSENSUS_TYPE'] == "best replicate":
            consensustype = "B"


        worksplib_base = os.path.join(info[Keys.WORKDIR], 'templib')
        worksplib = worksplib_base + ".splib"

        consensus_base = os.path.join(info[Keys.WORKDIR], 'consensus')
        consensus = consensus_base + '.splib'
        info['SPLIB'] = consensus

        command1 = "{exe} -L{slog} -c_RDY{decoy} -cI{mstype} -cP{iprob} -cN{rtcalib_base} {peplink}".format(
            exe = os.path.join(info['TPPDIR'], 'spectrast'),
            slog = info['SPLOG'],
            decoy = info['DECOY'],
            mstype = info['MS_TYPE'],
            iprob = info['IPROB'],
            rtcalib_base = worksplib_base,
            peplink = pepxml)

        command2 = "{exe} -L{slog} -cA{consensustype} -cN{output_name} {consensus_base}".format(
            exe = os.path.join(info['TPPDIR'], 'spectrast'),
            slog=info['SPLOG'],
            consensustype = consensustype,
            output_name = consensus_base,
            consensus_base = worksplib)

        lib2html_command = "{exe} {lib}".format(exe = os.path.join(info['SPECTRASTDIR'], 'Lib2HTML'), lib=consensus_base + ".splib")
        html2tsv = "python {exe} --input_file {consensus}.html --output_file {consensus_out}.tsvh".format(exe = os.path.join(info['SPECTRASTDIR'], 'spectrast_html_lib_2_csv.py'),
                                                                                                   consensus=consensus_base, consensus_out=consensus_base)
        rmconsesus = "rm {consensus}.html".format(consensus=consensus_base)
        return info, [command1, command2, lib2html_command, html2tsv, rmconsesus]


    def validate_run(self, log, info, exit_code, stdout):
        # Double check "Spectrast finished ..."
        if not " without error." in stdout:
            raise RuntimeError("SpectraST finished with some error!")

        validation.check_exitcode(log, exit_code)
        validation.check_file(log, info['SPLIB'])
        return info


if __name__ == "__main__":
    sys.argv = ['--INPUT', '/mnt/Systemhc/Data/process2/datasetiprophet.ini', '--OUTPUT', 'kufc.ini']
    Spectrast.main()
