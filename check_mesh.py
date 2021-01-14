import glob

solvedGlob = glob.glob('solved_mesh/*.p')
meshGlob = glob.glob('mesh_points/*.p')

solvedList = [int((path.split('/')[1]).replace('.p', '')) for path in solvedGlob]
meshList = [int((path.split('/')[1]).replace('.p', '')) for path in meshGlob]
solvedList.sort()
meshList.sort()

notList = []
for case in meshList:
    if case not in solvedList:
        notList.append(str(case))
print(','.join(notList))
