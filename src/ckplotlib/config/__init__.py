"""
* Written by CK
"""
import os
import sys
import configparser
from dataclasses import dataclass

from .. import get_configdir

FNAME = 'config.ini'

CONFIG_FILE = os.path.join(
    os.path.dirname( __file__ ),
    FNAME
)
CONFIG_FILE_HOME = os.path.join(
    get_configdir(),
    FNAME
)

@dataclass
class CkFigureConfig:
    use_mplstyle_base: bool
    show_mplstyle_src: bool
    mplstyle_font: str
    cycle: str
    legend_bbox_to_anchor: tuple

    def __post_init__( self ):
        is_error = False
        if self.cycle != 'ck' and self.cycle != 'matplotlib':
            error_msg = 'invalid cycle'
            is_error = True

        if is_error:
            print( '[error] ckplotlib.config' )
            print( f'{error_msg} in the ".ini" file' )
            sys.exit(1)



def _str2tuple( liststr: str ) -> tuple:
    return tuple( map(
        float,
        liststr.strip('()').strip('[]').split(',')
    ))


#==============================================================#
# read initialization files
#==============================================================#
config_files = [ CONFIG_FILE ]
if os.path.isfile( CONFIG_FILE_HOME ):
    config_files.append( CONFIG_FILE_HOME )

iniread = configparser.RawConfigParser()
iniread.read( config_files )
ini_ckfigure = iniread[ 'ckfigure' ]


#==============================================================#
# get ckFigureConfig
#==============================================================#
ckFigureConfig = CkFigureConfig(
    use_mplstyle_base = ini_ckfigure.getboolean( 'use_mplstyle_base' ),
    show_mplstyle_src = ini_ckfigure.getboolean( 'show_mplstyle_src' ),
    mplstyle_font     = ini_ckfigure[ 'mplstyle_font' ],
    cycle             = ini_ckfigure[ 'cycle' ],
    legend_bbox_to_anchor = _str2tuple( ini_ckfigure[ 'legend_bbox_to_anchor' ] )
)

# from pprint import pprint
# pprint( vars( ckFigureConfig ) )
