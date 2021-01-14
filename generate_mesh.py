import numpy as np
import sys, pickle, os


EXP_DIR = sys.argv[1]
MESH_DIR = EXP_DIR+'/mesh_points/'

if not os.path.exists(MESH_DIR):
    os.mkdir(MESH_DIR)


g_vals = np.linspace(-2,2, num=30)
pb_vals = np.linspace(-2,2, num=30)
count = 0
for g in g_vals:
    for pb in pb_vals:
        pickle.dump((g,pb), open('{}{:03n}.p'.format(MESH_DIR,count), 'wb'))
        count += 1
