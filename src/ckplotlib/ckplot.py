"""
* Written by CK
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import FormatStrFormatter
from contextlib import contextmanager
from cycler import cycler, Cycler

import numpy as np
import numpy.typing as npt
import os
import sys
import copy

from .tool import deepmerge
from .savefig import savefig, SAVE_PARAMS
from .savecsv import savecsv
from .ticker import WideLogLocator, WideLogAutoMinorLocator

from .config import ckFigureConfig
from .mplstyle import use_mplstyle_base as _use_mplstyle_base
from .mplstyle import use_mplstyle_font, use_mplstyle
from .color import ckcolor, ckcmap

from .savecsv import addlinename
from .cycle import skip_cycle


################################################################
# parameters
################################################################
#==============================================================#
# legend
#==============================================================#
LGD_PARAMS = dict(
    bbox_to_anchor = ckFigureConfig.legend_bbox_to_anchor
)
HANDLE_LENGTH_ZERO = dict(
    handlelength = 0.5
)


#==============================================================#
# locator
#==============================================================#
LOG_LOC_MAJ = ticker.LogLocator(
    base     = 10,
    numticks = 15
)
LOG_LOC_MIN = ticker.LogLocator(
    base     = 10,
    subs     = (2,3,4,5,6,7,8,9),
    numticks = 15
)

WIDE_LOG_LOC_MAJ = WideLogLocator(
    base     = 10,
    numticks = 15
)
WIDE_LOG_LOC_MIN = WideLogAutoMinorLocator()


#==============================================================#
# formatter
#==============================================================#
def log_scalar_formatter( x, pos ):
    """
    if logscale => ticklabels like 0.1, 1, 10, 100, ...
    """
    if x < 10:
        return "%.g" % x
    else:
        return "%d" % x

LOG_SCALAR_FMT_MAJ = ticker.FuncFormatter( log_scalar_formatter )




################################################################
# graph function
################################################################
def _is_inline() -> bool:
    return 'inline' in plt.rcParams[ 'backend' ]



def legend_adjust_handle_length(
    lines: list[plt.Line2D],
    *arg,
    **kwargs
) -> None:

    new_kwargs = dict( **LGD_PARAMS )
    new_kwargs.update( **kwargs )

    # nallow the spacing between the marker & the character if handle does not use lines
    all_line_styles_none = all([
        line.get_linestyle() == 'None' for line in lines
    ])
    if all_line_styles_none:
        new_kwargs.update( **HANDLE_LENGTH_ZERO )

    plt.legend( *arg, **new_kwargs )



def modify_loglim(
    lim: list,
    exponent_range_max: float = 1e8,
    max_is_fixed: bool = True,
    min_is_fixed: bool = False,
    minima: list | npt.NDArray | None = None,
    maxima: list | npt.NDArray | None = None
) -> None:
    modified = False
    max_range = 10**exponent_range_max
    minima_maxima_exist = minima is not None and maxima is not None

    if minima_maxima_exist:
        minima = np.array( minima )
        maxima = np.array( maxima )

    if all([ max_is_fixed, min_is_fixed ]):
        return modified

    elif max_is_fixed:
        new_min = lim[1] / max_range

        if lim[0] < new_min:
            lim[0] = new_min

            if minima_maxima_exist:
                is_lower = maxima < new_min
                if np.any( is_lower ):
                    print( f'  * lines of indices {np.where( is_lower )[0]} are out of range.' )
                    _new_min = np.min( minima[ ~is_lower ] )
                    if _new_min > new_min:
                        lim[0] = _new_min

            modified = True
        return modified


    elif min_is_fixed:
        new_max = lim[0] * max_range

        if lim[1] > new_max:
            lim[1] = new_max

            if minima_maxima_exist:
                is_upper = minima > new_max
                if np.any( is_upper ):
                    print( f'  * lines of indices {np.where( is_upper )[0]} are out of range.' )
                    _new_max = np.max( maxima[ ~is_upper ] )
                    if _new_max < new_max:
                        lim[1] = _new_max

            modified = True
        return modified

    else:
        print( '[error] modify_loglim' )
        print( 'either max_is_fixed or min_is_fixed must be True.' )
        sys.exit(1)

# def modify_loglim(
#     lim,
#     exponent_range_max = 1e8,
#     max_is_fixed = True,
#     min_is_fixed = False,
#     y_minima = None,
#     y_maxima = None
# ):
#     modified = False
#     max_range = 10**exponent_range_max
#     minima_maxima_exist = y_minima is not None and y_maxima is not None

#     if minima_maxima_exist:
#         y_minima = np.array( y_minima )
#         y_maxima = np.array( y_maxima )

#     if all([ max_is_fixed, min_is_fixed ]):
#         return modified

#     elif max_is_fixed:
#         new_min = lim[1] / max_range

#         if lim[0] < new_min:
#             lim[0] = new_min

#             if minima_maxima_exist:
#                 is_lower = y_maxima < new_min
#                 if np.any( is_lower ):
#                     lim[0] = np.min( y_minima[ ~is_lower ] )
#             modified = True

#         return modified


#== Text ===================================#
def annotate(
    ax: plt.Axes,
    text: str,
    fontsize: str | int = 'x-small',
    border:    bool = True,
    loc: str | None = None,
    x: float | None = None,
    y: float | None = None,
    ha:  str | None = None,
    va:  str | None = None,
    **kwargs
) -> None:
    """
    * "x" and "y" have priority ober "loc".
    * note:
        - lowerleft  of ax = (0, 0)
        - upperright of ax = (1, 1)
    """
    boxdict = dict(
        facecolor = 'None'
    )
    boxdict.update(
        **kwargs.get( 'bbox', {} )
    )

    posx = 1.05
    posy = 0.015
    _ha  = 'left'
    _va = 'top'

    if loc == 'bottom':
        posx, posy = 1.05, -0.2
        _va = 'bottom'
        _ha = 'left'
    elif loc == 'inner lower left':
        posx, posy = 0.03, 0.03
        _va = 'bottom'
        _ha = 'left'
    elif loc == 'inner lower right':
        posx, posy = 0.97, 0.03
        _va = 'bottom'
        _ha = 'right'
    elif loc == 'inner upper left':
        posx, posy = 0.03, 0.97
        _va = 'top'
        _ha = 'left'
    elif loc=='inner upper right':
        posx, posy = 0.97, 0.97
        _va = 'top'
        _ha = 'right'
    else:
        pass

    if x is not None: posx = x
    if y is not None: posy = y
    if ha is not None: _ha = ha
    if va is not None: _va = va

    if border:
        boxdict.update( linewidth = 1 )  # The default padding is pad = 0.3 [the unit where fontsize is 1]
    else:
        boxdict.update( linewidth = 0 )
    _kwargs = { k: v for k, v in kwargs.items() if k != 'bbox' }
    ax.text(
        x    = posx,
        y    = posy,
        s    = text,
        size = fontsize,
        transform = ax.transAxes,
        verticalalignment   = _va,
        horizontalalignment = _ha,
        bbox = boxdict,
        **_kwargs
    )


SUPTITLE_DELTA = 0.15
def _calc_suptitle_y( rows: int ) -> float:
    y = 1
    y += SUPTITLE_DELTA/2 if rows==1 else SUPTITLE_DELTA/rows
    return y

def suptitle(
    t: str,
    ax: plt.Axes | None = None,
    **kwargs
) -> plt.Text:
    if ax is None: ax = plt.gca()
    rows = ax.get_gridspec().nrows
    title_y = _calc_suptitle_y( rows )

    props = dict(
        y        = title_y,
        fontsize = 'xx-large',
        va       = 'bottom'
    )
    props.update( **kwargs )

    return plt.suptitle( t, **props )




#== range ==================================#
# def get_lines_x_minima_maxima( lines ):
#     x_minima = []; x_maxima = []
#     for line in lines:
#         x, _ = line.get_data()

#         x_minima.append( np.nanmin(x) )
#         x_maxima.append( np.nanmax(x) )

#     return (
#         x_minima,
#         x_maxima
#     )

def get_lines_x_minima_maxima(
    lines: list[plt.Line2D],
    ymin: int | float | None = None,
    ymax: int | float | None = None
) -> tuple[list[float]]:
    x_minima = []; x_maxima = []
    for line in lines:
        x, y = line.get_data()

        # xmin_ = x[0]  if xmin is None else xmin
        # xmax_ = x[-1] if xmax is None else xmax

        ymin_ = np.min( y ) if ymin is None else ymin
        ymax_ = np.max( y ) if ymax is None else ymax

        new_x = x[ ( y >= ymin_ ) & ( y <= ymax_ ) ]

        x_minima.append( np.nanmin(new_x) )
        x_maxima.append( np.nanmax(new_x) )

    return (
        x_minima,
        x_maxima
    )

def get_lines_y_minima_maxima(
    lines: list[plt.Line2D],
    xmin: int | float | None = None,
    xmax: int | float | None = None
) -> tuple[list[float]]:
    y_minima = []; y_maxima = []
    for line in lines:
        x, y = line.get_data()

        # xmin_ = x[0]  if xmin is None else xmin
        # xmax_ = x[-1] if xmax is None else xmax

        xmin_ = np.min( x ) if xmin is None else xmin
        xmax_ = np.max( x ) if xmax is None else xmax

        new_y = y[ ( x >= xmin_ ) & ( x <= xmax_ ) ]


        y_minima.append( np.nanmin(new_y) )
        y_maxima.append( np.nanmax(new_y) )

    return (
        y_minima,
        y_maxima
    )


def axes_log_limits( xmin: float, xmax: float ) -> list[int]:
    if xmin == 0:
        log_xmin = 0
    else:
        log_xmin = 10**np.floor( np.log10(xmin) )

    log_xmax = 10**np.ceil ( np.log10(xmax) )

    return [ log_xmin, log_xmax ]

def axes_margin_limits(
    xmin: float,
    xmax: float,
    xscale: str,
    margins: list[float]
) -> tuple[float]:
    if xscale == "linear":
        diff = abs( xmax - xmin )
        delta_xs = [ diff * margin for margin in margins ]

        return (
            xmin - delta_xs[0],
            xmax + delta_xs[1]
        )

    elif xscale == "log":
        xmax_log10 = np.log10( xmax )
        xmin_log10 = np.log10( xmin )
        diff = abs( xmax_log10 - xmin_log10 )
        delta_xs = [ diff * margin for margin in margins ]

        return (
            10**( xmin_log10 - delta_xs[0] ),
            10**( xmax_log10 + delta_xs[1] )
        )

    else:
        print( '[error] scale error in axes_margin_limits.' )
        print( f'invalid value of xscale: {xscale}' )
        sys.exit(1)


def xlim_margin(
    ax: plt.Axes,
    xrange: list | None = None,
    margins: list[float] = [
        plt.rcParams.get( 'axes.xmargin' ),
        plt.rcParams.get( 'axes.xmargin' )
    ]
) -> tuple[float]:
    """
    * ax
    * xrange
        - list => [xmin, xmax]
        - None => read by ax.get_xlim
    * [optional] margins
        - [margin_left, margin_right]
    """
    xrange = ax.get_xlim() if xrange is None else xrange
    new_xrange = axes_margin_limits(
        *xrange,
        xscale  = ax.get_xscale(),
        margins = margins
    )

    return new_xrange


def ylim_margin(
    ax: plt.Axes,
    yrange: list | None = None,
    margins: list[float] = [
        plt.rcParams.get( 'axes.ymargin' ),
        plt.rcParams.get( 'axes.ymargin' )
    ]
) -> tuple[float]:
    """
    * ax
    * yrange
        - list => [ymin, ymax]
        - None => read by ax.get_ylim
    * [optional] margins
        - [margin_bottom, margin_top]
    """
    yrange = ax.get_ylim() if yrange is None else yrange
    new_yrange = axes_margin_limits(
        *yrange,
        xscale  = ax.get_yscale(),
        margins = margins
    )

    return new_yrange


# def ticks( numticks, xmin, xmax, dx=1 ):
#     ticks = np.arange(
#         np.floor( xmin ), np.ceil( xmax ), dx
#     )
#     minorticks = np.array([])
#     while ( np.size( ticks ) > numticks ):
#         minorticks = np.append(
#             minorticks, ticks[1::2]
#         )
#         ticks = ticks[::2]
#     minorticks = np.sort(minorticks)
#     return ticks, minorticks


# def logticks( numticks, xmin, xmax ):
#     ticks, minorticks = ticks(
#         numticks = numticks,
#         xmin = np.log10( xmin ),
#         xmax = np.log10( xmax )
#     )
#     return 10**ticks, 10**minorticks


class _CkAxesProps:

    def __init__(
        self,
        xmin, xmax,
        ymin, ymax
    ):
        self.xmin = xmin;  self.xmax = xmax
        self.ymin = ymin;  self.ymax = ymax

        self.xlim = np.array([ xmin, xmax ])
        self.ylim = np.array([ ymin, ymax ])


    def set_all_positive( self ):
        self.all_x_is_positive = ( self.xlim > 0 ).all()
        self.all_y_is_positive = ( self.ylim > 0 ).all()




################################################################
# CkFigure class
################################################################
class CkFigure:

    fig = True
    save_props = dict(
        dirname     = None,
        fname       = None,
        png         = ckFigureConfig.png,
        svg         = ckFigureConfig.svg,
        png_dpi     = ckFigureConfig.png_dpi,
        svg_dpi     = ckFigureConfig.svg_dpi,
        save_params = SAVE_PARAMS
    )

    # export plotted data as csv file
    csv = ckFigureConfig.csv
    savecsv_props = dict(
        dirname    = None,
        subdirname = None,
        fname      = None,
        header     = None,
        common_x   = True,
        subplot_common_x = False
    )

    plt_props = {}
    plt_prop_kwargs = {}

    # plt_props = dict(
    #     xlabel = 'Temperature (K)',
    #     yscale = 'log'
    # )

    # plt_prop_kwargs = dict(
    #     legend = dict(
    #         bbox_to_anchor = (1, 1)
    #     )
    # )

    # annotate
    annotate_str = None
    annotate_props = dict(
        fontsize = 'x-small',
        border   = True,
        loc      = 'bottom',
        x        = None,
        y        = None,
        ha       = None,
        va       = None
    )

    # padding from minimum and maximum values in the graph,
    # specified as a percentage of the size of Axis [from 0 to 1]
    axes_xmargins = [ 0.05, 0.05 ]
    axes_ymargins = [ 0.05, 0.05 ]

    # x/ylog_intlim
    # - axis range = [10^a, 10^b] (a & b are integer)
    # - this props is valid if plt.xscale/yscale is 'log'
    is_xlog_intlim = False
    is_ylog_intlim = True

    # x/ylog_format
    # - use exponential notation
    # - this props is valid if plt.xscale/yscale is 'log'
    is_xlog_format = True
    is_ylog_format = True

    # minimum/maximum value that determines the display range of graph
    # - None => not specified: automatically determinted
    xmin = None; xmax = None
    ymin = None; ymax = None
    is_ylim_adjust_xlim = True

    no_line     = False
    adjust_lim  = True


    # * this props is valid if plt.xscale is 'log'
    set_xlog_range_max = False
    set_xlog_range_max_props = dict(
        exponent_range_max = 8,
        max_is_fixed       = True,
        min_is_fixed       = False
    )
    # * this props is valid if plt.yscale is 'log'
    set_ylog_range_max = False
    set_ylog_range_max_props = dict(
        exponent_range_max = 8,
        max_is_fixed       = True,
        min_is_fixed       = False
    )

    xlog_ticker_exponent_range_thr = 10
    ylog_ticker_exponent_range_thr = 10


    # use common axis range if fig includes multiple ax subplots
    common_xlim = True
    common_ylim = True

    save_original_fig = True


    #==============================================================#
    # constructor
    #==============================================================#
    def __init__(
        self,
        **kwargs
    ):
        for key, val in kwargs.items():
            if key in vars( self.__class__ ):
                setattr( self, key, val )


    #==============================================================#
    # set graph data
    #==============================================================#
    def setattr_ax_data(
            self,
            ax:    plt.Axes | None               = None,
            lines: list[mpl.lines.Line2D] | None = None,
            xmin:  float | None                  = None,
            xmax:  float | None                  = None,
            ymin:  float | None                  = None,
            ymax:  float | None                  = None
        ) -> tuple[ list[float], list[float] ]:
        """
        ### How to use:
        * if both arguments of "ax" and "lines" are used, "lines" has priority over "ax.get_lines()".

        ### What this function does:
        ax.ckAxesProps.xmin
        * add ckAxesProps to the instance variables of "ax".
        (ckAxesProps is instance of class _CkAxesProps)
        * ax.ckAxesProps includes member variables of "xmin", "xmax", "ymin", "ymax", "xlim", and "ylim"
        """

        if ax is None: ax = plt.gca()

        # "lines" has priority over "ax.get_lines()"
        lines = ax.get_lines() if lines is None else lines

        ### check
        if len( lines ) == 0:
            print( '[error] plot data does not exist.' )
            sys.exit(1)


        ### get min & max
        x_minima, x_maxima = get_lines_x_minima_maxima( lines )
        y_minima, y_maxima = get_lines_y_minima_maxima( lines )


        ### set data
        ax.ckAxesProps = _CkAxesProps(
            xmin = min( x_minima ),
            xmax = max( x_maxima ),
            ymin = min( y_minima ),
            ymax = max( y_maxima )
        )

        if xmin is not None: ax.ckAxesProps.xlim[0] = xmin
        if xmax is not None: ax.ckAxesProps.xlim[1] = xmax
        if ymin is not None: ax.ckAxesProps.ylim[0] = ymin
        if ymax is not None: ax.ckAxesProps.ylim[1] = ymax


        ### adjust lims
        # adjust y range in x range
        if self.is_ylim_adjust_xlim:
            y_minima, y_maxima = get_lines_y_minima_maxima(
                lines = lines,
                xmin  = ax.ckAxesProps.xlim[0],
                xmax  = ax.ckAxesProps.xlim[1],
            )
            ax.ckAxesProps.ylim[0] = min( y_minima )
            ax.ckAxesProps.ylim[1] = max( y_maxima )

        return (
            ax.ckAxesProps.xlim,
            ax.ckAxesProps.ylim
        )



    #==============================================================#
    # set graph style
    #==============================================================#
    def set_figure_style(
        self,
        fig: plt.Figure | None = None
    ) -> list[ _CkAxesProps ]:

        if fig is None:
            fig = plt.gcf()

        if len( fig.get_axes() ) == 0:
            print( '[error] CkFigure.set_figure_style' )
            print( 'plot axes do not exist.' )
            sys.exit(1)

        no_line = False
        for ax in fig.get_axes():
            if len( ax.get_lines() )==0:
                no_line = True
        if no_line:
            self.no_line = True

        if self.no_line: self.adjust_lim = False

        if self.adjust_lim:

            #--------------------------------------------------------------#
            # get xmin, xmax, ymin, ymax from plotted data
            #--------------------------------------------------------------#
            x_minima = [];  x_maxima = []
            y_minima = [];  y_maxima = []
            for ax in fig.get_axes():
                self.setattr_ax_data( ax = ax )

                if not hasattr( ax, 'ckAxesProps' ):
                    print( '[error] CkFigure.set_figure_style' )
                    print( 'ckAxesProps is not found in ax members.' )
                    sys.exit(1)

                x_minima.append( ax.ckAxesProps.xmin )
                x_maxima.append( ax.ckAxesProps.xmax )
                y_minima.append( ax.ckAxesProps.ymin )
                y_maxima.append( ax.ckAxesProps.ymax )


            #--------------------------------------------------------------#
            # common xlim/ylim settings
            #--------------------------------------------------------------#
            xmin = None;  xmax = None
            if self.common_xlim:
                xmin = min( x_minima )
                xmax = max( x_maxima )

            ymin = None;  ymax = None
            if self.common_ylim:
                ymin = min( y_minima )
                ymax = max( y_maxima )


            if self.is_ylim_adjust_xlim:
                if self.common_xlim and self.common_ylim:
                    y_minima = [];  y_maxima = []
                    for ax in fig.get_axes():
                        self.setattr_ax_data(
                            ax = ax,
                            xmin = xmin,
                            xmax = xmax
                        )
                        y_minima.append( ax.ckAxesProps.ylim[0] )
                        y_maxima.append( ax.ckAxesProps.ylim[1] )

                    ymin = min( y_minima )
                    ymax = max( y_maxima )

            # update all axes xlim & ylim
            for ax in fig.get_axes():
                if self.common_xlim:
                    ax.ckAxesProps.xlim = np.array([ xmin, xmax ])
                if self.common_ylim:
                    ax.ckAxesProps.ylim = np.array([ ymin, ymax ])


            #--------------------------------------------------------------#
            # if specify xmin, xmax, ymin, or ymax by instance variables
            #--------------------------------------------------------------#
            _xrange_update       = False
            _xrange_update_props = {}
            if self.xmin is not None:
                _xrange_update = True
                _xrange_update_props.update( xmin = self.xmin )
            if self.xmax is not None:
                _xrange_update = True
                _xrange_update_props.update( xmax = self.xmax )

            if self.is_ylim_adjust_xlim:
                if _xrange_update:
                    y_minima = []
                    y_maxima = []
                    for ax in fig.get_axes():
                        self.setattr_ax_data(
                            ax = ax,
                            **_xrange_update_props
                        )
                        y_minima.append( ax.ckAxesProps.ylim[0] )
                        y_maxima.append( ax.ckAxesProps.ylim[1] )

                    ymin = min( y_minima )
                    ymax = max( y_maxima )

                    if self.common_ylim:
                        ax.ckAxesProps.ylim = np.array([ ymin, ymax ])


            #--------------------------------------------------------------#
            # if specify xmin, xmax, ymin, or ymax by instance variables
            #--------------------------------------------------------------#
            for ax in fig.get_axes():
                if self.xmin is not None: ax.ckAxesProps.xlim[0] = self.xmin
                if self.xmax is not None: ax.ckAxesProps.xlim[1] = self.xmax
                if self.ymin is not None: ax.ckAxesProps.ylim[0] = self.ymin
                if self.ymax is not None: ax.ckAxesProps.ylim[1] = self.ymax


        #--------------------------------------------------------------#
        # result
        #--------------------------------------------------------------#
        ckAxesProps_results: list[_CkAxesProps] = []
        for ax in fig.get_axes():
            ckAxesProps = self.set_figure_style_ax(
                ax = ax,
                setattr_ax_data = False
            )
            ckAxesProps_results.append( ckAxesProps )

        return ckAxesProps_results



    def set_figure_style_ax(
        self,
        ax:    plt.Axes               = None,
        lines: list[mpl.lines.Line2D] = None,
        setattr_ax_data: bool         = True
    ) -> _CkAxesProps:

        if ax is None: ax = plt.gca()
        plt.sca( ax )

        if setattr_ax_data:
            self.setattr_ax_data(
                ax    = ax,
                lines = lines
            )

        if self.no_line: self.adjust_lim = False
        if self.adjust_lim and not hasattr( ax, 'ckAxesProps' ):
            print( '[error] CkFigure.set_figure_style_ax' )
            print( 'ckAxesProps is not found in ax members.' )
            sys.exit(1)

        # "lines" has priority over "ax.get_lines()"
        lines = ax.get_lines() if lines is None else lines



        #################
        # plt_props & plt_props_kwargs
        #################
        """
        * formats of "plt_props" & "plt_props_kwargs" are as followings:
            plt_props = dict(
                xlabel = 'Temperature (K)',
                yscale = 'log'
            )

            plt_prop_kwargs = dict(
                legend = dict(
                    bbox_to_anchor = (1, 1)
                )
            )
        """
        for key, val in self.plt_prop_kwargs.items():
            if not isinstance( val, dict ):
                print( f'[error] self.plt_prop_kwargs[{key}] must be dict.' )
                sys.exit(1)

        for key, val in self.plt_props.items():
            kwargs = self.plt_prop_kwargs.get( key, {} )

            if key == 'legend':
                legend_adjust_handle_length( lines, val, **kwargs )
                continue

            # getattr( plt, key )( val, **kwargs )
            pltfunc = getattr( plt, key, None )
            if pltfunc is None:
                getattr( ax, f'set_{key}' )( val, **kwargs )
            else:
                pltfunc( val, **kwargs )

        for key, val in self.plt_prop_kwargs.items():
            if key in self.plt_props: continue
            kwargs = val

            if key == 'legend':
                legend_adjust_handle_length( lines, **kwargs )
                continue

            # getattr( plt, key )( **kwargs )
            pltfunc = getattr( plt, key, None )
            if pltfunc is None:
                getattr( ax, f'set_{key}' )( **kwargs )
            else:
                pltfunc( **kwargs )



        #################
        # Anotation
        #################
        if self.annotate_str is not None:
            annotate(
                ax   = ax,
                text = self.annotate_str,
                **self.annotate_props
            )


        #################
        # xlim, ylim
        #################
        if self.no_line: self.adjust_lim = False
        if not self.adjust_lim:
            return getattr( ax, 'ckAxesProps', None )


        # reset lim
        ax.relim()
        ax.autoscale()

        ax.ckAxesProps.is_xlog = ax.get_xscale() == 'log'
        ax.ckAxesProps.is_ylog = ax.get_yscale() == 'log'

        ax.ckAxesProps.set_all_positive()
        skip_adjust_xlim = any([
            ax.ckAxesProps.is_xlog and ( not ax.ckAxesProps.all_x_is_positive and not self.set_xlog_range_max ),
            ax.ckAxesProps.is_xlog == 'symlog',
            ax.ckAxesProps.is_xlog == 'logit'
        ])
        skip_adjust_ylim = any([
            # ax.ckAxesProps.is_ylog and not ax.ckAxesProps.all_y_is_positive,
            ax.ckAxesProps.is_ylog and ( not ax.ckAxesProps.all_y_is_positive and not self.set_ylog_range_max ),
            ax.ckAxesProps.is_ylog == 'symlog',
            ax.ckAxesProps.is_ylog == 'logit'
        ])



        for (
            is_log, is_log_intlim,
            lim,
            skip_adjust_lim
        ) in zip(
            #
            [ ax.ckAxesProps.is_xlog,  ax.ckAxesProps.is_ylog  ],
            [ self.is_xlog_intlim, self.is_ylog_intlim ],
            #
            [ ax.ckAxesProps.xlim, ax.ckAxesProps.ylim ],
            #
            [ skip_adjust_xlim, skip_adjust_ylim ]
        ):
            if skip_adjust_lim: continue
            if is_log and is_log_intlim:
                lim_ = axes_log_limits( *lim )
                lim[0] = lim_[0]
                lim[1] = lim_[1]

        # max_range
        # x test
        if ax.ckAxesProps.is_xlog:
            if self.set_xlog_range_max:

                # "lines" has priority over "ax.get_lines()"
                lines = ax.get_lines() if lines is None else lines

                ### get min & max
                x_minima, x_maxima = get_lines_x_minima_maxima(
                    lines = lines,
                    ymin  = ax.ckAxesProps.ylim[0],
                    ymax  = ax.ckAxesProps.ylim[1]
                )

                range_exceed_maxval = modify_loglim(
                    ax.ckAxesProps.xlim,
                    **self.set_xlog_range_max_props,
                    minima = x_minima,
                    maxima = x_maxima
                )

                ax.ckAxesProps.xlog_range_exceed_maxval = range_exceed_maxval

        # max_range
        if ax.ckAxesProps.is_ylog:
            if self.set_ylog_range_max:

                # "lines" has priority over "ax.get_lines()"
                lines = ax.get_lines() if lines is None else lines

                ### get min & max
                y_minima, y_maxima = get_lines_y_minima_maxima(
                    lines = lines,
                    xmin  = ax.ckAxesProps.xlim[0],
                    xmax  = ax.ckAxesProps.xlim[1]
                )

                range_exceed_maxval = modify_loglim(
                    ax.ckAxesProps.ylim,
                    **self.set_ylog_range_max_props,
                    minima = y_minima,
                    maxima = y_maxima
                )

                ax.ckAxesProps.ylog_range_exceed_maxval = range_exceed_maxval


        if not skip_adjust_xlim:
            ax.ckAxesProps.new_xlim = xlim_margin(
                ax      = ax,
                xrange  = ax.ckAxesProps.xlim,
                margins = self.axes_xmargins
            )
            ax.set_xlim( ax.ckAxesProps.new_xlim )


        if not skip_adjust_ylim:
            ax.ckAxesProps.new_ylim = ylim_margin(
                ax      = ax,
                yrange  = ax.ckAxesProps.ylim,
                margins = self.axes_ymargins
            )
            ax.set_ylim( ax.ckAxesProps.new_ylim )



        #################
        # ticks
        #################
        for (
            is_log, is_log_format,
            axis,
            lim,
            ticker_range_thr,
            skip_adjust_lim
        ) in zip(
            #
            [ ax.ckAxesProps.is_xlog,  ax.ckAxesProps.is_ylog  ],
            [ self.is_xlog_format, self.is_ylog_format ],
            #
            [ ax.xaxis,  ax.yaxis ],
            #
            [ ax.ckAxesProps.xlim, ax.ckAxesProps.ylim ],
            #
            [
                self.xlog_ticker_exponent_range_thr,
                self.ylog_ticker_exponent_range_thr
            ],
            #
            [ skip_adjust_xlim, skip_adjust_ylim ]
        ):

            if skip_adjust_lim: continue

            if not is_log: continue

            # formatter
            if not is_log_format:
                axis.set_major_formatter( copy.copy( LOG_SCALAR_FMT_MAJ ) )

            if np.abs( np.log10(lim[0]) - np.log10(lim[1]) ) > 0.5:
                axis.set_minor_formatter( FormatStrFormatter('') )

            # locator
            exponent_range = np.log10( lim[1] / lim[0] )
            if exponent_range < ticker_range_thr:
                # normal log locator
                axis.set_major_locator( copy.copy( LOG_LOC_MAJ ) )
                axis.set_minor_locator( copy.copy( LOG_LOC_MIN ) )
            else:
                axis.set_major_locator( copy.copy( WIDE_LOG_LOC_MAJ ) )
                axis.set_minor_locator( copy.copy( WIDE_LOG_LOC_MIN ) )


        return ax.ckAxesProps


    #==============================================================#
    # savefig
    #==============================================================#
    def savefig(
        self,
        **kwargs
    ) -> None:
        """
        * savefig( **self.save_props). \n
        * if kwargs are used, savefig( **new_kwargs )
        where new_kwargs is dict(**self.save_props).update( **kwargs )
        ( kwargs has priority over "self.save_props").
        ----------
        * fname
        * dirname
        * fig         = plt.gcf()
        * png         = True
        * svg         = True
        * png_dpi     = 300
        * svg_dpi     = 150
        * replace     = True
        * save_params = SAVE_PARAMS
        """
        if not self.fig: return

        new_kwargs = dict( **self.save_props )
        new_kwargs.update( **kwargs )

        if new_kwargs.get( 'fname' ) is None: return

        savefig( **new_kwargs )


    #==============================================================#
    # savecsv
    #==============================================================#
    def savecsv(
        self,
        **kwargs
    ) -> None:
        """
        * if same key exists in self.save_props & self.savecsv_props[key] is None:
            self.save_props[key] is used instead of self.savecsv_props[key].
        * if kwargs are used: kwargs has priority over "self.savecsv_props".
        ----------
        * fname
        * dirname
        * header
        * common_x (default: True)
        * subplot_common_x (default: False)
        """
        if self.no_line: self.csv = False
        if not self.csv: return

        savecsv_props = dict(
            dirname    = None,
            subdirname = None,
            fname      = None,
            header     = None,
            common_x   = True,
            subplot_common_x = False
        )
        savecsv_props.update( **self.savecsv_props )

        # if val is None: use val of save_props for fig
        for key, val in savecsv_props.items():
            if val is not None: continue
            if self.save_props.get( key ) is None: continue
            savecsv_props[ key ] = self.save_props[ key ]

        savecsv_props.update( **kwargs )

        if savecsv_props['fname'] is None: return

        _subdir = savecsv_props['subdirname']
        _dir = savecsv_props['dirname']
        if _subdir is not None:
            if _dir is None:
                _dir = _subdir
            else:
                _dir = os.path.join(
                    _dir,
                    _subdir
                )
            savecsv_props['dirname'] = _dir
        savecsv_props.pop( 'subdirname' )

        savecsv( **savecsv_props )


    #==============================================================#
    # others
    #==============================================================#
    @staticmethod
    def _range_exceed_maxval(
        ckAxesProps_results: list[ _CkAxesProps ]
    ) -> bool:
        return any( sum(
            [
                [
                    getattr(
                        ckAxesProps,
                        'ylog_range_exceed_maxval',
                        False
                    ),
                    getattr(
                        ckAxesProps,
                        'xlog_range_exceed_maxval',
                        False
                    ),
                ] for ckAxesProps in ckAxesProps_results
            ],
            []
        ) )


    #==============================================================#
    # others
    #==============================================================#
    def make_figure(
        self,
        print_name: bool = ckFigureConfig.show_savefname,
        inline_show: bool = True,
        show: bool = False
    ) -> None:

        if self.save_props.get( 'fname' ) and print_name:
            print( f' > {self.save_props[ "fname" ]}' )

        # setstyle & savefig
        ckAxesProps_results = self.set_figure_style()
        self.savefig()
        self.savecsv()


        #--------------------------------------------------------------#
        # inline show
        #--------------------------------------------------------------#
        if inline_show and _is_inline():

            save_svg = self.save_props[ 'save_svg' ] if 'save_svg' in self.save_props else True
            if save_svg:
                try:
                    from matplotlib_inline import backend_inline
                    backend_inline.set_matplotlib_formats( 'svg' )
                except:
                    pass

            try:
                from IPython.display import display
                display( plt.gcf() )
            except:
                pass


        #--------------------------------------------------------------#
        # save original figure if ylog_range_exceed_maxval
        #--------------------------------------------------------------#
        if not self.save_original_fig:
            if show:
                plt.show()
            return

        if self._range_exceed_maxval( ckAxesProps_results ):
            ckFig_ = copy.deepcopy( self )
            ckFig_.set_xlog_range_max = False
            ckFig_.set_ylog_range_max = False
            ckFig_.save_props[ 'dirname' ] += '/original'
            ckFig_.save_props[ 'fname' ] += '_original'

            # setstyle & savefig
            ckFig_.set_figure_style()
            ckFig_.savefig()

        if show:
            self.set_figure_style()
            plt.show()




################################################################
# get figure props
################################################################
def get_figure_props(
    fig:          bool | None = None,
    save_dirname: str  | None = None,
    save_fname:   str  | None = None,
    save_props:   dict = {},

    csv:                bool | None = None,
    savecsv_subdirname: str  | None = None,
    savecsv_props:      dict = {},

    plt_props:       dict | None = None,
    plt_prop_kwargs: dict | None = None,

    xmin: float | None = None,
    xmax: float | None = None,
    ymin: float | None = None,
    ymax: float | None = None,
    common_xlim: bool | None = None,
    common_ylim: bool | None = None,
    is_ylim_adjust_xlim: bool | None = None,

    is_xlog_intlim: bool | None = None,
    is_ylog_intlim: bool | None = None,
    is_xlog_format: bool | None = None,
    is_ylog_format: bool | None = None,

    set_xlog_range_max: bool | None = None,
    set_ylog_range_max: bool | None = None,
    set_xlog_range_max_props: dict | None = None,
    set_ylog_range_max_props: dict | None = None,

    axes_xmargins: list[float, float] | None = None,
    axes_ymargins: list[float, float] | None = None,

    annotate_str:   str  | None = None,
    annotate_props: dict | None = None,

    no_line:    bool | None = None,
    adjust_lim: bool | None = None,

    xlog_ticker_exponent_range_thr: int | None = None,
    ylog_ticker_exponent_range_thr: int | None = None,

    save_original_fig: bool | None = None
) -> dict:
    """
    - `plt_props`
    - `plt_prop_kwargs`

    - save figure
        - `fig`
        - `save_dirname`
        - `save_fname`
        - `save_props`

    - export plotted data as csv file
        - `csv`
        - `savecsv_subdirname`
        - `savecsv_props`

    - Range options
        - `xmin`, `xmax`, `ymin`, `ymax`
        - `common_xlim` | `common_ylim`
        - `is_ylim_adjust_xlim`
        - `axes_xmargins` | `axes_ymargins`
        - `adjust_lim`

    - Range options for logscale
        - `is_xlog_intlim` | `is_ylog_intlim`
        - `is_xlog_format` | `is_ylog_format`
        - `xlog_ticker_exponent_range_thr` | `ylog_ticker_exponent_range_thr`
        - Range max options:
            - `set_xlog_range_max` | `set_ylog_range_max`
            - `set_xlog_range_max_props` | `set_ylog_range_max_props`
            - `save_original_fig`

    - Annotation
        - `annotate_str`
        - `annotate_props`

    - Others
        - `no_line`
    """

    fig_props = {}
    fig_props.update( save_props = save_props.copy() )
    fig_props.update( savecsv_props = savecsv_props.copy() )

    if save_dirname is not None: fig_props['save_props'].update( dirname = save_dirname )
    if save_fname   is not None: fig_props['save_props'].update( fname   = save_fname   )
    if savecsv_subdirname is not None: fig_props['savecsv_props'].update( subdirname = savecsv_subdirname )

    # if fig_props['save_props'].get( 'dirname' ) is None:
    #     fig_props['save_props']['dirname'] = SAVE_DIRNAME
    # if fig_props['save_props'].get( 'fname' ) is None:
    #     fig_props['save_props']['fname'] = SAVE_FNAME

    kwargs = dict(
        fig = fig,
        csv = csv,

        plt_props = plt_props,
        plt_prop_kwargs = plt_prop_kwargs,

        xmin = xmin,
        xmax = xmax,
        ymin = ymin,
        ymax = ymax,
        common_xlim = common_xlim,
        common_ylim = common_ylim,
        is_ylim_adjust_xlim = is_ylim_adjust_xlim,

        is_xlog_intlim = is_xlog_intlim,
        is_ylog_intlim = is_ylog_intlim,
        is_xlog_format = is_xlog_format,
        is_ylog_format = is_ylog_format,

        set_xlog_range_max = set_xlog_range_max,
        set_ylog_range_max = set_ylog_range_max,
        set_xlog_range_max_props = set_xlog_range_max_props,
        set_ylog_range_max_props = set_ylog_range_max_props,

        axes_xmargins = axes_xmargins,
        axes_ymargins = axes_ymargins,

        annotate_str   = annotate_str,
        annotate_props = annotate_props,

        no_line    = no_line,
        adjust_lim = adjust_lim,

        xlog_ticker_exponent_range_thr = xlog_ticker_exponent_range_thr,
        ylog_ticker_exponent_range_thr = ylog_ticker_exponent_range_thr,

        save_original_fig = save_original_fig
    )

    for key, val in kwargs.items():
        if val is not None:
            _val = val.copy() if isinstance( val, dict ) else val
            fig_props.update({
                key: _val
            })

    return fig_props




################################################################
# context manager
################################################################
@contextmanager
def ckfigure(
    *fig_props_list:   dict,
    cycle:             dict|Cycler|None = ckFigureConfig.default_cycle,
    use_mplstyle_base: bool             = ckFigureConfig.use_mplstyle_base,
    mplstyle_font:     str | None       = ckFigureConfig.mplstyle_font,
    mplstyle:          str | None       = None,
    mplstyle_dir:      str | None       = None,
    inline_show:       bool             = ckFigureConfig.inline_show,
    show:              bool             = False,
    close:             bool             = ckFigureConfig.close,
    **fig_props
):

    #==============================================================#
    # enter - preparing rcParams -
    #==============================================================#
    mpl_rc_params = {}

    #--------------------------------------------------------------#
    # rcParams from mplstyle file
    #--------------------------------------------------------------#
    if use_mplstyle_base:
        _props = _use_mplstyle_base( use = False )
        mpl_rc_params.update( _props )

    if mplstyle_font is not None or mplstyle_font == 'none':
        _props = use_mplstyle_font( mplstyle_font,  use = False )
        mpl_rc_params.update( _props )

    if mplstyle is not None:
        _props = use_mplstyle( mplstyle, dirname = mplstyle_dir, use = False )
        mpl_rc_params.update( _props )

    #--------------------------------------------------------------#
    # rcParams from cycle
    #--------------------------------------------------------------#
    if cycle is not None and cycle != {}:
        cycle_is_dict = isinstance( cycle, dict )
        prop_cycle = cycler( **cycle ) if cycle_is_dict else cycle
        mpl_rc_params.update({
            'axes.prop_cycle': prop_cycle
        })


    #==============================================================#
    # try - main plot -
    #==============================================================#
    try:
        with mpl.rc_context( mpl_rc_params ):

            #--------------------------------------------------------------#
            # main plot
            #--------------------------------------------------------------#
            yield


            #--------------------------------------------------------------#
            # set style & save
            #--------------------------------------------------------------#
            fig_props_list_len = len( fig_props_list )
            if fig_props_list_len == 0:
                ckFig = CkFigure( **fig_props )
                ckFig.make_figure( inline_show = inline_show, show = show )

            else:
                for i, fig_props_tmp in enumerate( fig_props_list ):
                    _show = False if i != fig_props_list_len - 1 else show
                    fig_props = deepmerge( fig_props, fig_props_tmp )
                    ckFig = CkFigure( **fig_props )
                    ckFig.make_figure( inline_show = inline_show, show = _show )


    #==============================================================#
    # finally - close figure -
    #==============================================================#
    finally:
        if close: plt.close()
