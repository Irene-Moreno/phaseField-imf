
##################################################################################
# READ THE VTU SOLUTION FILES AND GET THE PSD EVOLUTION WITH TIME
##################################################################################

import meshio
import time
import numpy as np
from os import listdir
from os.path import isfile, join
from matplotlib import pyplot as plt
import matplotlib.tri as tri
import colormaps as cmaps
from calculateInductionTime import get_sorted_list_of_files
from calculatePhaseFraction import read_VTU_for_coords_and_data

start_time = time.time()

def plotContourPlot(ordered_filedirs_f, filesdir_f):
    for fdir in ordered_filedirs_f:
        x_f, y_f, v_f, block_f, time_f = read_VTU_for_coords_and_data(filesdir_f + '/' + fdir)

        triang = tri.Triangulation(x_f, y_f)
        fig1, ax1 = plt.subplots()
        ax1.set_aspect('equal')
        tpc = ax1.tricontourf(triang, v_f, cmap=cmaps.berlin, vmin=0, vmax=1)
        fig1.colorbar(tpc)
        fig1.savefig(filesdir_f + '/' + f"contourplot-{time_f}.png", dpi=300)
        plt.close(fig1)

filesdir = '/home/imoreno/eng_idrive/ChemEngUsers/bwb20181/Documents/coupledCHAC/2023-11-20 16-08-08.978595'
files = [f for f in listdir(filesdir) if isfile(join(filesdir, f)) and f.endswith('.vtu')]

ordered_filedirs = get_sorted_list_of_files(files)
plotContourPlot(ordered_filedirs, filesdir)

print("--- %s seconds ---" % (time.time() - start_time))
