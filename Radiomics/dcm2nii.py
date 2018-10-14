
# coding : utf-8
# author : Hwiyoung Kim
# edited by Sangwook Kim

import os
import dicom2nifti
import dicom2nifti.settings as settings
import nibabel as nib
import numpy as np
import shutil
import argparse

# below code is for parser

parser=argparse.ArgumentParser(description="Type input output path")
parser.add_argument("-i", "--inpath", help="dicom input path")
parser.add_argument("-o","--outpath", help="nifti output path")
args=parser.parse_args()

# above code is for parser

# 처음 만들어지면 영상의 이름이 제멋대로 설정됩니다.
# 따라서 환자 이름 + 시퀀스 를 딴 폴더를 먼저 만들고 나중에 폴더 밖으로 빼내는 작업을 하는 코드입니다.

'''
경로를 적어주시면 됩니다. 
PATH : dicom 영상이 있는 폴더
PATH_out : nii 영상을 저장할 폴더

PATH='/home/ccids-sw/cest/GBMvsMets/dicom/postop_etc_review'
PATH_out='/home/ccids-sw/cest/GBMvsMets/nii/postop_etc_review'
'''

def main(PATH, PATH_out):
    for patient in os.listdir(PATH):
        patient_path = os.path.join(PATH, patient)

    # subject 별로 폴더를 만들기를 원하면 아래 두 줄의 주석을 제거하고 사용하시면 됩니다.
    # patient_out_path = os.path.join(PATH_out, patient)
    #     if not os.path.exists(patient_out_path):
    #         os.makedirs(patient_out_path)
        # patient_path=os.path.join(PATH)
        
        for series in os.listdir(patient_path):
            # 인풋 이미지 경로를 만드는 코드입니다.
            series_path = os.path.join(patient_path, series)

            # 저장경로 + 시퀀스 의 경로를 합치는 코드입니다.
            series_out_path = os.path.join(PATH_out, series)
            
            # 폴더가 없으면 폴더를 만드는 코드입니다.
            if not os.path.exists(series_out_path):
                os.makedirs(series_out_path)

            print(series_path, '-->', series_out_path)
            # dicom 에서 nifti 로 변환하는 코드입니다.
            dicom2nifti.convert_directory(series_path, series_out_path, reorient=False)

            for filename in os.listdir(series_out_path):
                os.rename(os.path.join(series_out_path, filename), os.path.join(series_out_path, series+".nii.gz"))

    # 아래의 코드는 폴더 밖으로 빼내는 코드입니다.
    for series_name in os.listdir(PATH_out):
        series_path = os.path.join(PATH_out, series_name)
        
        for filename in os.listdir(series_path):
            shutil.move(os.path.join(series_path, filename), os.path.join(PATH_out, filename))
        
        # 아래의 코드의 주석을 제거하면 자동으로 폴더가 제거됩니다.
        # (코드를 사용하지 않고도 제거할 수 있으므로 주석처리 하였습니다.)
        if len(os.listdir(os.path.join(PATH_out, series_name)))==0:
            os.rmdir(os.path.join(PATH_out, series_name))

if __name__=="__main__":

    PATH=args.inpath
    PATH_out=args.outpath

    print("Dicom --> Nifti 변환이 시작됩니다")
    main(PATH, PATH_out)
    print("Done")