Note: All CSVs are required to have a header

1> calculate_path.py
    input:  Raw angle CSV
    output: Calculated path CSV

2> compare_cl_gt.py
    input:  Calculated path CSV & Corresponding ground Truth CSV
    output: Comparison CSV

3> create_error_maps.py
    input:  Comparison CSV
    output: error maps & error per point CSV
