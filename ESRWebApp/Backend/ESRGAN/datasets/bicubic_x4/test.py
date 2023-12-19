import numpy as np
from skimage.io import imsave, imread
from skimage import img_as_float
import sys
sys.path.append('..')
from imresize import *
import cv2
import os


#path = os.listdir('lr_x4')

# 1. Load original image and do imresize+save to lr folder
def downscale(hrpath,lrpath):
	image_list = os.listdir(hrpath)

	for index, image_name in enumerate(image_list):
		img_uint8 = cv2.imread(os.path.join(hrpath, image_name))
		height, width, channels = img_uint8.shape
		new_height = height//4
		new_width = width//4
		new_size = (new_height,new_width)
		new_img_uint8 = imresize(img_uint8, output_shape=new_size)
		imsave(os.path.join(lrpath , image_name), new_img_uint8)
		im_bgr = cv2.imread(f'{lrpath}/{image_name}')
		im_rgb = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2RGB)
		cv2.imwrite(os.path.join(lrpath , image_name),im_rgb)
		print('saved image' , image_name)
		
		
downscale('hr_img','lr_x4')
#img_double = img_as_float(img_uint8)
#new_img_double = imresize(img_double, output_shape=new_size)
#imsave('py_0000_double.png', convertDouble2Byte(new_img_double))

# 2. Load images resized by python's imresize() and compare with images resized by MatLab's imresize()
#matlab_uint8 = imread('0000_uint8.png')
#python_uint8 = imread('py_0000_uint8.png')
#matlab_double = imread('0000_double.png')
#python_double = imread('py_0000_double.png')
#diff_uint8 = matlab_uint8.astype(np.int32) - python_uint8.astype(np.int32)
#diff_double = matlab_double.astype(np.int32) - python_double.astype(np.int32)
#print ('Python/MatLab uint8 diff: min =', np.amin(diff_uint8), 'max =', np.amax(diff_uint8))
#print ('Python/Matlab double diff: min =', np.amin(diff_double), 'max =', np.amax(diff_double))
