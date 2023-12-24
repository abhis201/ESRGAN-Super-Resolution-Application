import os
import shutil
from preparation.utils import download_url, unzip_zip_file, unzip_tar_file
from glob import glob

print('[!] Reformat DIV2K HR')
image_path = glob('temp/DIV2K_train_HR/*.png')
image_path.sort()
for index, path in enumerate(image_path):
        shutil.move(path, os.path.join('hr', f'{index:04d}.png'))

print('[!] Reformat DIV2K LR')
image_path = glob('temp/DIV2K_train_LR_bicubic/X4/*.png')
image_path.sort()
for index, path in enumerate(image_path):
	shutil.move(path, os.path.join('lr', f'{index:04d}.png'))