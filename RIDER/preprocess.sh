#!/usr/bin/env bash
patient=$1

patients_dir=/nv/vol141/phys_nrf/Emery/dataset/rider

python write_ct_as_nrrd.py $patients_dir/LungCT/${patient}

python structure_loading.py $patients_dir/Segs/${patient} --prefix struct
python mask_generation_with_CT_dimensions.py $patients_dir/${patient}

# Flip and fill masks
python flip_and_fill_masks.py $patients_dir/$patient
mask_dir=$patients_dir/$patient/masks
for mask in $(ls $mask_dir/flipped_and_filled/*nrrd); do
    echo ln -s $mask $mask_dir/
    ln -s $mask $mask_dir/
done

# Create flipped versions that aren't filled
python flip_masks.py $patients_dir/$patient/ --subdirectory original --no-archive
