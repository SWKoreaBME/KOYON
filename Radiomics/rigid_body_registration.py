from Registration import registration
from data_utils import *

import os
import nibabel as nib
import numpy as np
import SimpleITK as sitk

'''
(1) population : list of files you want to fix (T2 or T1 nii file in common)
(2) filename : each file you want to fix from list population

Below codes make registrated file from python code
    - Registration method : rigid body registration

* Now existing mask type (sequence) : necro, T2, T1_GD

Version

2018. september 
    Registration T1_nii and T1_mask --> T2

2018. 10. 3 
    (1) necro and whole file included
    (2) function MakeMaskName added

'''

def GetImageFromNII(nii_file):
    '''
    Code to convert nii file to simpleITK image
    :param nii_file: nifti file path
    :return: simpleITK Image format
    '''
    Image=nib.load(nii_file).get_data()
    Image = sitk.GetImageFromArray(Image)
    Image.SetSpacing(target_voxel_size)
    return Image

def MakeMaskName(mask_file):
    '''
    Get Mask name from file

    * When you use this function you have to change name you want

    :param mask_file: mask file name
    :return: wanted mask file name
    '''
    if 'ce' in mask_file:
        return '_ce_to_T2_mask'
    elif 'necro' in mask_file:
        return '_necro_to_T2_mask'

resampled_path='/home/ccids-sw/cest/GBMvsMets/GBM_resampled'
save_path='/home/ccids-sw/cest/GBMvsMets/GBM_registered'

mask_imgs=[img for img in os.listdir(resampled_path) if 'mask' in img]
subjects=list(set([a.split('_')[0] for a in os.listdir(resampled_path)]))

target_voxel_size=(1, 1, 1)

error=[]
phases=['necro', 't1', 't2']

for sub in subjects:

    print('\nsubject -- {} start\n'.format(sub))
    # whole_imgs=os.listdir(os.path.join(resampled_path, sub))
    whole_imgs=[img for img in os.listdir(resampled_path) if sub in img]

    imgs=sorted([os.path.join(resampled_path, a) for a in whole_imgs if 'mask' not in a and 'nii' in a]) # T1_GD, T2
    mask=sorted([os.path.join(resampled_path, a) for a in whole_imgs if 'mask' in a]) # ce, necro, t2 ..

    # print original size
    im_size=nib.load(imgs[1]).shape
    mask_size=nib.load(mask[-1]).shape
    print('Original Size\nref img size -- {}\nref mask size -- {}'.format(im_size,mask_size))

    #convert nifti file to Image
    movingImage=GetImageFromNII(imgs[0]) # T1
    t1_mask=[file for file in mask if 'ce' in file]

    for moving_mask in mask[:-1]+[imgs[0]]:
        movingLabel=GetImageFromNII(moving_mask) # T1 mask
        population=[imgs[1]]

        selx = sitk.ElastixImageFilter()
        selx.SetMovingImage(movingImage)
        selx.SetParameterMap(selx.GetDefaultParameterMap('rigid'))

        for filename in population:

            # name = filename.lstrip(resampled_path).rstrip('_T2.nii.gz') + '_ce_to_T2_mask'
            # name = filename.lstrip(resampled_path).split('.')[0]+'_to_T2_mask'

            if 'mask' in moving_mask:
                name=sub+MakeMaskName(moving_mask)
            else:
                name=moving_mask.lstrip(resampled_path).split('.')[0]+'_to_T2'

            print('{} -- Start'.format(name))

            fixedImage=GetImageFromNII(filename)
            selx.SetFixedImage(fixedImage)
            selx.Execute()

            resultLabel = sitk.Transformix(movingLabel, selx.GetTransformParameterMap())

            #convert Image -> array
            result_array = sitk.GetArrayFromImage(resultLabel)
            image_array = sitk.GetArrayFromImage(fixedImage)
            print('After Size\nimg size -- {}\nmask size -- {}'.format(image_array.shape, result_array.shape))

            #save image
            save_file(name, result_array, save_path, target_voxel_size)
            print('{} -- Saved'.format(name))

            if image_array.shape != result_array.shape: error.append(name)


print('ERROR -- {}'.format(error))