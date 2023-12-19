'''
Codes for testing SFTGAN
'''

import os
import glob
import numpy as np
import cv2
import torch
from Backend.SFTGAN.pytorch_test import util
from Backend.SFTGAN.pytorch_test import architectures as arch

# options
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
model_path = 'Backend/SFTGAN/pretrained_models/SFTGAN_torch.pth'  # torch version
# model_path = 'Backend/SFTGAN/pretrained_models/SFTGAN_noBN_OST_bg.pth'  # pytorch version

test_img_folder_name = 'lr'  # image folder name
device = torch.device('cuda')  # if you want to run on CPU, change 'cuda' -> 'cpu'
# device = torch.device('cpu')

def sftgan(pathsr):
	test_img_folder = '/home/abhishek/Documents/SRwebapp/Backend/ESRGAN/datasets/TEST/' + test_img_folder_name # HR images
	test_prob_path = 'Backend/SFTGAN/data/' + test_img_folder_name + '_segprob'  # probability maps
	save_result_path = pathsr
	#util.mkdirs([save_result_path])

	if 'torch' in model_path:  # torch version
		model = arch.SFT_Net_torch()
	else:  # pytorch version
		model = arch.SFT_Net()
	model.load_state_dict(torch.load(model_path), strict=True)
	model.eval()
	model = model.to(device)

	print('Testing SFTGAN Backend/SFTGAN.')

	for idx, path in enumerate(glob.glob(test_img_folder+"/*")):
		imgname = os.path.basename(path)
		basename = os.path.splitext(imgname)[0]
		print(idx + 1, basename)
		# read image
		img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
		img = util.modcrop(img, 8)
		img = img * 1.0 / 255
		if img.ndim == 2:
		    img = np.expand_dims(img, axis=2)
		img = torch.from_numpy(np.transpose(img[:, :, [2, 1, 0]], (2, 0, 1))).float()
		# MATLAB imresize
		# You can use the MATLAB to generate LR images first for faster imresize operation
		img_LR = util.imresize(img, 1 / 4, antialiasing=True)
		img_LR = img_LR.unsqueeze(0)
		img_LR = img_LR.to(device)

		# read segmentation probability maps
		seg = torch.load(os.path.join(test_prob_path, basename + '_bic.pth'))
		seg = seg.unsqueeze(0)
		# change probability
		# seg.fill_(0)
		# seg[:,5].fill_(1)
		seg = seg.to(device)
		with torch.no_grad():
		    output = model((img_LR, seg)).data.float().cpu().squeeze()
		output = util.tensor2img(output)
		util.save_img(output, os.path.join(save_result_path, basename + '.png'))
