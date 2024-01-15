
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
P_fit_eqs = {}; Js = []; tgs = []; R2s = []
fig2, ax2 = plt.subplots()
i=0

for index, row in SalAc_Aceto.iterrows():

    # Read and process the dataframe
    label = str(row.Actual_conc_g_g)[:4]+'_'+str(row.Isothermal_temp)[:4]
    induction_times = [row._1_CB_Induction_Time, row._2_CB_Induction_Time, row._3_CB_Induction_Time, row._4_CB_Induction_Time, row._5_CB_Induction_Time]
    induction_times.sort()
    P = [1/5, 2/5, 3/5, 4/5, 5/5]
    ln1_P = [np.log(1-p) for p in P]
    ln1_P_inf_removed = ln1_P
    ln1_P_inf_removed[-1] = np.log(0.00000001)

    # Plot the linearized data
    ax2.plot(induction_times, ln1_P_inf_removed, linestyle='--', color=viridis_colors[i])
    ax2.plot(induction_times[:-1], ln1_P[:-1], linestyle='-', color=viridis_colors[i], label=label)
    i+=1

    # Calculate the J and tg values (without the last value)
    result = linregress(induction_times[:-1], ln1_P[:-1])  # Not using the last value (P=1, log(1-P)=-inf) to get k1, k2
    P_fit_eqs[index] = [result.slope, result.intercept, result.rvalue]

    V = row.Sample_volume
    J = -result.slope/V
    tg = result.intercept/(J*V)

    Js.append(J)
    tgs.append(tg)
    R2s.append(result.rvalue**2)

ax2.set_ylabel('ln(1-P)')
ax2.set_xlabel('Induction time')
plt.legend(frameon=False)
plt.savefig('Linearized Ps.png', dpi=500)
plt.close()

# NOTE: It's normal to have very different values of J
SalAc_Aceto["J"] = Js
SalAc_Aceto["tg"] = tgs
SalAc_Aceto["R^2"] = R2s


# Get initial estimates for the parameters in exponential fitting
avg_SalAc_Aceto = SalAc_Aceto.mean(numeric_only=True)
print(avg_SalAc_Aceto["J"])
print(avg_SalAc_Aceto["tg"])
print(avg_SalAc_Aceto["Sample_volume"])

########################## GETTING THE k1 AND k2 VALUES
# Filter out the experiments for which R^2 < 0.9
filtered_SaAc = SalAc_Aceto.loc[SalAc_Aceto['R^2'] >= 0.9]

# Calculate the supersaturation in each experiment and linearize the data
filtered_SaAc["1/S"] = 1/(filtered_SaAc['Actual_conc_g_g'] - filtered_SaAc['Solubility'])
filtered_SaAc["ln(J)"] = np.log(np.array(filtered_SaAc["J"]))

result = linregress(filtered_SaAc["1/S"], filtered_SaAc["ln(J)"])
k1 = np.exp(result.intercept)
k2 = -result.slope
R2 = result.rvalue**2

fig3, ax3 = plt.subplots()
ax3.scatter(filtered_SaAc["1/S"], filtered_SaAc["ln(J)"])
ax3.set_ylabel('ln(J)')
ax3.set_xlabel('1/S')

plt.savefig('Linearized Js.png', dpi=500)
plt.close()

print(k1)
print(k2)
print(R2)
