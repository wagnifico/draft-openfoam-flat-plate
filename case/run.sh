#/bin/bash

#cd "${0%/*}" || exit
. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions

runApplication blockMesh

paraFoam -touch-all