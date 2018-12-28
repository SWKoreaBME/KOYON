import argparse

from GBM_registration_module import registration_GBM as registration
from GBM_mask_binary_check_module import mask_binary_check

'''
    This is main process code for GBMvs.Mets Data
    
    [1] process sequence
        
        (0) Get directory
        (1) resampling
        (2) registration
        (3) save to save path
        
    [2] resample parameters
    
    [3] registration parameters
    
    [4] Way to input directory path
        
        (1) argparser added ( input, output, resampling, voxel size )

'''

# argument parser
parser=argparse.ArgumentParser()
parser.add_argument('-i', '--input_path', help='Input path')
parser.add_argument('-o', '--output_path', help='output path (save path)')
parser.add_argument('-r', '--resample', help='execute resampling (True / False)', default=False, type=bool)
parser.add_argument('-v', '--voxel_size', type=tuple, default=(1,1,1))


args=parser.parse_args()

input_path=args.input_path
output_path=args.output_path
resample=args.resample
target_voxel_size = tuple([int(elem) for elem in args.voxel_size if elem!=','])

error_files=[]

# main procedure

def main():
    registration(input_path, output_path, mask_phases=['necro', 'ce', 't2'], img_phases=['T1GD', 'T2'], img_fix='T2', mask_fix='t2', target_voxel_size=target_voxel_size)

if __name__ == '__main__':
    print('input path : ', input_path)
    print('output path : ', output_path)
    print('resampling : ', resample)
    if resample:
        print('resampling pixel value : ', target_voxel_size)
    main()

    print('Mask Binary Checking Start')
    mask_binary_check(dir_path=output_path)

    if len(error_files) != 0 :
        print('\n=================')
        print('Error files : ', error_files)

    print('Registration Done')