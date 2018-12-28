import nibabel as nib
import glob
import numpy as np
import argparse
import os

def mask_binary_check(dir_path='./'):
    mask_file_path = os.path.join(dir_path, '*mask*.nii')

    not_binary_file = []
    for file in glob.glob(mask_file_path):
        filearray = nib.load(file).get_data()
        xs, ys, zs = np.where(filearray != 0)
        for x, y, z in zip(xs, ys, zs):
            if filearray[x][y][z] != 1:
                not_binary_file.append(file)
                continue

        print(file, ' : binary checked')

    if len(not_binary_file) != 0:
        for not_binary in not_binary_file:
            print(not_binary, 'is not binary')
        print('=================')
        print(len(not_binary_file), 'files are not binary, please try again!')

    else:
        print('=================')
        print('All mask files are binary, Well done!')

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", '--path', help='input directory path name', default='./')
    args = parser.parse_args()

    dir_path = args.path
    mask_binary_check(dir_path)

if __name__=='__main__':
    main()