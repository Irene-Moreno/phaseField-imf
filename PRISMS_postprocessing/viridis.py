
###### GENERATE DIVISIONS OF THE VIRIDIS COLOR PALETTE

import matplotlib.cm as cm
import matplotlib.colors as mcolors

def generate_viridis_colors(num_colors):
    viridis = cm.get_cmap('viridis', num_colors)
    norm = mcolors.Normalize(vmin=0, vmax=num_colors - 1)
    hex_colors = [mcolors.to_hex(viridis(norm(i))) for i in range(num_colors)]
    return hex_colors
