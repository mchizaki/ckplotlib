"""
* Written by CK
"""
import matplotlib.pyplot as plt
import os
import pickle

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
    SAVE_PARAMS: dict = SAVE_PARAMS,
    save_png:    bool = True,
    save_svg:    bool = True,
    save_pkl:    bool = False,
    # save_pgf:    bool = False,
    replace:     bool = True
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
                **SAVE_PARAMS
            )

    if save_svg:
        save_fpath = f'{save_fname}.svg'
        if replace or not os.path.isfile( save_fpath ):
            fig.savefig(
                save_fpath,
                format = 'svg',
                dpi    =  svg_dpi,
                **SAVE_PARAMS
            )

    # if save_pgf:
    #     save_fpath = f'{save_fname}.pgf'
    #     if replace or not os.path.isfile( save_fpath ):
    #         fig.savefig(
    #             save_fpath,
    #             format = 'pgf',
    #             **SAVE_PARAMS
    #         )

    if save_pkl:
        save_fpath = f'{save_fname}.pkl'
        if replace or not os.path.isfile( save_fpath ):
            with open( save_fpath, 'wb' ) as f:
                pickle.dump(fig, f)
