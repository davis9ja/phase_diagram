import pickle
import pandas as pd
import seaborn as sns
import glob, os
import numpy as np
import matplotlib.pyplot as plt

fileList = glob.glob('solved_mesh/*.p')
data_dict = {'g':[], 'pb':[], 'gs_eig':[], 'abs_error_gs':[], 'error_gs':[], 'eta1B_norm':[], 'eta2B_norm':[]}
g_vals = np.linspace(-2,2, num=30)
pb_vals = np.linspace(-2,2, num=30)
param_grid = []
for g in g_vals:
    for pb in pb_vals:
        param_grid.append((g,pb))
    

if not os.path.exists('ensemble/'):
    os.mkdir('ensemble/')

for filePath in fileList:
    data_point = pickle.load(open(filePath, 'rb'))
    data_dict['g'].append(data_point['g'])
    data_dict['pb'].append(data_point['pb'])
    data_dict['gs_eig'].append(data_point['gs_eig'])
    data_dict['abs_error_gs'].append(data_point['abs_error_gs'])
    data_dict['error_gs'].append(data_point['error_gs'])
    data_dict['eta1B_norm'].append(data_point['eta1B_norm'])
    data_dict['eta2B_norm'].append(data_point['eta2B_norm'])

df = pd.DataFrame(data_dict)
df['log_eta2B_norm'] = df.apply(lambda row: np.log(row.eta2B_norm), axis=1)

df = df.sort_values(['g', 'pb']).reset_index()
print(df.shape[0])

fig, ax = plt.subplots(figsize=[10,10])
g = sns.heatmap(df.pivot('g', 'pb', 'gs_eig'), 
                xticklabels=['{:.2f}'.format(x) for x in g_vals], 
                yticklabels=['{:.2f}'.format(y) for y in pb_vals])
plt.ylabel('Ground state eigenvalue')
plt.savefig('ensemble/gs_eig_plot.png')

fig, ax = plt.subplots(figsize=[10,10])
g = sns.heatmap(df.pivot('g', 'pb', 'abs_error_gs'), 
                xticklabels=['{:.2f}'.format(x) for x in g_vals], 
                yticklabels=['{:.2f}'.format(y) for y in pb_vals])
plt.ylabel('Absolute error in ground state eigenvalue')
plt.savefig('ensemble/abs_error_gs_plot.png')

fig, ax = plt.subplots(figsize=[10,10])
g = sns.heatmap(df.pivot('g', 'pb', 'error_gs'), 
                xticklabels=['{:.2f}'.format(x) for x in g_vals], 
                yticklabels=['{:.2f}'.format(y) for y in pb_vals])
plt.ylabel('Residual error in ground state eigenvalue')
plt.savefig('ensemble/error_gs_plot.png')

data_dict_comp = pickle.load(open('data_dict.p', 'rb'))
df_comp = pd.DataFrame(data_dict_comp)
df_comp = df_comp.rename(columns={'abs_error_gs':'abs_error_gs_comp'})
print(df_comp)
comp_err = df_comp['abs_error_gs_comp']

df['abs_error_gs_comp'] = comp_err.to_numpy()
df['err_reduction'] = df.apply(lambda row: int(abs(row.abs_error_gs_comp - row.abs_error_gs)/row.abs_error_gs_comp*100), axis=1)
#df = df.reset_index()
print(df)
df.loc[(df['err_reduction'] > 100), 'err_reduction'] = -1
#print(df[df['err_reduction'] > 100])

fig, ax = plt.subplots(figsize=[10,10])
g = sns.heatmap(df.pivot('g', 'pb', 'err_reduction'), 
                xticklabels=['{:.2f}'.format(x) for x in g_vals], 
                yticklabels=['{:.2f}'.format(y) for y in pb_vals],
                annot=True, fmt='d')
plt.ylabel('Percent error reduction from standard reference')
plt.savefig('ensemble/err_reduction_plot.png')
