#/bin/bash

#cd "${0%/*}" || exit
. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions

runApplication blockMesh
runApplication topoSet
runApplication foamToVTK -faceSet plateFaceSet

paraFoam -touch-all