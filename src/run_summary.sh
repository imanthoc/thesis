#!/bin/bash
for f in angle_msrs/*; do
    printf "$f\n"
    python3 convert_angles_to_crds.py "$f" -O --legacy
    python3 convert_angles_to_crds.py "$f" -O --lsq
    printf '\n'
done
