import os
import numpy as np
import nibabel as nib
import scipy.misc
import random

from PIL import Image
from skimage import transform, io
import torchvision.transforms as transforms

import torch
'''
    Dataset.py

    Data handling functions
'''
def nii2numpy(nii):
    return nib.load(nii).get_data()

def save_image(img, sub, path):
    dt = 0
    w, h, n = img.shape
    if (w, h) == (512, 512):
        for x in range(n):
            try:
                scipy.misc.imsave(path+'/{}_{}.jpg'.format(sub, dt), img[:, :, x])
                dt += 1
            except:
                continue

def get_ids(dir):
    """Returns a list of the ids in the directory"""
    """.jpg 를 빼는 과정"""
    return (f[:-4] for f in os.listdir(dir))

def split_ids(ids, n=119):
    """Split each id in n, creating n tuples (id, k) for each id"""
    return ((id, i) for i in range(n) for id in ids)

def split_train_val(img_dir, val_percent=0.1):
    subs = os.listdir(img_dir)
    for i, s in enumerate(subs):
        pth = os.path.join(img_dir, s)
        ids = get_ids(pth)
        # ids = split_ids(ids, i)

        dataset = list(ids)
        length = len(dataset)
        n = int(length * val_percent)
        random.shuffle(dataset)

        if i == 0:
            res = {'train': dataset[:-n], 'val': dataset[-n:]}
        else:
            res['train'] += dataset[:-n]
            res['val'] += dataset[-n:]

        random.shuffle(res['train'])
        random.shuffle(res['val'])

    return res

def MakeDataset(img_dir, mask_dir, val_percent=0.1, img_size=256):
    res = split_train_val(img_dir, val_percent=val_percent)

    dataset = {}
    for key in res.keys():
        dataset[key] = []

    for key in res.keys():
        for image in res[key]:
            name = image[:7]

            im_path = os.path.join(img_dir, name, (image + '.jpg'))
            mask_path = os.path.join(mask_dir, name, (image + '.jpg'))

            # get array
            image_array=transform.resize(io.imread(im_path), (1, img_size, img_size))
            mask_array=transform.resize(io.imread(mask_path), (1, img_size, img_size))

            image_array = transforms.ToTensor()(image_array).cuda(0)
            mask_array = transforms.ToTensor()(mask_array).cuda(0)

            # merge
            dataset[key] += [image_array, mask_array]

    return dataset

def ReadImage(image, dir, im_size):
    name = image[:7]
    im_path = os.path.join(dir, name, (image + '.jpg'))
    image_array = transform.resize(io.imread(im_path), (im_size, im_size, 1))
    image_array = transforms.ToTensor()(image_array)
    image_array=torch.unsqueeze(image_array, 0).float()
    return image_array

# # Get Data =============================================
# im_path='/path/to/img_dir'
# mask_path='path/to/mask_dir'
#
# save_im_path='/media/ccids-sw/2TB/segmentation_data/train'
# save_mask_path='/media/ccids-sw/2TB/segmentation_data/train_masks'
#
# images=[os.path.join(im_path, img) for img in os.listdir(im_path)]
# masks=[os.path.join(mask_path, img) for img in os.listdir(mask_path)]
#
# subjects=[img[:7] for img in os.listdir(im_path)]
#
# for subject in subjects:
#     image=[img for img in images if subject in img]
#     mask=[ma for ma in masks if subject in ma]
#
#     if not os.path.exists(os.path.join(save_im_path, subject)):
#         os.mkdir(os.path.join(save_im_path, subject)); os.mkdir(os.path.join(save_mask_path, subject))
#
#     print(image, mask)
#     image_array=nii2numpy(image[0])
#     mask_array=nii2numpy(mask[0])
#
#     save_image(img=image_array, sub=subject, path= os.path.join(save_im_path, subject))
#     save_image(img=mask_array, sub=subject, path=os.path.join(save_mask_path, subject))
#
# # Saved =====================================

# TODO : DataLoader
# img_dir='/media/ccids-sw/2TB/segmentation_data/train'
# res=split_train_val(img_dir=img_dir, val_percent=0.1)
# print(res['train'])