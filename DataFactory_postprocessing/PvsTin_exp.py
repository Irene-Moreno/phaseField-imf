
#################################################################################
#    PULL DATA FROM MASTER SHEET AND PLOT P vs tIN CURVES
#################################################################################

def safe_float_convert(x):
    try:
        float(x)
        return True # numeric, success!
    except ValueError:
        return False # not numeric
    except TypeError:
        return False # null type


import pandas as pd
import numpy as np
from scipy.stats import linregress
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt


########################## READING THE FILE
# Read the file
xlsx = pd.ExcelFile("/home/imoreno/eng_idrive/ChemEngUsers/bwb20181/Documents/DataFactory_postprocessing/Experimental Master Sheet (1).xlsx")
MasterSheet = pd.read_excel(xlsx, 'Kinetics')
SalAc_Aceto = MasterSheet.loc[MasterSheet['Solute'] == "Salicyclic Acid"]  # typo in the sheet, wrote typo here too till its fixed
SalAc_Aceto = SalAc_Aceto.drop(columns=['FD Induction Time (s)', 'FD Nucleation Rate (#/s)', 'FD Growth Rate d90 (um/s)', '1 CB Nucleation Rate (#/s)', '2 CB Nucleation Rate (#/s)', '3 CB Nucleation Rate (#/s)', '4 CB Nucleation Rate (#/s)', '5 CB Nucleation Rate (#/s)', 
                                        '1 CB Growth Rate fit to all (um/s)', '2 CB Growth Rate fit to all (um/s)', '3 CB Growth Rate fit to all (um/s)', '4 CB Growth Rate fit to all (um/s)', '5 CB Growth Rate fit to all (um/s)', '1 CB Mean Aspect Ratio', '2 CB Mean Aspect Ratio', 
                                        '3 CB Mean Aspect Ratio', '4 CB Mean Aspect Ratio', '5 CB Mean Aspect Ratio', 'Mean CB Mean Aspect Ratio', 'SD CB Mean Aspect Ratio', 'Crystal Shape', 'Polymorph Form', 'Comments', 'Unnamed: 55', 'Unnamed: 56', 'Unnamed: 57', 'Unnamed: 58'])

# Converting the induction time numbers into floats
for i in range(1,6):
    mask = SalAc_Aceto[str(i) + ' CB Induction Time (s)'].map(safe_float_convert)
    SalAc_Aceto = SalAc_Aceto.loc[mask]
    # Renaming some columns to make processing easier
    SalAc_Aceto.rename(columns = {str(i) + ' CB Induction Time (s)':'_'+str(i) + '_CB_Induction_Time'}, inplace = True)
    SalAc_Aceto.rename(columns = {'Actual Conc (g/g solvent)':'Actual_conc_g_g'}, inplace = True)
    SalAc_Aceto.rename(columns = {'Isothermal Temp':'Isothermal_temp'}, inplace = True)

# Filter out rows with missing measurements
SalAceto_NaNs = SalAc_Aceto[SalAc_Aceto.isna().any(axis=1)]  # Creates a dframe with the rows containing a nan
SalAc_Aceto = pd.concat([SalAc_Aceto, SalAceto_NaNs]).drop_duplicates(keep=False)  # Excludes those rows from the original
SalAc_Aceto = SalAc_Aceto.sort_values(by = 'Actual_conc_g_g') 


########################## GETTING THE PROBABILITY CURVES
# Plot the probability curves
viridis_colors = ['#fde725', '#e2e418', '#c2df23', '#a5db36', '#86d549', '#69cd5b', '#52c569', '#3bbb75', '#2ab07f', '#21a685', '#1e9b8a', '#21918c', '#25858e', '#297a8e', '#2d708e', '#32648e', '#38588c', '#3e4c8a', '#433e85', '#472f7d', '#482173', '#471164', '#440154']
fig, ax = plt.subplots()
i=0
for index, row in SalAc_Aceto.iterrows():
    induction_times = [row._1_CB_Induction_Time, row._2_CB_Induction_Time, row._3_CB_Induction_Time, row._4_CB_Induction_Time, row._5_CB_Induction_Time]
    induction_times.sort()
    P = [1/5, 2/5, 3/5, 4/5, 5/5]  # From paper (M=5, m_t = [1, 2, 3, 4, 5])
    ax.plot(induction_times, P, color=viridis_colors[i], label=str(row.Actual_conc_g_g)[:4]+'_'+str(row.Isothermal_temp)[:4])
    i+=1

