from GBM_utils import *
import os
import argparse

from GBM_mask_binary_check_module import mask_binary_check

parser=argparse.ArgumentParser()
parser.add_argument('-i', '--input_path')
parser.add_argument('-o', '--output_path')
parser.add_argument('-v', '--voxel_size', type=tuple, default=(1,1,1))
args=parser.parse_args()

#=============================

raw_path=args.input_path
save_path=args.output_path
voxel_size=tuple([int(elem) for elem in args.voxel_size if elem!=','])

#=============================

def resampling():
    for subject in os.listdir(raw_path):
        images = [img for img in os.listdir(os.path.join(raw_path, subject)) if 'nii' in img]
        for im in images:
            data = os.path.join(raw_path, subject, im)

            im_file_resampled, im_voxel = resample(data, voxel_size)
            if 'mask' in im:
                im_file_resampled = mask2binary(im_file_resampled)

            new_name = im.split('.nii')[0]

            save_file(new_name, im_file_resampled, save_path, im_voxel)
            print(im_file_resampled.shape)
            print(data, '-- Done')

if __name__=="__main__":
    print('input path : ', raw_path)
    print('output path : ', save_path)
    print('resampling pixel value : ', voxel_size)

    resampling()
    print('resampling Done!')
    print('=================')

    print('Mask Binary Checking Start')
    mask_binary_check()

    print('=================')
    print('All procedure Done.')