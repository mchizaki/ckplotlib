
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt
import ckplotlib.ckplot as cplt

SAVE_DIRNAME = 'result'

x = np.linspace( 0, 10, 500 )


#==============================================================#
# common subplot props
#==============================================================#
figure_props = cplt.get_figure_props(
    save_dirname = SAVE_DIRNAME,
    save_fname   = 'fig_cplt_subplot0',
    plt_args = dict(
        xlabel = '$x$ label',
        ylabel = '$y$ label',
        title  = 'title'
    ),
    plt_prop_kwargs = dict(
        legend = dict(
            title = 'lgd title'
        )
    )
)

with cplt.ckfigure( **figure_props ):
    fs = plt.rcParams[ 'figure.figsize' ]
    plt.figure( figsize = ( fs[0]*3, fs[1] ) )
    plt.subplots_adjust( wspace = 0.5 )
    plt.subplot(121)
    plt.plot( x, np.sin( x ), 'k', label = r'$\sin(x)$' )
    plt.plot( x, np.cos( x ), 'r', label = r'$\cos(x)$' )
    plt.subplot(122)
    plt.plot( x, np.sin( x ), 'k', label = r'$\sin(x)$' )
    plt.plot( x, np.cos( x ), 'r', label = r'$\cos(x)$' )



#==============================================================#
# not common subplot props
#==============================================================#
figure_props_list = [
    cplt.get_figure_props(
        save_dirname = SAVE_DIRNAME,
        save_fname   = 'fig_cplt_subplot1',
        plt_args = dict(
            xlabel = '$x$ label',
            ylabel = r'$\sin(x)$',
            title  = 'title 1'
        ),
        ymin = -2,
        ymax = 2
    ),
    cplt.get_figure_props(
        plt_args = dict(
            xlabel = '$x$ label',
            ylabel = r'$\cos(x)$',
            title  = 'title 2'
        ),
        plt_prop_kwargs = dict(
            legend = dict(
                title = 'lgd title'
            )
        ),
        ymin = -2,
        ymax = 2,
        axes_xmargins = [ 0, 0.5 ],
        axes_ymargins = [ 0, 0 ]
    )
]

with cplt.ckfigure(
    *figure_props_list,
    common_subplot_props = False
):
    fs = plt.rcParams[ 'figure.figsize' ]
    plt.figure( figsize = ( fs[0]*3, fs[1] ) )
    plt.subplots_adjust( wspace = 0.5 )
    plt.subplot(121)
    plt.plot( x, np.sin( x ), 'k', label = r'$\sin(x)$' )
    plt.plot( x, np.cos( x ), 'r', label = r'$\cos(x)$' )
    plt.subplot(122)
    plt.plot( x, np.sin( x ), 'k', label = r'$\sin(x)$' )
    plt.plot( x, np.cos( x ), 'r', label = r'$\cos(x)$' )