plt.legend(frameon=False)
plt.savefig("PvsTin.png", dpi=500)
plt.close()


########################## GETTING THE J AND tg VALUES
# Get the sample volume (in mL): g_solvent/density_solvent (g/mL)
SalAc_Aceto["Sample_volume"] = SalAc_Aceto["Actual Mass Solvent (g)"]/SalAc_Aceto["Density of Solvent (g/mL)"]

# Calculate the solubility for each experiment
solubility = []
for T in SalAc_Aceto['Isothermal_temp']:
    solubility.append(1E-05*(T**2) + 0.0002*T + 0.0159)  # From solubility data in Detherm
SalAc_Aceto["Solubility"] = solubility


# NOTE: TRY USING CURVE FIT FROM SCIPY, FITTING THE WHOLE FUNCTION, AND NOT HAVING TO TAKE ONE POINT OFF TO
# LINEARIZE THE EQUATION (THAT MAKES IT VERY INACCURATE)


# Linearize the probability and induction time values
P_fit_eqs = {}; Js = []; tgs = []; stds = []
fig2, ax2 = plt.subplots()
i=0

for index, row in SalAc_Aceto.iterrows():

    # Read and process the dataframe
    label = str(row.Actual_conc_g_g)[:4]+'_'+str(row.Isothermal_temp)[:4]
    induction_times = [row._1_CB_Induction_Time, row._2_CB_Induction_Time, row._3_CB_Induction_Time, row._4_CB_Induction_Time, row._5_CB_Induction_Time]
    induction_times.sort()
    P = [1/5, 2/5, 3/5, 4/5, 5/5]

    # Plot the data
    ax2.plot(induction_times, P, linestyle='-', color=viridis_colors[i], label=label)
    i+=1

    # Calculate the J and tg values
    prms_guess = [1., -1., -0.0023903, 0.5906]  # A, B, C, D       # 1
    popt, pcov = curve_fit(lambda t, a, b, c, d: b*np.exp(c*t + d) + a, induction_times, P, p0=(prms_guess[0], prms_guess[1], prms_guess[2], prms_guess[3]), maxfev = 100000000)

    P_fit_eqs[index] = [popt[0], popt[1], popt[2], popt[3], pcov]

    V = row.Sample_volume               # eq: P(t) = A + B*exp(C*t + D)
    J = -popt[2]/V                      # J= -C/V
    tg = popt[3]/(J*V)                  # tg = D/JV

    Js.append(J)
    tgs.append(tg)
    stds.append(np.sqrt(np.diag(pcov)))

ax2.set_ylabel('P(t)')
ax2.set_xlabel('Induction time')
plt.legend(frameon=False)
plt.savefig('PvsIndT.png', dpi=500)
plt.close()

# NOTE: It's normal to have very different values of J
SalAc_Aceto["J"] = Js
SalAc_Aceto["tg"] = tgs
SalAc_Aceto["std"] = stds


########################## GETTING THE k1 AND k2 VALUES
# Calculate the supersaturation in each experiment and linearize the data
SalAc_Aceto["1/S"] = 1/(SalAc_Aceto['Actual_conc_g_g'] - SalAc_Aceto['Solubility'])

# prms_guess = [1., -1., -0.0023903, 0.5906]  # A, B, C, D       # 1
popt, pcov = curve_fit(lambda t, a, b: a*np.exp(b*t), SalAc_Aceto["1/S"], SalAc_Aceto["J"], maxfev = 100000000)

k1 = popt[0]
k2 = -popt[1]
std = pcov

fig3, ax3 = plt.subplots()
ax3.scatter(SalAc_Aceto["1/S"], SalAc_Aceto["J"])
ax3.set_ylabel('J')
ax3.set_xlabel('1/S')

plt.savefig('Jvs1_S.png', dpi=500)
plt.close()

print(k1)
print(k2)
print(std)
