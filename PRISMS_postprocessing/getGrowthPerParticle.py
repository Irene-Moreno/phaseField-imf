##################################################################################
# READ THE VTU SOLUTION FILES AND GET THE PARTICLE GROWTH RATES FROM THEM
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


def updateParticleProperties(dict_f, centroid_f, properties_f):
    found_centroid = False
    for key in dict_f.keys():
        if abs(key[0] - centroid_f[0]) <= 5 and abs(key[1] - centroid_f[1]) <= 5:
            # If the centroid is close enough, append the properties to the associated key
            dict_f[key].append(properties_f)
            found_centroid = True
            break

    if not found_centroid:
        dict_f[centroid_f] = [properties_f]

    return dict_f


def getParticleGrowthRate(raw_imgs_f, img_times_f):
    growth_rate_f = {}
    for i in range(len(raw_imgs_f)):
        contours, hierarchy = cv2.findContours(raw_imgs_f[i], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        for cnt in contours:
            M = cv2.moments(cnt)
            # Skip to the next iteration if the particle is broken at the edge (so moments = 0)
            if M['m00']==0.0 or M['m10']==0.0 or M['m01']==0.0:
                continue 
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            print(f'({cx}, {cy})')
            cnt_area = cv2.contourArea(cnt)
            cnt_diam = 2*np.sqrt(cnt_area/np.pi)
        
            # For each contour, append its diameter to a dict of the shape {(cx1, cy1): [diams], (cx2, cy2): [diams]...}
            # growth_rate_f.setdefault((cx, cy),[]).append(cnt_diam)
            growth_rate_f = updateParticleProperties(growth_rate_f, (cx, cy), cnt_diam)
            print(len(growth_rate_f))

    return growth_rate_f

growth_rates = getParticleGrowthRate(raw_imgs, img_times)

# Include a list of 0s for the times prior to the nucleation of the latter particles
for centroid, diams in growth_rates.items():
    if len(diams) < len(img_times)-1:
        n_zeros = len(img_times) -1 - len(diams)
        diams = [0 for i in range(n_zeros)] + diams
    growth_rates[centroid] = diams
    print(len(diams))

print(growth_rates)

# Plot the growth rates in the shape "diameter vs time"
fig, ax = plt.subplots()
# vcolors = generate_viridis_colors(int(len(img_times)+1))

for centroid, diams in growth_rates.items():
    ax.plot(img_times[1:], diams, label=str(centroid))
ax.set_ylabel('Diameters')
ax.set_xlabel('Time')
plt.legend(frameon=False)
plt.savefig('Growth rates.png', dpi=500)
