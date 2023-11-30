
##################################################################################
# READ THE VTU SOLUTION FILES AND PLOT THE 2D COLORMAPS
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

def plotPseudocolorPlot(ordered_filedirs_f, filesdir_f, binary):

    if binary == True:
        cmap = 'binary_r'
    else:
        cmap = cmaps.berlin

    raw_img_f = []
    for fdir in ordered_filedirs_f:
        x_f, y_f, v_f, block_f, time_f = read_VTU_for_coords_and_data(filesdir_f + '/' + fdir)

        triang = tri.Triangulation(x_f, y_f)
        fig1, ax1 = plt.subplots()
        ax1.set_aspect('equal')
        tpc = ax1.tripcolor(triang, v_f, shading='gouraud', cmap=cmap, vmin=0, vmax=1)
        ax1.set_ylim(0, 800)
        ax1.set_xlim(0, 800)
        fig1.colorbar(tpc)
        fig1.savefig(filesdir_f + '/' + f"snapshot-{time_f}.png", dpi=300)

        fig1.canvas.draw()
        temp_canvas = fig1.canvas
        s, (width, height) = temp_canvas.print_to_buffer()
        raw_img_i = np.frombuffer(s, np.uint8).reshape((height, width, 4))  # Will round down floats but
        raw_img_i = raw_img_i[-1]
        raw_img_f.append(raw_img_i)                                                          # needed for the contour plot
        plt.close(fig1)                                                                      # (our snapshots are ints anyway)
    return raw_img_f


if __name__ == '__main__':

    filesdir = '/home/imoreno/eng_idrive/ChemEngUsers/bwb20181/Documents/coupledCHAC/2023-11-20 16-08-08.978595'
    files = [f for f in listdir(filesdir) if isfile(join(filesdir, f)) and f.endswith('.vtu')]

    ordered_filedirs = get_sorted_list_of_files(files)
    raw_imgs = plotPseudocolorPlot(ordered_filedirs, filesdir, binary=False)

    print("--- %s seconds ---" % (time.time() - start_time))
