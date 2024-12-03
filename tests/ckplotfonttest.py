#%%
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt
import ckplotlib.ckplot as cplt

SAVE_DIRNAME = 'result'

x = np.linspace( 0, 10, 500 )
y = np.sin( x )

#%%
figure_props = cplt.get_figure_props(
    save_dirname = SAVE_DIRNAME,
    save_fname   = 'fig_cplt3_arial'
)

with cplt.ckfigure( **figure_props, mplstyle_font='arial' ):
    plt.figure()
    plt.plot( x, y, label = r'$\sin(x)$' )
    plt.xlabel( '$x$ label' )
    plt.ylabel( '$y$ label' )
    plt.title( 'title' )
    cplt.legend()
