#/bin/bash

#cd "${0%/*}" || exit
. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions

restore0Dir


runApplication blockMesh
runApplication topoSet
# runApplication foamToVTK -faceSet plateFaceSet # to check faceSet
runApplication createBaffles -overwrite
runApplication checkMesh


runApplication $(getApplication)

paraFoam -touch-all