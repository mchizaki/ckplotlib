# ckplotlib
Add-on library of Matplotlib for publication quality plots

## Usage [under construction]

### ckfigure
Context manager of `ckplotlib.ckplot.ckfigure` enables you to markup and save high-quality figures easily.

### figure props
Context manager of `ckplotlib.ckplot.ckfigure` can receive the `figure_props` of `dict`.
The function of `ckplotlib.ckplot.get_figure_props` helps you create `figure_props` dictionary.

Arguments of `ckplotlib.ckplot.get_figure_props` (all arguments are optional):
```python
fig:          bool
save_dirname: str
save_fname:   str
save_props:   dict

csv:                bool
savecsv_subdirname: str
savecsv_props:      dict

plt_props:       dict
plt_prop_kwargs: dict

xmin: float
xmax: float
ymin: float
ymax: float
common_xlim: bool
common_ylim: bool
is_ylim_adjust_xlim: bool

is_xlog_intlim: bool
is_ylog_intlim: bool
is_xlog_format: bool
is_ylog_format: bool

set_xlog_range_max: bool
set_ylog_range_max: bool
set_xlog_range_max_props: dict
set_ylog_range_max_props: dict

axes_xmargins: list[float, float]
axes_ymargins: list[float, float]

annotate_str:   str
annotate_props: dict

no_line:    bool
adjust_lim: bool

xlog_ticker_exponent_range_thr: int
ylog_ticker_exponent_range_thr: int
```

- `plt_props` and `plt_prop_kwargs`
    ```python
    plt_props = dict(
        xlabel = 'Temperature (K)',
        yscale = 'log'
    )
    
    plt_prop_kwargs = dict(
        legend = dict(
            bbox_to_anchor = (1, 1)
        )
    )
    ```

- save figure
    - `fig`
    - `save_dirname`
    - `save_fname`
    - `save_props`

- export plotted data as csv file
    - `csv`
    - `savecsv_subdirname`
    - `savecsv_props`

- `xmin`, `xmax`, `ymin`, `ymax`
    - minimum/maximum value that determines the display range of graph
    - None => not specified: automatically determinted

- `common_x/ylim`:
    use common axis range if fig includes multiple ax subplots

- `x/ylog_intlim`
    - axis range = [10^a, 10^b] (a & b are integer)
    - this props is valid if plt.xscale/yscale is 'log'

- `x/ylog_format`
    - use exponential notation
    - this props is valid if plt.xscale/yscale is 'log'

- log range max
    - these props are valid if plt.x/yscale is 'log'
    - `set_x/ylog_range_max`
    - `set_x/ylog_range_max_props`
        - `exponent_range_max`: 8
        - `max_is_fixed`: True
        - `min_is_fixed`: False

- `axes_xmargins` and `axes_ymargins`:
    padding from minimum and maximum values in the graph,
    specified as a percentage of the size of Axis [from 0 to 1]
    e.g. axes_xmargins = [ 0.05, 0.05 ]

- annotate
    - `annotate_str`
    - `annotate_props`




## Plot examples [under construction]
common codes:
```python
import numpy as np
import matplotlib.pyplot as plt
import ckplotlib.ckplot as cplt

x = np.linspace( 0, 10, 500 )
y = np.sin( x )
```

### matplotlib normal
```python
plt.figure()
plt.plot( x, y )
```
![mplt0](sample/fig_mplt0.svg)

### ckplotlib normal
```python
with cplt.ckfigure():
    plt.figure()
    plt.plot( x, y )
```
![mplt0](sample/fig_cplt0.svg)

### markup and save figure
```python
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
![mplt0](sample/fig_cplt1.svg)

