# ckplotlib
Add-on library of Matplotlib for publication quality plots

# Usage: under construction

## ckfigure
Context manager of `ckplotlib.ckplot.ckfigure` enables you to easily plot and save high quality figures

### plot example
```[python]
import numpy as np
x = np.linspace( 0, 10, 100 )
y = np.sin( x )
```

import graph libraries.
```[python]
import matplotlib.pyplot as plt
import ckplotlib.ckplot as cplt
```

#### matplotlib normal
```[python]
plt.figure()
plt.plot( x, y )
```

#### ckplotlib normal
```[python]
with cplt.ckfigure():
    plt.figure()
    plt.plot( x, y )
```

#### markup and save figure
```[python]
figure_props = cplt.get_figure_props(
    save_dirname = 'result',
    save_fname   = 'fig_cplt1',
    plt_props = dict(
        xlabel = '$x$ label',
        ylabel = '$y$ label',
        title  = 'title'
    )
)

with cplt.ckfigure( **figure_props ):
    plt.figure()
    plt.plot( x, y )
```

