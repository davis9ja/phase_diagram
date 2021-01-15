import glob

solvedGlob = glob.glob('target_es_experiment/solved_mesh/*.p')
meshGlob = glob.glob('target_es_experiment/mesh_points/*.p')

solvedList = [int((path.split('/')[2]).replace('.p', '')) for path in solvedGlob]
meshList = [int((path.split('/')[2]).replace('.p', '')) for path in meshGlob]
solvedList.sort()
meshList.sort()

notList = []
for case in meshList:
    if case not in solvedList:
        notList.append(str(case))

print('{:3d} mesh points still missing\n'.format(len(notList)))
print(','.join(notList))
