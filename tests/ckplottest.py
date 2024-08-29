#%%
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt
import ckplotlib.ckplot as cplt

SAVE_DIRNAME = 'result'

x = np.linspace( 0, 10, 500 )
y = np.sin( x )


#%% [markdown]
"""
## Plot examples
"""


#%% [markdown]
"""
### ckplotlib normal (with) [recommended]
"""
#%%
with cplt.ckfigure():
    plt.figure()
    plt.plot( x, y )


#%% [markdown]
"""
### ckplotlib normal (decorator)
"""
#%%
@cplt.ckfigure()
def myplotfunc():
    plt.figure()
    plt.plot( x, y )

myplotfunc()


#%% [markdown]
"""
### with save options
"""
#%%
figure_props = cplt.get_figure_props(
    save_dirname = SAVE_DIRNAME,
    save_fname   = 'fig_cplt0'
)
pprint( figure_props )

with cplt.ckfigure( **figure_props ):
    plt.figure()
    plt.plot( x, y )


#%% [markdown]
"""
### with markup options of plt args
"""
#%%
figure_props = cplt.get_figure_props(
    save_dirname = SAVE_DIRNAME,
    save_fname   = 'fig_cplt1',
    plt_args = dict(
        xlabel = '$x$ label',
        ylabel = '$y$ label',
        title  = 'title'
    )
)
pprint( figure_props )

with cplt.ckfigure( **figure_props ):
    plt.figure()
    plt.plot( x, y )


#%% [markdown]
"""
### with markup options of plt kwargs
"""
#%%
figure_props = cplt.get_figure_props(
    save_dirname = SAVE_DIRNAME,
    save_fname   = 'fig_cplt2',
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
pprint( figure_props )

with cplt.ckfigure( **figure_props ):
    plt.figure()
    plt.plot( x, y, label = r'$\sin(x)$' )


#%% [markdown]
"""
### with legend
"""
#%%
figure_props = cplt.get_figure_props(
    save_dirname = SAVE_DIRNAME,
    save_fname   = 'fig_cplt3',
    plt_args = dict(
        xlabel = '$x$ label',
        ylabel = '$y$ label',
        title  = 'title'
    ),
    plt_prop_kwargs = dict(
        legend = {}
    )
)
pprint( figure_props )

with cplt.ckfigure( **figure_props ):
    plt.figure()
    plt.plot( x, y, label = r'$\sin(x)$' )


#%% [markdown]
"""
### with axes_margin option
"""
#%%
figure_props = cplt.get_figure_props(
    save_dirname = SAVE_DIRNAME,
    save_fname   = 'fig_cplt_axes_margin',
    axes_xmargins = [ 0.05, 0.2 ],
    axes_ymargins = [ 0, 0.3 ]
)

with cplt.ckfigure( **figure_props ):
    plt.figure()
    plt.plot( x, y )



#%% [markdown]
"""
### with hlines and vlines
"""
#%%
figure_props = cplt.get_figure_props(
    save_dirname = SAVE_DIRNAME,
    save_fname   = 'fig_cplt_hlines_vlines',
    hlines_yvals  = [ 0, 1, -0.5 ],
    vlines_xvals  = [ 4 ],
    vlines_props  = dict(
        color     = 'r',
        linewidth = 2,
        linestyle = '-.',
        zorder    = 10
    )
)
with cplt.ckfigure( **figure_props ):
    plt.figure()
    plt.plot( x, y )


#%% [markdown]
"""
### with annotate
"""
#%%
figure_props = cplt.get_figure_props(
    save_dirname = SAVE_DIRNAME,
    save_fname   = 'fig_cplt_annotate',
    annotate_str = 'annotate\ntest'
)
with cplt.ckfigure( **figure_props ):
    plt.figure()
    plt.plot( x, y )

figure_props = cplt.get_figure_props(
    save_dirname = SAVE_DIRNAME,
    save_fname   = 'fig_cplt_annotate2',
    annotate_str = 'annotate\ntest',
    annotate_props = dict(
        loc = None
    )
)
with cplt.ckfigure( **figure_props ):
    plt.figure()
    plt.plot( x, y )

figure_props = cplt.get_figure_props(
    save_dirname = SAVE_DIRNAME,
    save_fname   = 'fig_cplt_annotate3',
    annotate_str = 'annotate\ntest',
    annotate_props = dict(
        loc = 'inner lower left'
    )
)
with cplt.ckfigure( **figure_props ):
    plt.figure()
    plt.plot( x, y )


#%% [markdown]
"""
### logscale
"""
#%%
figure_props = cplt.get_figure_props(
    save_dirname = SAVE_DIRNAME,
    save_fname   = 'fig_cplt_log1',
    plt_args = dict(
        xlabel = '$x$ label',
        ylabel = '$y$ label',
        yscale = 'log'
    )
)

with cplt.ckfigure( **figure_props ):
    plt.figure()
    plt.plot( x, 5 * np.exp( -x ) )


#%% [markdown]
"""
### logscale without intlim option
"""
#%%
figure_props = cplt.get_figure_props(
    save_dirname = SAVE_DIRNAME,
    save_fname   = 'fig_cplt_log2',
    plt_args = dict(
        xlabel = '$x$ label',
        ylabel = '$y$ label',
        yscale = 'log'
    ),
    is_ylog_intlim = False
)

with cplt.ckfigure( **figure_props ):
    plt.figure()
    plt.plot( x, 5 * np.exp( -x ) )


#%% [markdown]
"""
### logscale of wide range
"""
#%%
figure_props = cplt.get_figure_props(
    save_dirname = SAVE_DIRNAME,
    save_fname   = 'fig_cplt_log3',
    plt_args = dict(
        xlabel = '$x$ label',
        ylabel = '$y$ label',
        yscale = 'log'
    )
)

with cplt.ckfigure( **figure_props ):
    plt.figure()
    plt.plot( x, 5 * np.exp( -x * 10 ) )


#%% [markdown]
"""
### logscale with data including zero values
If the data contains zero values, the axis is not adjusted.
"""
#%%
figure_props = cplt.get_figure_props(
    save_dirname = SAVE_DIRNAME,
    save_fname   = 'fig_cplt_log4',
    plt_args = dict(
        xlabel = '$x$ label',
        ylabel = '$y$ label',
        yscale = 'log'
    ),
    is_ylog_intlim = False
)

with cplt.ckfigure( **figure_props ):
    plt.figure()
    plt.plot( x, 5 * np.sin( x ) )


#%% [markdown]
"""
### logscale with log_range_max option
"""
#%%
figure_props = cplt.get_figure_props(
    save_dirname = SAVE_DIRNAME,
    save_fname   = 'fig_cplt_ylog_range_max',
    plt_args = dict(
        yscale = 'log'
    ),
    set_ylog_range_max = True
)

x1 = np.logspace( -30, 2, 500 )
x2 = np.linspace( 0, 100, 500 )
with cplt.ckfigure( **figure_props ):
    plt.figure()
    plt.plot( x1, x1 )
    plt.plot( x2, 100 * np.exp( -x2 / 10 ) )



#%% [markdown]
"""
### matplotlib normal
"""
#%%
plt.figure()
plt.plot( x, y )
plt.savefig(
    'result/fig_plt0.svg',
    format      = 'svg',
    dpi         = 150,
    pad_inches  = 0.2,
    bbox_inches = 'tight',
)
