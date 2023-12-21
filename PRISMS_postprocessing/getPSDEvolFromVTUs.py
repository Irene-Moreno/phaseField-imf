
##################################################################################
# READ THE VTU SOLUTION FILES AND GET THE CONTOUR PLOTS FROM THEM
##################################################################################

import cv2
import math
import time
import statistics
import numpy as np
from os import listdir
from os.path import isfile, join
from scipy.stats import linregress
from matplotlib import pyplot as plt
from calculateInductionTime import get_sorted_list_of_files
from plotPseudocolorPlots import plotPseudocolorPlot
from viridis import generate_viridis_colors


############ (1): GETTING THE RAW IMAGE DATA FOR THE BINARY IMAGE

filesdir = '/home/imoreno/eng_idrive/ChemEngUsers/bwb20181/Documents/coupledCHAC/2023-11-20 16-08-08.978595'
files = [f for f in listdir(filesdir) if isfile(join(filesdir, f)) and f.endswith('.vtu')]

ordered_filedirs = get_sorted_list_of_files(files)
raw_imgs, img_times = plotPseudocolorPlot(ordered_filedirs, filesdir, binary=True, savepscplots=True)


def getMedianAndDiameterEvol(raw_imgs_f, img_times_f):
    median_evol_f = []
    diameters_f = {}
    for i in range(len(raw_imgs_f)):
        contours, hierarchy = cv2.findContours(raw_imgs_f[i], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        diams_i = []

        for cnt in contours:
            cnt_area = cv2.contourArea(cnt)
            cnt_diam = 2*np.sqrt(cnt_area/np.pi)
            diams_i.append(cnt_diam)

        diameters_f[img_times_f[i]] = diams_i

        # Get the median
        if len(diams_i) > 0:
            median_evol_f.append(statistics.median(diams_i))
        else:
            median_evol_f.append(0)
    return median_evol_f, diameters_f

median_evol, diameters = getMedianAndDiameterEvol(raw_imgs, img_times)


# Plot the median evolution
plt.plot(img_times, median_evol)
plt.savefig('Median evolution.png')
result = linregress(img_times, median_evol)


################### PSD EVOLUTION
# Get the bins distribution
flattened_diams = [value for sublist in diameters.values() for value in sublist]
max_diam = max(flattened_diams)
bins_end = math.ceil(max_diam/5)*5  # gets the next multiple of 5 of the max diameter

# Sort out the diams into each bin and plot the histogram evolution
vcolors = generate_viridis_colors(int(len(img_times)+1))
fig, ax = plt.subplots()
i=0
for time, diams in diameters.items():
    ax.hist(diams, bins=int(bins_end/5), range=(0, bins_end), histtype='step', color=vcolors[i], label=str(time))
    i+=1
ax.set_ylabel('Counts')
ax.set_xlabel('Particle diameter')
plt.legend(frameon=False)
plt.savefig('Particle diameter histogram.png', dpi=500)
