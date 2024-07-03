import numpy as np
import matplotlib.pyplot as plt
import ckplotlib.ckplot as cplt

SAVE_DIRNAME = 'result'
theta = np.arange(0, 10)
sin_theta = np.sin(theta)
cos_theta = np.cos(theta)
x1 = np.array([0, 1, 2, 3])
x2 = np.array([0, 2, 4, 6])


#==============================================================#
# addlinename
#==============================================================#
figure_props = cplt.get_figure_props(
    save_dirname = SAVE_DIRNAME,
    save_fname   = 'fig_cplt_csv0'
)
with cplt.ckfigure(**figure_props):
    plt.figure()
    plt.plot(theta, sin_theta)
    plt.plot(theta, cos_theta)
    plt.show()


figure_props = cplt.get_figure_props(
    save_dirname = SAVE_DIRNAME,
    save_fname   = 'fig_cplt_csv1',
    savecsv_props = dict(
        header = 'this is header'
    )
)
with cplt.ckfigure(**figure_props):
    plt.figure()
    plt.plot(theta, sin_theta)
    cplt.addlinename('sin(theta)')
    plt.plot(theta, cos_theta)
    cplt.addlinename('cos(theta)')



figure_props = cplt.get_figure_props(
    save_dirname = SAVE_DIRNAME,
    save_fname   = 'fig_cplt_csv2',
    savecsv_props = dict(
        header = 'this is header'
    )
)
with cplt.ckfigure(**figure_props):
    plt.figure()
    plt.plot(theta, sin_theta)
    cplt.addlinename('theta', 'sin(theta)')
    plt.plot(theta, cos_theta)
    cplt.addlinename('theta', 'cos(theta)')


figure_props = cplt.get_figure_props(
    save_dirname = SAVE_DIRNAME,
    save_fname   = 'fig_cplt_csv3',
    savecsv_props = dict(
        common_x = False
    )
)
with cplt.ckfigure(**figure_props):
    plt.figure()
    plt.plot(theta, sin_theta)
    cplt.addlinename('theta1', 'sin(theta)')
    plt.plot(theta, cos_theta)
    cplt.addlinename('theta2', 'cos(theta)')


#==============================================================#
# common_x
#==============================================================#
figure_props = cplt.get_figure_props(
    save_dirname = SAVE_DIRNAME,
    save_fname   = 'fig_cplt_csv_common_true'
)
with cplt.ckfigure( **figure_props ):
    plt.figure()
    plt.plot( x1, x1**2 )
    plt.plot( x2, x2**2 )


figure_props = cplt.get_figure_props(
    save_dirname = SAVE_DIRNAME,
    save_fname   = 'fig_cplt_csv_common_false',
    savecsv_props = dict(
        common_x = False
    )
)
with cplt.ckfigure( **figure_props ):
    plt.figure()
    plt.plot( x1, x1**2 )
    plt.plot( x2, x2**2 )


#==============================================================#
# subplot_common_x
#==============================================================#
figure_props = cplt.get_figure_props(
    save_dirname = SAVE_DIRNAME,
    save_fname   = 'fig_cplt_csv_subplot_common_true',
    savecsv_props = dict(
        subplot_common_x = True
    )
)
with cplt.ckfigure( **figure_props ):
    plt.figure()
    plt.subplot(211)
    plt.plot( x1, x1**2 )
    plt.subplot(212)
    plt.plot( x2, x2**2 )


figure_props = cplt.get_figure_props(
    save_dirname = SAVE_DIRNAME,
    save_fname   = 'fig_cplt_csv_subplot_common_false',
    savecsv_props = dict(
        subplot_common_x = False
    )
)
with cplt.ckfigure( **figure_props ):
    plt.figure()
    plt.subplot(211)
    plt.plot( x1, x1**2 )
    plt.subplot(212)
    plt.plot( x2, x2**2 )
