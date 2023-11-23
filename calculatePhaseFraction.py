
##################################################################################
# READ THE VTU SOLUTION FILES AND EXTRACT THE PHASE FRACTION PER SNAPSHOT
##################################################################################

import meshio
import vtk
import re
from os import listdir
from os.path import isfile, join
from operator import itemgetter
from calculateInductionTime import get_sorted_list_of_files

filesdir = '/home/imoreno/eng_idrive/ChemEngUsers/bwb20181/Documents/coupledCHAC/2023-11-20 16-08-08.978595'
files = [f for f in listdir(filesdir) if isfile(join(filesdir, f)) and f.endswith('.vtu')]
ordered_filedirs = get_sorted_list_of_files(files)


reader = vtk.vtkXMLUnstructuredGridReader()
reader.SetFileName(filesdir + '/' + ordered_filedirs[0])
reader.Update()  # Needed because of GetScalarRange
output = reader.GetOutput()
n_arr = output.GetPointData().GetScalars("n")
# print(n_arr)

for fdir in ordered_filedirs:
    mesh_file = meshio.read(filesdir + '/' + fdir)
    dict_file = mesh_file.points

    dict_file = [list(i) for i in sorted(dict_file, key=itemgetter(0))]

    n_file = mesh_file.get_cell_data
    # n_file = n_file['n']
    print(n_file)

    # print(dict_file)  # 144 coordinate points
    break
