from GBM_utils import save_file, mask2binary

import collections
import os
import SimpleITK as sitk
import nibabel as nib

def GetImageFromNII(nii_file, target_voxel_size):
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
    else:
        return ''

def registration_GBM(input_path, save_path, mask_phases=['necro', 't2', 'ce'], img_phases=['T1GD', 'T2'], img_fix='T2',
                     mask_fix='t2', target_voxel_size=(1, 1, 1)):
    errors = []
    subjects = list(set([a.split('_')[0] for a in os.listdir(input_path)]))

    for sub in subjects:
        whole_imgs = [img for img in os.listdir(input_path) if sub in img]
        mask_dict = collections.defaultdict()
        img_dict = collections.defaultdict()

        for phase in mask_phases:
            try:
                mask_dict[phase] = \
                [os.path.join(input_path, file) for file in whole_imgs if 'mask' in file and phase in file][0]
            except:
                continue

        for phase in img_phases:
            try:
                img_dict[phase] = \
                [os.path.join(input_path, file) for file in whole_imgs if 'mask' not in file and phase in file][0]
            except:
                continue

        movingImage = GetImageFromNII(img_dict['T1GD'], target_voxel_size)
        fixedImage = GetImageFromNII(img_dict['T2'], target_voxel_size)

        # first registration setting
        selx = sitk.ElastixImageFilter()
        selx.SetMovingImage(movingImage)
        selx.SetFixedImage(fixedImage)
        selx.SetParameterMap(selx.GetDefaultParameterMap('rigid'))

        # execute first registration (original files registration)
        resultImage = selx.Execute()

        # save first registered Image
        result_array = sitk.GetArrayFromImage(resultImage)
        image_array = sitk.GetArrayFromImage(fixedImage)

        if result_array.shape != image_array.shape:
            errors.append(img_dict['T1GD'].lstrip(input_path))

        else:
            name = img_dict['T1GD'].lstrip(input_path).split('.')[0] + '_to_' + img_fix
            save_file(name, result_array, save_path, target_voxel_size)

        # Registration other mask files

        if mask_fix in mask_phases:
            mask_phases.remove(mask_fix)

        for phase in mask_phases:
            try:
                movingLabel = GetImageFromNII(mask_dict[phase], target_voxel_size)
                resultLabel = sitk.Transformix(movingLabel, selx.GetTransformParameterMap())
            except:
                continue

            # save first registered Image
            result_array = sitk.GetArrayFromImage(resultLabel)
            image_array = sitk.GetArrayFromImage(fixedImage)

            if result_array.shape != image_array.shape:
                errors.append(mask_dict[phase].lstrip(input_path))

            else:
                name = sub + MakeMaskName(mask_dict[phase])
                result_array = mask2binary(result_array)
                save_file(name, result_array, save_path, target_voxel_size)

    if len(errors) != 0:
        print('below files failed !!')
        print('\n=====================\n')

        for error_file in errors:
            print(error_file)

        print('total ', len(errors), 'failed registration')

    else:
        print('\n=====================\n')
        print('All files successfully registered!')
        print('\nregistration Done')

if __name__=='__main__':

    print('\n\tThis is registration code')
    print('\tPlease import this function somewhere else!')

    print('\n\t== How to import ==')
    print('\n\t(1) go to python file')
    print('\n\t(2) above python file write \n\t"from Registration_GBM import registration_GBM"')

    print('\n\tGood bye')