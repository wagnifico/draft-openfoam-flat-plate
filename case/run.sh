#/bin/bash

#cd "${0%/*}" || exit
. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions

restore0Dir

mode="pimple"
while getopts ":m" option; do
   case $option in
      h) mode=$OPTARG;;
     \?) echo "Error: Invalid option"
         exit;;
   esac
done

cp system/$mode/* system

runApplication blockMesh
runApplication topoSet
# runApplication foamToVTK -faceSet plateFaceSet # to check faceSet
runApplication createBaffles -overwrite
runApplication checkMesh

runApplication $(getApplication)

paraFoam -touch-all