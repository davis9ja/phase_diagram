import glob


EXP_DIR = sys.argv[1]

solvedGlob = glob.glob(EXP_DIR+'/solved_mesh/*.p')
meshGlob = glob.glob(EXP_DIR+'/mesh_points/*.p')

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
