# -*- coding: utf-8 -*-

import sys
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from PIL import Image

#othu_thresholding method
#args: array representation of image 'image_arr', threshold value 'k' (integer)
#output: thresholded input image, value of otsu method function
def otsu_thresholding(image_arr, k):
    #group together pixels according to threshold k
    group0_where = np.where(image_arr <= k)
    group1_where = np.where(image_arr > k)
    group0 = np.column_stack((group0_where[0],group0_where[1]))
    group1 = np.column_stack((group1_where[0],group1_where[1]))
    thres_img = np.copy(image_arr)
    #compute values needed for otsu function
    n0 = group0.shape[0]
    n1= group1.shape[0]
    m0 = np.sum(thres_img[group0[:,0],group0[:,1]]) / n0
    m1 = np.sum(thres_img[group1[:,0],group1[:,1]]) / n1
    m = np.sum(thres_img)/thres_img.size
    n = thres_img.size
    thres_img[group0[:,0],group0[:,1]] = 0
    thres_img[group1[:,0],group1[:,1]] = 255
    otsu_value = (n0/n)*( (m0-m)**2 ) + (n1/n)*( (m1-m)**2 )
    #return thresholded image and otsu value
    results = [thres_img, otsu_value]
    return results
    
#find_otsu_k method
#args: 'image_array' array representation of a grayscale image,
#      'k_range' unique values of intensity in the input image, to be used as threshold values
#output: value of best threshold, best thresholded image
def find_otsu_k(image_arr, k_range):
    max_otsu_value = -1.0
    best_k = -1
    best_thres_img = None
    #use each value of intensity as threshold value, choose best according to otsu method
    for k in k_range:
        thres_results = otsu_thresholding(image_arr, k)
        otsu_value = thres_results[1]
        if max_otsu_value < otsu_value:
            max_otsu_value = otsu_value
            best_k = k
            best_thres_img = thres_results[0]
    
    return best_k, best_thres_img

#script command line input
input_filename = sys.argv[1]	#filename of input image
output_filename = sys.argv[2]   #filename of output image
window_size = int(sys.argv[3])  #window size of adaptive otsu method

#create array representation of the input image in grayscale,
#  if input is an RGB image convert it to grayscale by computing mean of colors
image_array = np.array(Image.open(input_filename))
if image_array.ndim > 2: #input image is color image, convert it to grayscale by computing average value of RGB channels for each pixel
    image_array_gray = np.zeros((image_array.shape[0], image_array.shape[1]))
    for i in range(image_array.shape[0]):
        for j in range(image_array.shape[1]):
            colors = image_array[i, j]
            color_sum = np.sum(colors)
            pixel_intensity = int(color_sum / colors.size)
            image_array_gray[i, j] = pixel_intensity
else:
	image_array_gray = image_array.copy()

#initialize output image
otsu_thres_image = np.zeros((image_array_gray.shape[0],image_array_gray.shape[1]))

#for each pixel of the input image perform otsu method for the specified window containing the pixel
for i in range(image_array_gray.shape[0]):
    for j in range(image_array_gray.shape[1]):
	#compute window boundaries
        row_low_bound = max(0,i-round((window_size-1)/2))
        col_low_bound = max(0,j-round((window_size-1)/2))
        row_up_bound = min(image_array_gray.shape[0],i+window_size-round((window_size-1)/2))
        col_up_bound = min(image_array_gray.shape[1],j+window_size-round((window_size-1)/2))
	#create array of the window neihbourhood to pass to otsu as an argument
        neighbourhood = np.copy(image_array_gray[row_low_bound:row_up_bound, col_low_bound:col_up_bound])
	#compute the relevant coordinates of the pixel inside the window
        neigh_i_coord = np.where(neighbourhood == image_array_gray[i, j])[0][0]
        neigh_j_coord = np.where(neighbourhood == image_array_gray[i, j])[1][0]
	#find unique values of intensities inside the window
        neigh_intensities = [i for i in sorted(np.unique(neighbourhood).tolist())[:-1]]
	#if all the pixels of the window have the same intensity use 70 as threshold
        if len(neigh_intensities) <= 1:
            if image_array_gray[i, j] > 69:
                otsu_thres_image[i, j] = 255
            else:
                otsu_thres_image[i, j] = 0
            continue
        pixel_otsu_results = find_otsu_k(neighbourhood, neigh_intensities)
        otsu_neigh = pixel_otsu_results[1]
        new_intensity = otsu_neigh[neigh_i_coord,neigh_j_coord]
        otsu_thres_image[i, j] = new_intensity

#save output image
new_img = Image.fromarray(np.uint8(otsu_thres_image))
new_img.save(output_filename)
