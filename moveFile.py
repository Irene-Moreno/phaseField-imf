
import os
import shutil
from datetime import datetime

## Create the new directory
now = str(datetime.now()).replace(':', '-')
newdir = f'/home/imoreno/eng_idrive/ChemEngUsers/bwb20181/Documents/coupledCHAC/{now}'
os.makedirs(newdir)

## Move files to new directory
results_dir = '/home/imoreno/phaseField-imf/applications/coupledCahnHilliardAllenCahn/'
for file in os.listdir(results_dir):
    if file.startswith('solution') or file.startswith('parameters.prm'):
        this_dir = results_dir + str(file)
        shutil.copy2(this_dir, newdir)
    if file.startswith('solution'):
        os.remove(this_dir)
