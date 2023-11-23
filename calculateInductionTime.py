
##################################################################################
# READ THE VTU SOLUTION FILES AND EXTRACT THE INDUCTION TIME
##################################################################################

import meshio
import re
from os import listdir
from os.path import isfile, join

filesdir = '/home/imoreno/eng_idrive/ChemEngUsers/bwb20181/Documents/coupledCHAC/2023-11-20 16-08-08.978595'
files = [f for f in listdir(filesdir) if isfile(join(filesdir, f)) and f.endswith('.vtu')]

def get_sorted_list_of_files(files_f):
    filetimes = []
    for filedir in files_f:
        time_pattern = r'(\d+)'
        time = int(re.search(time_pattern, filedir).group())
        filetimes.append(time) 
    filetimes = sorted(filetimes)
    filetimes[0] = str('00000')

    ordered_filedirs_f = []
    for ordered_time in filetimes:
        for filedir in files_f:
            if str(ordered_time) in filedir:
                ordered_filedirs_f.append(filedir)
    return ordered_filedirs_f


def get_timestep(params_fdir_f):
    fp = open(params_fdir_f)
    for i, line in enumerate(fp):
        if "set Time step " in line:
            r, str_tstep = line.split(' = ')
            timestep_f = float(str_tstep.split('  #')[0])
    return timestep_f


def get_induction_time(ordered_filedirs_f, timestep_f):
    for fdir in ordered_filedirs_f:

        mesh_file = meshio.read(filesdir + '/' + fdir)
        dict_file = mesh_file.point_data
        n = dict_file['n']

        induction_time_f = 1000000000000
        for nvalue in n:
            if nvalue > 0.1:
                time_pattern = r'(\d+)'
                time = re.search(time_pattern, fdir).group()
                induction_time_f = str(float(time)*timestep_f)
                break
        
        if isinstance(induction_time_f, str):  # Once the induction time is found, the loop is exited
            break  # This checks if the induction time is a string, which should be once found
    
    return induction_time_f


ordered_filedirs = get_sorted_list_of_files(files)

params_fdir = filesdir + '/parameters.prm'
timestep = get_timestep(params_fdir)

induction_time = get_induction_time(ordered_filedirs, timestep)
