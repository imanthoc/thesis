#!/bin/bash

if [ "$#" -lt 3 ]; then
    echo "Usage:"
    echo "./auto_run.sh <raw CSV> <ground truth CSV> <run name>"
    exit 1
fi

raw_csv=$1
gt_csv=$2
name=$3

dir=$name\_run

mkdir $dir

python3 calculate_path.py $raw_csv > $dir/path.csv
python3 compare_cl_gt.py $dir/path.csv $gt_csv > $dir/comparison.csv
python3 create_error_maps.py $dir/comparison.csv
