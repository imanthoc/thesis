#!/bin/bash
for f in angle_msrs_2/*; do
    printf "$f\n"
    python3 single_points_scripts/visualize_angle_timeseries.py $f
    printf '\n'
done
