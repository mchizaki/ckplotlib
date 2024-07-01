"""
* Written by CK
* Last update on June 27, 2024
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
from copy import copy

MPLSTYLE_DIRNAME = os.path.dirname( __file__ )

SYSTEM_STYLELIB_DIR = os.path.join(
    mpl.get_configdir(),
    'stylelib'
)


################################################################
# FontConstants
################################################################
#==============================================================#
# Arial for sans
#==============================================================#
try:
    from matplotlib._mathtext import _font_constant_mapping as mapping
    from matplotlib._mathtext import FontConstantsBase

    class ArialFontConstants( FontConstantsBase ):
        script_space   = 0.075
        subdrop        = 0.2
        sup1           = 0.4
        sub1           = 0.2
        sub2           = 0.3
        delta          = 0.075
        delta_slanted  = 0.3
        delta_integral = 0

    def _append_arial_font_constants():
        mapping.update( Arial = ArialFontConstants )

except:
    def _append_arial_font_constants():
        print( '[error] ckplotlib.mplstyle' )
        print( 'failed to set ArialFontConstants' )


#==============================================================#
# Times New Roman for serif
#==============================================================#
try:
    from matplotlib._mathtext import _font_constant_mapping as mapping
    from matplotlib._mathtext import ComputerModernFontConstants
    # from matplotlib._mathtext import STIXFontConstants
    class TimesNewRomanFontConstants( ComputerModernFontConstants ):
        pass

    # class TimesNewRomanFontConstants( STIXFontConstants ):
    #     pass

    def _append_times_font_constants():
        mapping.update( **{'Times New Roman': TimesNewRomanFontConstants} )

except:
    def _append_times_font_constants():
        print( '[error] ckplotlib.mplstyle' )
        print( 'failed to set TimesNewRomanFontConstants' )




################################################################
# use_mplstyle
################################################################
#==============================================================#
# use_mplstyle
#==============================================================#
def _get_mplstyle_path(
    mplstyle: str,
    dirs: list = []
) -> str | None:
    """
    search mplstyle file
    1. mplstyle (if "mplstyle" is path)
    2. search from directories sepecified as list of dirs
        - dirs[0]
        - dirs[1]
    """

    # mplstyle is written as path
    exists = os.path.isfile( mplstyle )
    if exists:
        return mplstyle


    fname = mplstyle
    FMT_LEN = 9
    FMT = '.mplstyle'

    if len( fname ) > FMT_LEN:
        wo_fmt = not fname[-FMT_LEN:] == FMT
    else:
        wo_fmt = True

    if wo_fmt:
        fname = f'{mplstyle}.mplstyle'

    for mplstyle_dir in dirs:
        path = os.path.join(
            mplstyle_dir,
            fname
        )
        exists = os.path.isfile( path )
        if exists:
            return path

    # error
    print( '[error] ckplotlib.mplstyle._get_mplstyle_path' )
    print( f'invalid mplstyle name "{mplstyle}".' )
    return None


def get_mplstyle_path(
    mplstyle: str,
    dirname: str|None = None
    ) -> str | None:
    """
    search & return mplstyle file
    if "mplstyle" is path:
        return "mplstyle"
    else:
        search from directories
        1. dirname [if is not None]
        2. current directory
        3. MPLSTYLE_DIRNAME
        4. SYSTEM_STYLELIB_DIR
    """

    search_dirs = [
        '.',
        MPLSTYLE_DIRNAME,
        SYSTEM_STYLELIB_DIR
    ]
    if dirname is not None:
        search_dirs.insert( 0, dirname )

    mplstyle = _get_mplstyle_path(
        mplstyle = mplstyle,
        dirs     = search_dirs
    )
    return mplstyle


def use_mplstyle(
    mplstyle: str,
    dirname: str|None = None,
    use: bool = False
    ) -> dict:
    """
    search mplstyle file
    if "mplstyle" is path:
        use "mplstyle"
    else:
        search from directories
        1. dirname [if is not None]
        2. current directory
        3. MPLSTYLE_DIRNAME
        4. SYSTEM_STYLELIB_DIR
    """
    mplstyle = get_mplstyle_path(
        mplstyle = mplstyle,
        dirname  = dirname
    )

    props = {}
    if mplstyle is not None:
        if use:
            plt.style.use( mplstyle )
        props.update( **_mplstyle2dict( mplstyle ) )

    return props




# def _use_mplstyle(
#     mplstyle: str,
#     dirs: list = []
# ):
#     """
#     search mplstyle file
#     1. mplstyle (if "mplstyle" is path)
#     2. search from directories sepecified as list of dirs
#         - dirs[0]
#         - dirs[1]
#     """

#     # mplstyle is written as path
#     exists = os.path.isfile( mplstyle )
#     if exists:
#         plt.style.use( mplstyle )
#         return


#     fname = f'{mplstyle}.mplstyle'
#     for mplstyle_dir in dirs:
#         path = os.path.join(
#             mplstyle_dir,
#             fname
#         )
#         exists = os.path.isfile( path )
#         if exists:
#             plt.style.use( path )
#             return

#     # error
#     print( '[error] ckplotlib.mplstyle._use_mplstyle' )
#     print( f'invalid mplstyle name "{mplstyle}".' )
#     sys.exit(1)




