#!/bin/bash
for f in angle_msrs/*; do
    python3 convert_angles_to_crds.py "$f" --all > $f\_CALCULATION.txt
done
