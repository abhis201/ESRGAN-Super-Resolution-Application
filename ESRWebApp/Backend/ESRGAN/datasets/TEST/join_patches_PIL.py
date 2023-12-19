import cv2
import os
import numpy as np
import PIL
from PIL import Image
import shutil
import pandas as pd


def reformat_dirs(path1, path2, path3):
    shutil.rmtree(os.path.join(path1))
    shutil.rmtree(os.path.join(path2))
    shutil.rmtree(os.path.join(path3))
    print("Removed!")
    os.rename('hr_shift_patches',path1)
    os.rename('lr_shift_patches',path2)
    os.rename('sr_shift_patches',path3)
    print("Renamed!!")


def join_cropped_image(path, height, width, size):

    num_row_images = height//size
    num_col_images = width//size

    list_im_col = []
    i=0
    if(not(os.path.exists(f'{path}_shift_patches'))):
        os.mkdir(f'{path}_shift_patches')
        os.mkdir(f'{path}_concat')

    for j in range(num_row_images):
        list_im_row = []
        image_list = os.listdir(path)
        image_list.sort()
        for index,image_name in enumerate(image_list):
                img = cv2.imread(os.path.join(path, image_name))
                list_im_row.append(img)
                print(f'index_{index}')
                print(f'{image_name}')
                if(not(os.path.exists(f'{path}_shift_patches/{image_name}'))):
                    shutil.move(f'{path}/{image_name}',os.path.join(f'{path}_shift_patches'))    
                i = i+1
                print(i)
                if i>=num_col_images:
                    i=0
                    break
                    
        img_row = []
        k=0
        for k in range(num_col_images):
            img_row.append(np.asarray(list_im_row[k]))
        imgs_comb = np.hstack(img_row)
        imgs_row = Image.fromarray(imgs_comb)
        list_im_col.append(imgs_row)

    img_col = []
    l=0
    for l in range(num_row_images):
        img_col.append(np.asarray(list_im_col[l]))
    imgs_comb_vert = np.vstack(img_col)
    imgs_comb_all = Image.fromarray(imgs_comb_vert)
    imgs_comb_all.save( f'{image_name.split("_")[0]}.png' )
    im_bgr = cv2.imread( f'{image_name.split("_")[0]}.png')
    im_rgb = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2RGB)
    cv2.imwrite(f'{image_name.split("_")[0]}.png',im_rgb)
    shutil.move(f'{image_name.split("_")[0]}.png',f'{path}_concat')

df1 = pd.read_csv('lr_metadata.csv')
lr_count = df1.shape[0]
for i in range(lr_count):
    join_cropped_image('lr',df1.loc[i, 'height'] , df1.loc[i, 'width'],32)

df = pd.read_csv('hr_metadata.csv')
hr_count = df.shape[0]
for j in range(hr_count):
    join_cropped_image('hr',df.loc[j, 'height'],df.loc[j, 'width'],128)
    join_cropped_image('sr',df.loc[j, 'height'],df.loc[j, 'width'],128)

reformat_dirs('hr','lr','sr')
