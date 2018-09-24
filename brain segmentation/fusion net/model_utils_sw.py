from Dataset import *

import torch
import torch.nn as nn
import torch.utils as utils
import torch.nn.init as init
import torch.utils.data as data
import torchvision.utils as v_utils
import torchvision.datasets as dset
import torchvision.transforms as transforms
from torch.autograd import Variable

def MaskToBinary(img):
    '''
    :param mask_resampled_img: numpy array; Resampled numpy array
    :return: mask_binary_img: numpy array with binary data
    '''
    roi = np.where(img >= np.mean(img))
    roi = list(roi)
    size = img.shape
    mask_binary_img = np.zeros(size)
    for x, y, z in zip(roi[0], roi[1], roi[2]):
        mask_binary_img[x][y][z] = 1
    mask_binary_img = mask_binary_img.astype(dtype='int')

    return mask_binary_img

def MaskToBinary2D(img):
    '''
    :param mask_resampled_img: numpy array; Resampled numpy array
    :return: mask_binary_img: numpy array with binary data
    '''
    roi = np.where(img >= np.max(img)*0.7)
    roi = list(roi)
    size = img.shape
    mask_binary_img = np.zeros(size)
    for x, y in zip(roi[0], roi[1]):
        mask_binary_img[x][y] = 1
    mask_binary_img = mask_binary_img.astype(dtype='int')

    return mask_binary_img

def DiceCoefficient(gt, pred):
    # https://stackoverflow.com/questions/31273652/how-to-calculate-dice-coefficient-for-measuring-accuracy-of-image-segmentation-i
    gt = np.array(gt.data)
    pred = MaskToBinary(np.array(pred.data))
    k = 1
    dice = np.sum(pred[gt == k] == k) * 2.0 / (np.sum(pred[pred == k] == k) + np.sum(gt[gt == k] == k))
    return dice

def BatchSet(batch, img_dir, mask_dir, img_size, cuda=True):
    for i, image in enumerate(batch):
        im = ReadImage(image=image, dir=img_dir, im_size=img_size)
        mask = ReadImage(image=image, dir=mask_dir, im_size=img_size)

        if i == 0:
            im_batch = im
            mask_batch = mask
        else:
            im_batch = torch.cat((im_batch, im), 0)
            mask_batch = torch.cat((mask_batch, mask), 0)

    if cuda:
        return im_batch.cuda(0), mask_batch.cuda(0)
    else:
        return im_batch, mask_batch

def ValidDice(val_imgs, val_labels, fusion):
    dice_sum = 0
    for i, data in enumerate(zip(val_imgs, val_labels)):
        img, label = data

        img = torch.unsqueeze(img, 0)
        label = torch.unsqueeze(label, 0)

        x = Variable(img).cuda(0)
        y_ = Variable(label).cuda(0)
        y = fusion.forward(x)

        # dice coefficient
        dice_sum += DiceCoefficient(y_, y)
    return dice_sum / (i + 1)


def MakeVal(batch_size, img_size, train_list, cuda=True, img_dir='/media/ccids-sw/2TB/segmentation_data/train_original', mask_dir='/media/ccids-sw/2TB/segmentation_data/train_masks_original'):
    for i, image in enumerate(train_list):
        if i == batch_size:
            break

        im = ReadImage(image=image, dir=img_dir, im_size=img_size)
        mask = ReadImage(image=image, dir=mask_dir, im_size=img_size)

        if i == 0:
            im_batch = im
            mask_batch = mask
        else:
            im_batch = torch.cat((im_batch, im), 0)
            mask_batch = torch.cat((mask_batch, mask), 0)

    if cuda:
        return im_batch.cuda(0), mask_batch.cuda(0)
    else:
        return im_batch, mask_batch
