#!/bin/sh
module load mpi
source /usr/lib/openfoam/openfoam2206/etc/bashrc

rm -r runs 2> /dev/null || true
mkdir -p runs

cp -r case runs/test
cd runs/test

bash run.sh