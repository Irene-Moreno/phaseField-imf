
##################################################################################
# READ THE VTU SOLUTION FILES, PLOT THEM AND EXTRACT THE PHASE FRACTION
##################################################################################

# The analysis of 24 files took about 1.3 min

import re
import meshio
import numpy as np
from os import listdir
from os.path import isfile, join
from matplotlib import pyplot as plt
import matplotlib.tri as tri
import colormaps as cmaps
from calculateInductionTime import get_sorted_list_of_files


def readVTUForPseudocolor(filedir):
    # Grab the snapshot time for the image name
    time_pattern = r'(\d+)'
    time_f = int(re.search(time_pattern, filedir.split('/')[-1]).group())

    # Read the vertices and blocks forming each cell
    mesh = meshio.vtu.read(filedir)
    x_f, y_f, _ = mesh.points.transpose()
    v_f = mesh.point_data['n']
    block_f = mesh.cells_dict['quad']
    
    return x_f, y_f, v_f, block_f, time_f


def plotPseudocolorPlot(ordered_filedirs_f, filesdir_f):
    for fdir in ordered_filedirs_f:
        x_f, y_f, v_f, block_f, time_f = readVTUForPseudocolor(filesdir_f + '/' + fdir)

        triang = tri.Triangulation(x_f, y_f)
        fig1, ax1 = plt.subplots()
        ax1.set_aspect('equal')
        tpc = ax1.tripcolor(triang, v_f, shading='gouraud', cmap=cmaps.berlin, vmin=0, vmax=1)
        fig1.colorbar(tpc)
        fig1.savefig(filesdir_f + '/' + f"snapshot-{time_f}.png", dpi=600)
        plt.close(fig1)


def calculatePhaseFraction(ordered_filedirs_f):
    times = []
    phase_fractions = []
    for fdir in ordered_filedirs_f:
        x_f, y_f, v_f, block_f, time_f = readVTUForPseudocolor(filesdir + '/' + fdir)
        times.append(time_f)

        n_area_f = 0
        t_area_f = 0
        for i, j, k, l in block_f:  # Blocks has the correct number of cells (no repeated ones)
            x1 = x_f[i]             # so there is no double-counting calculating the phase fraction
            y1 = y_f[i]
            v1 = v_f[i]

            x2 = x_f[j]
            y2 = y_f[j]
            v2 = v_f[j]

            x3 = x_f[k]
            y3 = y_f[k]
            v3 = v_f[k]

            x4 = x_f[l]
            y4 = y_f[l]
            v4 = v_f[l]
            mx = np.mean([x1, x2, x3, x4])
            my = np.mean([y1, y2, y3, y4])
            mv = np.mean([v1, v2, v3, v4])

            if x1 != x2:
                width = abs(x1-x2)
            elif x1 != x3:
                width = abs(x1-x3)
            elif x1 != x4:
                width = abs(x1-x3)
            
            if y1 != y2:
                heigth = abs(y1-y2)
            elif y1 != y3:
                heigth = abs(y1-y3)
            elif y1 != y4:
                heigth = abs(y1-y3)
            
            if mv > 0.5:
                n_area_f += width*heigth
                t_area_f += width*heigth
            else:
                t_area_f += width*heigth
        
        phase_fraction = n_area_f/t_area_f
        phase_fractions.append(phase_fraction)

    return phase_fractions, times


filesdir = '/home/imoreno/eng_idrive/ChemEngUsers/bwb20181/Documents/coupledCHAC/2023-11-20 16-08-08.978595'
files = [f for f in listdir(filesdir) if isfile(join(filesdir, f)) and f.endswith('.vtu')]

ordered_filedirs = get_sorted_list_of_files(files)
plotPseudocolorPlot(ordered_filedirs, filesdir)
phase_fracs, times = calculatePhaseFraction(ordered_filedirs)
print(phase_fracs)


# The list of coordinates stored in points contains the list of cell nodes used to create the grid in the same order
# that the cells_dict contains, and that the scalar fields (such as n or c) are stored as. Hence, iterating through
# the index of each node in each cell block, we can get the (x, y) coordinates and field value of each node.
# Then, through taking their mean, we can get the location of the center of each cell (and the mean value of the field
# in that centre).

# In principle, I should be able to plot the mean values of the field obtained this way with a colormap, and this way
# reproduce the images that come from VisIt.
