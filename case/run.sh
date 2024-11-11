#/bin/bash

#cd "${0%/*}" || exit
. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions

runApplication blockMesh
runApplication topoSet
# runApplication foamToVTK -faceSet plateFaceSet # to check faceSet
runApplication createBaffles
runApplication checkMesh

paraFoam -touch-all