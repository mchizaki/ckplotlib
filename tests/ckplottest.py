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
    save_dirname = 'result',
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
    save_dirname = 'result',
    save_fname   = 'fig_cplt1',
    plt_props = dict(
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
    save_dirname = 'result',
    save_fname   = 'fig_cplt2',
    plt_props = dict(
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
    save_dirname = 'result',
    save_fname   = 'fig_cplt3',
    plt_props = dict(
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
### logscale
"""
#%%
figure_props = cplt.get_figure_props(
    save_dirname = 'result',
    save_fname   = 'fig_cplt_log1',
    plt_props = dict(
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
    save_dirname = 'result',
    save_fname   = 'fig_cplt_log2',
    plt_props = dict(
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
    save_dirname = 'result',
    save_fname   = 'fig_cplt_log3',
    plt_props = dict(
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
    save_dirname = 'result',
    save_fname   = 'fig_cplt_log4',
    plt_props = dict(
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