# def use_mplstyle(
#     mplstyle: str,
#     dirname: str|None = None
#     ):
#     """
#     search mplstyle file
#     if "mplstyle" is path:
#         use "mplstyle"
#     else:
#         search from directories
#         1. dirname [if is not None]
#         2. current directory
#         3. MPLSTYLE_DIRNAME
#         4. SYSTEM_STYLELIB_DIR
#     """

#     search_dirs = [
#         '.',
#         MPLSTYLE_DIRNAME,
#         SYSTEM_STYLELIB_DIR
#     ]
#     if dirname is not None:
#         search_dirs.insert( 0, dirname )

#     _use_mplstyle(
#         mplstyle = mplstyle,
#         dirs     = search_dirs
#     )


def _strip_comment( s: str ) -> str:
    """
    cited from matplotlib.cbook
    Strip everything from the first unquoted #.
    """
    pos = 0
    while True:
        quote_pos = s.find('"', pos)
        hash_pos = s.find('#', pos)
        if quote_pos < 0:
            without_comment = s if hash_pos < 0 else s[:hash_pos]
            return without_comment.strip()
        elif 0 <= hash_pos < quote_pos:
            return s[:hash_pos].strip()
        else:
            closing_quote_pos = s.find('"', quote_pos + 1)
            if closing_quote_pos < 0:
                raise ValueError(
                    f"Missing closing quote in: {s!r}. If you need a double-"
                    'quote inside a string, use escaping: e.g. "the \" char"')
            pos = closing_quote_pos + 1  # behind closing quote

def _mplstyle2dict( fname: str ) -> dict:
    rc_temp = {}
    with open( fname ) as fd:
        for line_no, line in enumerate( fd, 1 ):

            strippedline = _strip_comment( line )
            if not strippedline:
                continue
            tup = strippedline.split( ':', 1 )
            if len(tup) != 2:
                print(
                    'Missing colon in file %r, line %d (%r)',
                    fname, line_no, line.rstrip('\n')
                )
                continue
            key, val = tup
            key = key.strip()
            val = val.strip()
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]  # strip double quotes
            if key in rc_temp:
                print(
                    'Duplicate key in file %r, line %d (%r)',
                    fname, line_no, line.rstrip('\n')
                )
            # rc_temp[key] = (val, line, line_no)
            rc_temp[key] = val

    return rc_temp


#==============================================================#
# use_mplstyle_base
#==============================================================#
def use_mplstyle_base( use: bool = True ) -> dict:
    """
    - import base.mplstyle
    """
    base_mplstyle = f'{MPLSTYLE_DIRNAME}/base.mplstyle'
    if use:
        plt.style.use( base_mplstyle )
    return _mplstyle2dict( base_mplstyle )


#==============================================================#
# use_mplstyle_font
#==============================================================#
def use_mplstyle_font(
        mplstyle: str = 'arial',
        adjust_mathtext_space_ratio: float | None = 0.4,
        use: bool = True
) -> dict:
    """
    ### use_mplstyle
    - import font mplstyle
        - font: 'arial' or 'times' [defalut: 'arial']
        - font mplstyle is searched from
            if mplstyle is path:
                use mplstyle
            else:
                search from directories of
                1. currect directory
                2. f'{MPLSTYLE_DIRNAME}/font'
                3. SYSTEM_STYLELIB_DIR
    - adjust mathtext space
        - adjust_mathtext_space_ratio: [default: 0.4]
        (no change if the ratio is 1)
    """

    props = {}

    if   mplstyle == 'arial':
        props = use_mplstyle_arial( use = use )

    elif mplstyle == 'times':
        props = use_mplstyle_times( use = use )

    else:
        _mplstyle = mplstyle

        search_dirs = [
            '.',
            f'{MPLSTYLE_DIRNAME}/font',
            SYSTEM_STYLELIB_DIR
        ]

        mplstyle = _get_mplstyle_path(
            mplstyle = _mplstyle,
            dirs     = search_dirs
        )
        if mplstyle is not None:
            if use:
                plt.style.use( mplstyle )
            props = _mplstyle2dict( mplstyle )


    if adjust_mathtext_space_ratio is not None:
        adjust_mathtext_space(
            make_space_ratio = adjust_mathtext_space_ratio
        )

    return props


def use_mplstyle_arial( use: bool = True ) -> dict:
    mplstyle = f'{MPLSTYLE_DIRNAME}/font/arial.mplstyle'
    if use:
        plt.style.use( mplstyle )
    _append_arial_font_constants()
    return _mplstyle2dict( mplstyle )

def use_mplstyle_times( use: bool = True ) -> dict:
    mplstyle = f'{MPLSTYLE_DIRNAME}/font/times.mplstyle'
    if use:
        plt.style.use( mplstyle )
    _append_times_font_constants()
    return _mplstyle2dict( mplstyle )




################################################################
# adjust_mathtext_space
################################################################
try:
    from matplotlib._mathtext import Parser as Parser_
    Parser = copy( Parser_ )
    Parser._make_space_original = copy( Parser._make_space )
    Parser._make_space_ck_ratio = 1

    def _make_space( self, percentage ):
        new_percentage = percentage * self._make_space_ck_ratio
        return self._make_space_original( new_percentage )

    Parser._make_space = _make_space
    Parser_ = Parser

except:
    pass


def adjust_mathtext_space( make_space_ratio: float = 0.4 ):
    """
    if ratio is 1: space does not change
    """
    try:
        from matplotlib._mathtext import Parser
        Parser._make_space_ck_ratio = make_space_ratio
    except:
        pass
