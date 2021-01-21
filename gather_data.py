import pickle
import pandas as pd
import glob
import numpy as np
import sys

EXP_DIR=sys.argv[1]

# glob the files in solved mesh
fileList = glob.glob(EXP_DIR+'/solved_mesh/*.p')

# gather the dataframes in a list
df_list = []
for filePath in fileList:
    data_point = pickle.load(open(filePath, 'rb'))
    
    # need to wrap numpy arrays as lists so they fit in DF
    for key in data_point.keys():
        value = data_point[key]        
        if type(value) is np.ndarray:
            data_point[key] = [value]

    data_point_df = pd.DataFrame(data_point)
    df_list.append(data_point_df)

# append all dataframes in the list to a single dataframe
mesh_data_df = pd.concat(df_list)

# pickle final dataframe and store in solved_mesh
pickle.dump(mesh_data_df, open(EXP_DIR+'/solved_mesh/full_dataframe.p', 'wb'))
