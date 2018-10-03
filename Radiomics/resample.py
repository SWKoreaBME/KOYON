from data_utils import *
import os

# TODO : Save resampled mask files

raw_path='/home/ccids-sw/Desktop/additional_data'

# origin_path='IDHwt_nii'
# mask_path='IDHwt_mask'

save_path='/home/ccids-sw/Desktop/additional_resampled'
# seq = ['T1', 'T1_GD', 'T2_F']

# whole_path, subjects = data_struct(folder_path=raw_path, mask_path='IDHwt_mask', origin_path='IDHwt_nii')
#-----------------------------------------------------------------------

#TODO: Read raw files and sort them by sequence
voxel_size=(1, 1, 1)

# raw_imgs=os.listdir(raw_path)

for subject in os.listdir(raw_path):
    images=[img for img in os.listdir(os.path.join(raw_path, subject)) if 'nii' in img]
    for im in images:
        data=os.path.join(raw_path, subject, im)

        im_file_resampled, im_voxel = resample(data, voxel_size)
        im_file_resampled = mask2binary(im_file_resampled)

        save_file(im.rstrip('.nii'), im_file_resampled, save_path, im_voxel)
        print(im_file_resampled.shape)
        print(data, '-- Done')

#
# for sub in subjects:
#
#     # os.mkdir(os.path.join(save_path, sub))
#
#     raw_imgs=whole_path[sub]
#
#     for img in raw_imgs:
#
#         print(img, '-- Start')
#
#         if 'mask' in img:
#             im_pt = os.path.join(raw_path, mask_path, img)
#         else:
#             im_pt = os.path.join(raw_path, origin_path, sub, img)
#
#         # Read file
#         im_file=nib.load(im_pt)
#
#         # resample mask image
#         im_file_resampled, im_voxel=resample(im_pt, (0.5, 0.5 ,5))
#         if 'mask' in img:
#             im_file_resampled = mask2binary(im_file_resampled)
#
#         # if 'mask' in img:
#         #     print('{} is mask file -- binary'.format(img))
#         #     im_file_resampled=mask2binary(im_file_resampled)
#
#         # save resampled mask image
#         save_file(img.rstrip('.nii.gz'), im_file_resampled, os.path.join(save_path, sub), im_voxel)
#
#         print(img, '-- Done')