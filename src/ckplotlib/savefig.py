"""
* Written by CK
"""
import matplotlib.pyplot as plt
import os
import pickle
from .config import ckFigureConfig

SAVE_PARAMS = dict(
    bbox_inches = 'tight',
    pad_inches  = 0.2
)


def savefig(
    fname: str,
    dirname:    str | None = None,
    fig: plt.Figure | None = None,
    png_dpi:     int  = 300,
    svg_dpi:     int  = 150,
    save_png:    bool = ckFigureConfig.png,
    save_svg:    bool = ckFigureConfig.svg,
    save_pkl:    bool = False,
    save_pgf:    bool = False,
    replace:     bool = True,
    save_params: dict = SAVE_PARAMS,
    **kwargs
) -> None:

    if fig is None: fig = plt.gcf()

    save_fname = fname
    if dirname is not None:
        os.makedirs( dirname, exist_ok=True )
        save_fname = os.path.join( dirname, fname )

    if save_png:
        save_fpath = f'{save_fname}.png'
        if replace or not os.path.isfile( save_fpath ):
            fig.savefig(
                save_fpath,
                format = 'png',
                dpi    = png_dpi,
                **save_params,
                **kwargs
            )

    if save_svg:
        save_fpath = f'{save_fname}.svg'
        if replace or not os.path.isfile( save_fpath ):
            fig.savefig(
                save_fpath,
                format = 'svg',
                dpi    =  svg_dpi,
                **save_params,
                **kwargs
            )

    if save_pgf:
        save_fpath = f'{save_fname}.pgf'
        if replace or not os.path.isfile( save_fpath ):
            fig.savefig(
                save_fpath,
                format = 'pgf',
                **save_params,
                **kwargs
            )

    if save_pkl:
        save_fpath = f'{save_fname}.pkl'
        if replace or not os.path.isfile( save_fpath ):
            with open( save_fpath, 'wb' ) as f:
                pickle.dump(fig, f)
