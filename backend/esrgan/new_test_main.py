import torch
import os
import cv2
from PIL import Image
from backend.esrgan.model.ESRGAN import ESRGAN
from torchvision.utils import save_image
import torchvision.transforms.functional as TF
from collections import OrderedDict
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--gan_pth_path', default='parameters/gan.pth')
parser.add_argument('--psnr_pth_path', default='parameters/psnr.pth')
parser.add_argument('--interp_pth_path', default='parameters/interp.pth')
parser.add_argument('--lr_dir',default='datasets/lr')
parser.add_argument('--conv_lr',default='datasets/upscale_img')
parser.add_argument('--sr_dir',default='datasets/sr')
parser.add_argument('--alpha', type=int, default=0.8)

args = parser.parse_args()


net_PSNR = torch.load(args.psnr_pth_path)
net_ESRGAN = torch.load(args.gan_pth_path)
net_interp = OrderedDict()

for k, v_PSNR in net_PSNR.items():
    v_ESRGAN = net_ESRGAN[k]
    net_interp[k] = (1 - args.alpha) * v_PSNR + args.alpha * v_ESRGAN

torch.save(net_interp, args.interp_pth_path)

if not os.path.exists(args.lr_dir):
    raise Exception('[!] No lr path')
if not os.path.exists(args.sr_dir):
    os.makedirs(args.sr_dir)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

with torch.no_grad():
    net = ESRGAN(3, 3, scale_factor=4)
    net.load_state_dict(net_interp)
    net = net.to(device).eval()

    for image_name in os.listdir(args.conv_lr):
        image = Image.open(os.path.join(args.conv_lr, image_name)).convert('RGB')
        image = TF.to_tensor(image).to(device).unsqueeze(dim=0)

        image = net(image)

        save_image(image,  os.path.join(args.sr_dir, image_name))
        print(f'save {image_name}')
