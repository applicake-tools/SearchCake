__author__ = 'wolski'

from applicake2.base.app import WrappedApp
from applicake2.base.coreutils.arguments import Argument
from applicake2.base.coreutils.keys import Keys, KeyHelp

class SearchEnginesBase(WrappedApp):
    def add_args(self):
         return [
            Argument(Keys.EXECUTABLE, KeyHelp.EXECUTABLE),
            Argument(Keys.WORKDIR, KeyHelp.WORKDIR),
            Argument(Keys.THREADS, KeyHelp.THREADS),
            Argument(Keys.MZXML, KeyHelp.MZXML),

            Argument('FRAGMASSERR', 'Fragment mass error', default=0.4),
            Argument('FRAGMASSUNIT', 'Unit of the fragment mass error',default='Da'),
            Argument('PRECMASSERR', 'Precursor mass error',default=15),
            Argument('PRECMASSUNIT', 'Unit of the precursor mass error',default='ppm'),
            Argument('MISSEDCLEAVAGE', 'Number of maximal allowed missed cleavages', default=1),
            Argument('ENZYME', 'Enzyme used to digest the proteins',default='Trypsin'),
            Argument('STATIC_MODS', 'List of static modifications',default='Carbamidomethyl (C)'),
            Argument('VARIABLE_MODS', 'List of variable modifications'),

            Argument('comet_fragment_bin_offset', 'wenguang added temp', default=0.4),
            Argument('comet_theoretical_fragment_ions', 'wenguang added temp', default=1),

            Argument('DBASE', 'Sequence database file with target/decoy entries'),
        ]
