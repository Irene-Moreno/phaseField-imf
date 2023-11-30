
##################################################################################
# READ THE VTU SOLUTION FILES AND GET THE CONTOUR PLOTS FROM THEM
##################################################################################

import cv2
import meshio
import time
import numpy as np
from os import listdir
from os.path import isfile, join
from matplotlib import pyplot as plt
import matplotlib.tri as tri
import colormaps as cmaps
from calculateInductionTime import get_sorted_list_of_files
from plotPseudocolorPlots import plotPseudocolorPlot


############ (1): GETTING THE RAW IMAGE DATA FOR THE BINARY IMAGE

filesdir = '/home/imoreno/eng_idrive/ChemEngUsers/bwb20181/Documents/coupledCHAC/2023-11-20 16-08-08.978595'
files = [f for f in listdir(filesdir) if isfile(join(filesdir, f)) and f.endswith('.vtu')]

ordered_filedirs = get_sorted_list_of_files(files)
raw_imgs = plotPseudocolorPlot(ordered_filedirs, filesdir, binary=True)
contours, hierarchy = cv2.findContours(raw_imgs[7], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print(contours)

# plt.imshow(X, interpolation='nearest')
# plt.savefig("numpy_figure_contour.png", dpi=300)
