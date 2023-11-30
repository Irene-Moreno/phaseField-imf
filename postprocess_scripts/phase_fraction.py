#!/usr/bin/env python3

import sys
import time
from visit import *

#DeleteAllPlots()

start_time = time.time()

# Step 1: Open a database (the whole .vtu time series)
dbname="/home/imoreno/eng_idrive/ChemEngUsers/bwb20181/Documents/coupledCHAC/2023-11-20 16-08-08.978595/solution-*.vtu database"
OpenDatabase(dbname)

# Step 2: Add plots (using variable "n")
# This variable must be in the range [0,1]
# with 0 representing one phase, 1 representing another phase
# and n=0.5 representing the midpoint accross the interface
AddPlot("Pseudocolor", "n")

# Step 3: Draw the plots
DrawPlots()

# Step 4: Get the number of grid points in the domain
Query("Grid Information")
gpq = GetQueryOutputValue()
# Extracting number of grid points in each direction
num_x_coords = int(gpq[2])
num_y_coords = int(gpq[3])
num_z_coords = int(gpq[4])

# Step 5 Get the area (or volume) of the whole domain
av=0.0
if num_z_coords >= 1:
    Query("Volume")
    # Assign result to variable a
    av=GetQueryOutputValue()
else:
    Query("2D area")
    # Assign result to variable a
    av=GetQueryOutputValue()

# Step 6: Initialize phase fraction and open output file
phasefrac=[0.0]*TimeSliderGetNStates()
# Set the output file name
ofnm="phi_vs_t.txt"
# Open  output file
outF = open(ofnm, "w")

# Step 7: Animate through time and save results
for states in range(TimeSliderGetNStates()):
    #Set slider to state
    SetTimeSliderState(states)
    # Get the time corresponding to the state
    Query("Time")
    # Assign this time to the variable "t"
    t = GetQueryOutputValue()
    # Get the total area (or volume) of domains where n=1 by integration
    Query("Weighted Variable Sum")
    # Set this area (or volume) to the variable wvs
    wvs=GetQueryOutputValue()
    # Calculate phase fraction
    phasefrac[states]=wvs/av
    # Print the state number, time and phase fraction to
    # screen and to files
    print("% d, %.1f, %.5f" %(states, t, phasefrac[states]))
    print >> outF, "% d %.1f %.5f" %(states, t, phasefrac[states])
outF.close()

DeleteAllPlots()
CloseDatabase(dbname)

sys.exit()

print("--- %s seconds ---" % (time.time() - start_time))
