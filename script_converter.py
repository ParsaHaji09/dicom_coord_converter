from pydicom import dcmread
import numpy as np
from pydicom.dataset import Dataset
from rt_utils import image_helper as imhelp
from glob import glob
import matplotlib.pyplot as plt

def get_img_list(path):
    series_data = []
    for file in glob(f"{path}/*.dcm"):
        ds = dcmread(file)
        img1 = ds.pixel_array
        series_data.append(img1)

    return series_data

def get_transformation_matrix(path):
    # load all images into series data
    series_data = []
    for file in glob(f"{path}/*.dcm"):
        ds = dcmread(file)
        series_data.append(ds)

    #transformation matrix that maps 2D pixels to 3D coordinates
    transformation_matrix = imhelp.get_pixel_to_patient_transformation_matrix(series_data)
 
    return transformation_matrix