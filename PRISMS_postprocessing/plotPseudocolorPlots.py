
##################################################################################
# READ THE VTU SOLUTION FILES AND PLOT THE 2D COLORMAPS
##################################################################################

import io
import cv2
import meshio
import time
import numpy as np
from os import listdir
from os.path import isfile, join
import matplotlib as mpl
from matplotlib import pyplot as plt
import matplotlib.tri as tri
import colormaps as cmaps
from calculateInductionTime import get_sorted_list_of_files
from calculatePhaseFraction import read_VTU_for_coords_and_data

start_time = time.time()
mpl.rcParams['savefig.pad_inches'] = 0

def plotPseudocolorPlot(ordered_filedirs_f, filesdir_f, binary, savepscplots):

    if binary == True:
        cmap = 'binary_r'
    else:
        cmap = cmaps.berlin

    raw_img_f = []; times_f = []
    for fdir in ordered_filedirs_f:
        x_f, y_f, v_f, block_f, time_f = read_VTU_for_coords_and_data(filesdir_f + '/' + fdir)
        times_f.append(time_f)

        triang = tri.Triangulation(x_f, y_f)
        fig1, ax1 = plt.subplots()
        ax1.set_aspect('equal')
        tpc = ax1.tripcolor(triang, v_f, shading='gouraud', cmap=cmap, vmin=0, vmax=1)
        ax1.set_ylim(0, 800)
        ax1.set_xlim(0, 800)
        cbar = fig1.colorbar(tpc)
        # NOTE: If axis labels are added, they will need to be removed BEFORE saving to a buffer
        # right now there is no issue since they are inside the if

        if savepscplots == True and binary == False:
            ax1.set_ylabel('Y axis')
            ax1.set_xlabel('X axis')
            fig1.savefig(filesdir_f + '/' + f"snapshot-{time_f}.png", bbox_inches='tight', transparent="True", pad_inches=0, dpi=500)
        elif binary == True:
            ax1.set_axis_off()
            cbar.remove()
            buffer = io.BytesIO()  # Save the image directly into a buffer
            fig1.savefig(buffer, bbox_inches='tight', transparent="True", pad_inches=0, format='png')
            buffer.seek(0)
            raw_img_i = cv2.imdecode(np.frombuffer(buffer.read(), dtype=np.uint8), cv2.IMREAD_GRAYSCALE)

        raw_img_f.append(raw_img_i)
        plt.close()
    return raw_img_f, times_f


if __name__ == '__main__':

    filesdir = '/home/imoreno/eng_idrive/ChemEngUsers/bwb20181/Documents/coupledCHAC/2023-11-20 16-08-08.978595'
    files = [f for f in listdir(filesdir) if isfile(join(filesdir, f)) and f.endswith('.vtu')]

    ordered_filedirs = get_sorted_list_of_files(files)
    raw_imgs = plotPseudocolorPlot(ordered_filedirs, filesdir, binary=False, savepscplots=True)

    print("--- %s seconds ---" % (time.time() - start_time))
