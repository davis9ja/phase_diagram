import pickle
import pandas as pd
import seaborn as sns
import glob, os
import numpy as np
import matplotlib.pyplot as plt
import sys

EXP_DIR=sys.argv[1]    

if not os.path.exists(EXP_DIR+'/ensemble/'):
    os.mkdir(EXP_DIR+'/ensemble/')

df = pickle.load(open(EXP_DIR+'/solved_mesh/full_dataframe.p', 'rb'))
print(df)

g_vals = np.linspace(-2,2, num=30)
pb_vals = np.linspace(-2,2, num=30)


fig, ax = plt.subplots(figsize=[10,10])
g = sns.heatmap(df.pivot('g', 'pb', 'gs_eig'), 
                xticklabels=['{:.2f}'.format(x) for x in g_vals], 
                yticklabels=['{:.2f}'.format(y) for y in pb_vals])
plt.ylabel('Ground state eigenvalue')
plt.savefig(EXP_DIR+'/ensemble/gs_eig_plot.png')

fig, ax = plt.subplots(figsize=[10,10])
g = sns.heatmap(df.pivot('g', 'pb', 'abs_error_gs'), 
                xticklabels=['{:.2f}'.format(x) for x in g_vals], 
                yticklabels=['{:.2f}'.format(y) for y in pb_vals],
                vmin=0, vmax=5)
plt.ylabel('Absolute error in ground state eigenvalue')
plt.savefig(EXP_DIR+'/ensemble/abs_error_gs_plot.png')

fig, ax = plt.subplots(figsize=[10,10])
g = sns.heatmap(df.pivot('g', 'pb', 'error_gs'), 
                xticklabels=['{:.2f}'.format(x) for x in g_vals], 
                yticklabels=['{:.2f}'.format(y) for y in pb_vals])
plt.ylabel('Residual error in ground state eigenvalue')
plt.savefig(EXP_DIR+'/ensemble/error_gs_plot.png')

print(df[df['abs_error_gs'] > 1e3])

data_dict_comp = pickle.load(open('data_dict.p', 'rb'))
df_comp = pd.DataFrame(data_dict_comp)
df_comp = df_comp.rename(columns={'abs_error_gs':'abs_error_gs_comp'})

comp_err = df_comp['abs_error_gs_comp']

df['abs_error_gs_comp'] = comp_err.to_numpy()
df['err_reduction'] = df.apply(lambda row: int((row.abs_error_gs_comp - row.abs_error_gs)/row.abs_error_gs_comp*100), axis=1)
#df = df.reset_index()

#df.loc[(df['err_reduction'] > 100), 'err_reduction'] = -10
#print(df[df['err_reduction'] > 100])

fig, ax = plt.subplots(figsize=[10,10])
g = sns.heatmap(df.pivot('g', 'pb', 'err_reduction'), 
                xticklabels=['{:.2f}'.format(x) for x in g_vals], 
                yticklabels=['{:.2f}'.format(y) for y in pb_vals],
                annot=False, fmt='d', 
                robust=True)
plt.ylabel('Percent error reduction from standard reference (std ref abs error - opt ref abs error)/std ref abs error')
plt.savefig(EXP_DIR+'/ensemble/err_reduction_plot.png')
