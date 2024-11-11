#!/bin/sh
module load mpi
source /usr/lib/openfoam/openfoam2206/etc/bashrc


rm -r runs/case
cp -r case runs/
cd runs/case

bash run.sh