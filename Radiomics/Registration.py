import SimpleITK as sitk

def registration(fix_im, mov_im):
    '''
    :param fix_im: numpy array fixed image
    :param mov_im: numpy array moving image
    :return: numpy array registrated image
    '''
    fix_im_sitk = sitk.GetImageFromArray(fix_im)
    mov_im_sitk = sitk.GetImageFromArray(mov_im)
    res_im = sitk.Elastix(fix_im_sitk, mov_im_sitk,"rigid")
    res_im = sitk.GetArrayFromImage(res_im)
    return res_im