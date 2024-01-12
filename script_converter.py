#Use pydicom.dcmread function to read dicom files
from pydicom import dcmread
import numpy as np
from rt_utils import image_helper as imhelp
import os
from glob import glob
import matplotlib.pyplot as plt

class ROIData:
    mask: str
    use_pin_hole: bool = False
    approximate_contours: bool = True


def get_transformation_matrix(path):
    # load all images into series data
    series_data = []
    for file in glob(f"{path}/*.dcm"):
        ds = dcmread(file)
        series_data.append(ds)

    #transformation matrix that maps 2D pixels to 3D coordinates
    transformation_matrix = imhelp.get_pixel_to_patient_transformation_matrix(series_data)
    print(transformation_matrix)


    #get_contours_coords only uses roi_data.mask, use_pin_holes, approximate_contours
    #get the contour coordinates
    
    data = dcmread("./test_data/IM-0003-0003.dcm").pixel_array

    #potentially need to edit later
    dumbmask = np.zeros((data.shape[0], data.shape[1], 19), dtype=bool)
    dumbmask[100:250, 100:200, 2:-1] = 1
    third_slice = dumbmask[:, :, 2]
    

    data_roi = ROIData()
    data_roi.mask = dumbmask

    contours, _ = imhelp.find_mask_contours(third_slice, data_roi.approximate_contours)
    result = imhelp.get_contours_coords(data_roi, series_data)

def main():
    #test
    inp = input("File Path: ")
    get_3D_coordinates(inp)


#coords = imhelp.get_contours_coords(series_data)
# data = dcmread("./t2_tse_tra_4/IM-0003-0003.dcm").pixel_array
# dumbmask = np.zeros((data.shape[0], data.shape[1], 19), dtype=bool)
# dumbmask[100:250, 100:200, 2:-1] = 1
# plt.imshow(dumbmask[:, :, 10])
# plt.show()


# _______________________________Rtstruct___________________________________
# rtstruct = RTStructBuilder.create_new(dicom_series_path="./t2_tse_tra_4")
# rtstruct.add_roi(mask=dumbmask, color=[255,0,0], name="RT-Utils ROI!")
# rtstruct.save("./testSliceRT/test2")
