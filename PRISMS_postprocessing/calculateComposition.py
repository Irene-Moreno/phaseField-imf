
##################################################################################
# READ THE VTU SOLUTION FILES AND EXTRACT THE PHASE FRACTION
##################################################################################

# The analysis of 24 files took about 40.6 seconds

import re
import time
import meshio
import numpy as np
from os import listdir
from os.path import isfile, join
from matplotlib import pyplot as plt
import matplotlib.tri as tri
import colormaps as cmaps
from calculateInductionTime import get_sorted_list_of_files

start_time = time.time()

def read_VTU_for_coords_and_data_comp(filedir):
    # Grab the snapshot time for the image name
    time_pattern = r'(\d+)'
    time_f = int(re.search(time_pattern, filedir.split('/')[-1]).group())

    # Read the vertices and blocks forming each cell
    mesh = meshio.vtu.read(filedir)
    x_f, y_f, _ = mesh.points.transpose()
    v_f = mesh.point_data['c']
    block_f = mesh.cells_dict['quad']
    
    return x_f, y_f, v_f, block_f, time_f

