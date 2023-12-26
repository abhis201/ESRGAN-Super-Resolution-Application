from django.shortcuts import render
from Backend.scripts.imresize import *
import os
import cv2
from skimage.io import imsave
from PIL import Image
from Backend.ESRGAN.model.ESRGAN import *
from torchvision.utils import save_image
import torchvision.transforms.functional as TF
from collections import OrderedDict
from Backend.scripts.calculate_PSNR_SSIM import *
import torch
from Backend.Bicubic.bicupscale import *
from Backend.SFTGAN.pytorch_test.test_sftgan import *
import socket


hr_path = ''
lr_path = ''
sr_esrgan_path = ''
sr_bicubic_path = ''
sr_sftgan_path = ''
srimgE = ''
srimgB = ''
srimgS = ''
indeximg=0
srres = 0
srimg = ''
srSimage_name = ''
srEimage_name = ''
srBimage_name = ''
lrpsnr = 0
lrssim = 0
sftpsnr = 0
sftssim = 0
bicpsnr = 0
bicssim = 0
esrpsnr = 0
esrssim = 0
msg= ''

def home(request):
    return render(request,'home.html')

def loadimg(request):
    global hr_path, lr_path,sr_esrgan_path,sr_bicubic_path,sr_sftgan_path,indeximg,srimgB,srimgE,srimgS,hrimg,srSimage_name,srEimage_name,srBimage_name,srres
    global lrpsnr,lrssim,sftpsnr,sftssim,bicpsnr,bicssim,esrpsnr,esrssim
    lr_path = str(request.GET['lrhid1'])
    hr_path = str(request.GET['hrhid1'])
    sr_esrgan_path = str(request.GET['srhid1'] + "sr_esrgan")
    sr_bicubic_path = str(request.GET['srhid1'] + "sr_bicubic")
    sr_sftgan_path = str(request.GET['srhid1'] + "sr_sftgan")

    current_working_directory = os.getcwd()
    print("Current Working Directory:", current_working_directory)
    lrdir = os.listdir(lr_path)
    hrdir = os.listdir(hr_path)
    srdir_esrgan = os.listdir(sr_esrgan_path)
    srdir_bicubic = os.listdir(sr_bicubic_path)
    srdir_sftgan = os.listdir(sr_sftgan_path)
    lrdir.sort()
    hrdir.sort()
    srdir_esrgan.sort()
    srdir_sftgan.sort()
    srdir_bicubic.sort()
    totimg = len(lrdir)

    for index, lrimage_name in enumerate(lrdir):
        break;
    lrimg = str("static/" + ("/".join(lr_path.split("/")[1:])) + "/" + lrimage_name)

    for index, hrimage_name in enumerate(hrdir):
        break;
    hrimg = str("static/" + ("/".join(hr_path.split("/")[1:])) + "/" + hrimage_name)

    if len(os.listdir(sr_esrgan_path)and(os.listdir(sr_sftgan_path))and(os.listdir(sr_bicubic_path))) > 0:
        srres = 1

    if srres==1:
        for index, srEimage_name in enumerate(srdir_esrgan):
            break;
        srimgE = str("static/" + ("/".join(sr_esrgan_path.split("/")[1:])) + "/" + srEimage_name)
        srEimage_name = srEimage_name


        for index, srBimage_name in enumerate(srdir_bicubic):
            break;
        srimgB = str("static/" + ("/".join(sr_bicubic_path.split("/")[1:])) + "/" + srBimage_name)
        srBimage_name = srBimage_name


        for index, srSimage_name in enumerate(srdir_sftgan):
            break;
        srimgS = str("static/" + ("/".join(sr_sftgan_path.split("/")[1:])) + "/" + srSimage_name)
        srSimage_name = srSimage_name

        lrpsnr = 0 #calpsnr(lrimg, lr_path)
        lrssim = 0 #calssim(lrimg, lr_path)
        sftpsnr = calpsnr(srSimage_name, sr_sftgan_path)
        sftssim = calssim(srSimage_name, sr_sftgan_path)
        bicpsnr = calpsnr(srBimage_name, sr_bicubic_path)
        bicssim = calssim(srBimage_name, sr_bicubic_path)
        esrpsnr = calpsnr(srEimage_name, sr_esrgan_path)
        esrssim = calssim(srEimage_name, sr_esrgan_path)


    indeximg = index
    lr_path = lr_path
    hr_path = hr_path
    sr_esrgan_path = sr_esrgan_path
    sr_bicubic_path = sr_bicubic_path
    sr_sftgan_path = sr_sftgan_path
    return render(request,'home.html',{'imglr':lrimg,'imghr':hrimg,'imgsrE':srimgE,'imgsrB':srimgB,'imgsrS':srimgS,'psnrlr':lrpsnr,'ssimlr':lrssim
        ,'psnrsft':sftpsnr,'psnrbic':bicpsnr,'psnresr':esrpsnr,'ssimsft':sftssim,'ssimbic':bicssim,'ssimesr':esrssim,'imgno':1,'totalimg':totimg})

def makelr(request):
    global hr_path, lr_path, indeximg
    hr_path = str(request.GET['hrhid'])
    lr_path = str(request.GET['lrhid'])

    def downscale(hrpath, lrpath):
        image_list = os.listdir(hrpath)

        for index, image_name in enumerate(image_list):
            img_uint8 = cv2.imread(os.path.join(hrpath, image_name))
            height, width, channels = img_uint8.shape
            new_height = height // 4
            new_width = width // 4
            new_size = (new_height, new_width)
            new_img_uint8 = imresize(img_uint8, output_shape=new_size)
            imsave(os.path.join(lrpath, image_name), new_img_uint8)
            im_bgr = cv2.imread(f'{lrpath}/{image_name}')
            im_rgb = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2RGB)
            cv2.imwrite(os.path.join(lrpath, image_name), im_rgb)
            print('saved image', image_name)

    downscale(hr_path,lr_path)
    lr_path = lr_path
    hr_path = hr_path
    return render(request,'home.html')

def previmg(request):
    global lrpsnr, lrssim, sftpsnr, sftssim, bicpsnr, bicssim, esrpsnr, esrssim
    global hr_path, lr_path,sr_esrgan_path,sr_bicubic_path,sr_sftgan_path,srres, indeximg,srimgB,srimgE,srimgS,lrimg,hrimg,srSimage_name,srEimage_name,srBimage_name
    lrdir = os.listdir(lr_path)
    hrdir = os.listdir(hr_path)

    lrdir.sort()
    hrdir.sort()
    count = len(lrdir)

    for indexprev, lrimage_name in enumerate(lrdir):
        if(indexprev == (indeximg-1)):
            break;
    lrimg = str("static/" + ("/".join(lr_path.split("/")[1:])) + "/" + lrimage_name)

    for indexprev, hrimage_name in enumerate(hrdir):
        if (indexprev == indeximg - 1):
            break;
    hrimg = str("static/" + ("/".join(hr_path.split("/")[1:])) + "/" + hrimage_name)

    if len(os.listdir(sr_esrgan_path)and(os.listdir(sr_sftgan_path))and(os.listdir(sr_bicubic_path))) > 0:
        srres = 1

    if srres==1:
        srdir_esrgan = os.listdir(sr_esrgan_path)
        srdir_esrgan.sort()
        for indexprev, srEimage_name in enumerate(srdir_esrgan):
            if (indexprev == indeximg - 1):
                break;
        srimgE = str("static/" + ("/".join(sr_esrgan_path.split("/")[1:])) + "/" + srEimage_name)


        srdir_bicubic = os.listdir(sr_bicubic_path)
        srdir_bicubic.sort()
        for indexprev, srBimage_name in enumerate(srdir_bicubic):
            if (indexprev == indeximg - 1):
                break;
        srimgB = str("static/" + ("/".join(sr_bicubic_path.split("/")[1:])) + "/" + srBimage_name)


        srdir_sftgan = os.listdir(sr_sftgan_path)
        srdir_sftgan.sort()
        for indexprev, srSimage_name in enumerate(srdir_sftgan):
            if (indexprev == indeximg - 1):
                break;
        srimgS = str("static/" + ("/".join(sr_sftgan_path.split("/")[1:])) + "/" + srSimage_name)

        lrpsnr = 0 #calpsnr(lrimg, lr_path)
        lrssim = 0 #calssim(lrimg, lr_path)
        sftpsnr = calpsnr(srSimage_name, sr_sftgan_path)
        sftssim = calssim(srSimage_name, sr_sftgan_path)
        bicpsnr = calpsnr(srBimage_name, sr_bicubic_path)
        bicssim = calssim(srBimage_name, sr_bicubic_path)
        esrpsnr = calpsnr(srEimage_name, sr_esrgan_path)
        esrssim = calssim(srEimage_name, sr_esrgan_path)

    indeximg = indexprev
    return render(request,'home.html',{'imglr':lrimg,'imghr':hrimg,'imgsrE':srimgE,'imgsrB':srimgB,'imgsrS':srimgS,'psnrlr':lrpsnr,'ssimlr':lrssim
        ,'psnrsft':sftpsnr,'psnrbic':bicpsnr,'psnresr':esrpsnr,'ssimsft':sftssim,'ssimbic':bicssim,'ssimesr':esrssim,'imgno':indeximg+1,'totalimg':count})



def nextimg(request):
    global lrpsnr, lrssim, sftpsnr, sftssim, bicpsnr, bicssim, esrpsnr, esrssim
    global hr_path, lr_path,sr_esrgan_path,sr_sftgan_path,sr_bicubic_path,srres, indeximg,srimgB,srimgE,srimgS,lrimg,hrimg,srSimage_name,srEimage_name,srBimage_name
    lrdir = os.listdir(lr_path)
    hrdir = os.listdir(hr_path)

    lrdir.sort()
    hrdir.sort()
    count = len(lrdir)

    for indexnext, lrimage_name in enumerate(lrdir):
        if (indexnext == (indeximg + 1)):
            break;
    lrimg = str("static/" + ("/".join(lr_path.split("/")[1:])) + "/" + lrimage_name)

    for indexnext, hrimage_name in enumerate(hrdir):
        if (indexnext == indeximg + 1):
            break;
    hrimg = str("static/" + ("/".join(hr_path.split("/")[1:])) + "/" + hrimage_name)

    if len(os.listdir(sr_esrgan_path)and(os.listdir(sr_sftgan_path))and(os.listdir(sr_bicubic_path))) > 0:
        srres = 1

    if srres==1:
        srdir_esrgan = os.listdir(sr_esrgan_path)
        srdir_esrgan.sort()
        for indexnext, srEimage_name in enumerate(srdir_esrgan):
            if (indexnext == indeximg + 1):
                break;
        srimgE = str("static/" + ("/".join(sr_esrgan_path.split("/")[1:])) + "/" + srEimage_name)


        srdir_bicubic = os.listdir(sr_bicubic_path)
        srdir_bicubic.sort()
        for indexnext, srBimage_name in enumerate(srdir_bicubic):
            if (indexnext == indeximg + 1):
                break;
        srimgB = str("static/" + ("/".join(sr_bicubic_path.split("/")[1:])) + "/" + srBimage_name)


        srdir_sftgan = os.listdir(sr_sftgan_path)
        srdir_sftgan.sort()
        for indexnext, srSimage_name in enumerate(srdir_sftgan):
            if (indexnext == indeximg + 1):
                break;
        srimgS = str("static/" + ("/".join(sr_sftgan_path.split("/")[1:])) + "/" + srSimage_name)

        lrpsnr = 0 #calpsnr(lrimg,lr_path)
        lrssim = 0 #calssim(lrimg,lr_path)
        sftpsnr = calpsnr(srSimage_name, sr_sftgan_path)
        sftssim = calssim(srSimage_name, sr_sftgan_path)
        bicpsnr = calpsnr(srBimage_name, sr_bicubic_path)
        bicssim = calssim(srBimage_name, sr_bicubic_path)
        esrpsnr = calpsnr(srEimage_name, sr_esrgan_path)
        esrssim = calssim(srEimage_name, sr_esrgan_path)

    indeximg = indexnext
    return render(request, 'home.html', {'imglr': lrimg, 'imghr': hrimg,'imgsrE':srimgE,'imgsrB':srimgB,'imgsrS':srimgS,'psnrlr':lrpsnr,'ssimlr':lrssim
        ,'psnrsft':sftpsnr,'psnrbic':bicpsnr,'psnresr':esrpsnr,'ssimsft':sftssim,'ssimbic':bicssim,'ssimesr':esrssim,'imgno':indeximg+1,'totalimg':count})

def applysr(request):
    global lr_path,srres,sr_esrgan_path,sr_sftgan_path,sr_bicubic_path,indeximg

    if len(os.listdir(sr_esrgan_path)and(os.listdir(sr_sftgan_path))and(os.listdir(sr_bicubic_path)))>0:
        srres=1
        print("SR images already present in folder")
        return render(request,'home.html')

    gan_pth_path='Backend/ESRGAN/parameters/gan.pth'
    psnr_pth_path='Backend/ESRGAN/parameters/psnr.pth'
    interp_pth_path='Backend/ESRGAN/parameters/interp.pth'
    lr_dir=lr_path
    sr_esrgan_dir=sr_esrgan_path
    alpha=0.8

    net_PSNR = torch.load(psnr_pth_path)
    net_ESRGAN = torch.load(gan_pth_path)
    net_interp = OrderedDict()

    for k, v_PSNR in net_PSNR.items():
        v_ESRGAN = net_ESRGAN[k]
        net_interp[k] = (1 - alpha) * v_PSNR + alpha * v_ESRGAN

    torch.save(net_interp, interp_pth_path)

    if not os.path.exists(lr_dir):
        raise Exception('[!] No lr path')
    if not os.path.exists(sr_esrgan_dir):
        os.makedirs(sr_esrgan_dir)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    with torch.no_grad():
        net = ESRGAN(3, 3, scale_factor=4)
        net.load_state_dict(net_interp)
        net = net.to(device).eval()

        for image_name in os.listdir(lr_dir):
            image = Image.open(os.path.join(lr_dir, image_name)).convert('RGB')
            image = TF.to_tensor(image).to(device).unsqueeze(dim=0)

            image = net(image)

            save_image(image, os.path.join(sr_esrgan_dir, image_name))
            print(f'upscaled {image_name}')

    #bicubic sr upscale

    bicupscale(lr_path,sr_bicubic_path)
    print('Bicubic Done!!')
    # sftgan sr upscale
    print(lr_path, sr_sftgan_path)
    print("Starting sftgan")
    segmentation(lr_path)
    srpath = sr_sftgan_path + "/"
    sftgan(srpath)
    print('SFTGAN Done!!!')

    return render(request, 'home.html')

def calpsnr(img1,path):
    global hrimg,hr_path
    img1 = cv2.imread(path+"/"+img1)
    img2 = cv2.imread(hr_path+hrimg.split("/")[-1])
    psnr=calculate_psnr(img1, img2)
    return(psnr)

def calssim(img1,path):
    global hrimg,hr_path
    img1 = cv2.imread(path+"/"+img1)
    img2 = cv2.imread(hr_path+hrimg.split("/")[-1])
    ssimvalue = ssim(img1, img2)
    return(ssimvalue)

def nextpage(request):
    global lrpsnr, lrssim, sftpsnr, sftssim, bicpsnr, bicssim, esrpsnr, esrssim
    global lr_path,sr_esrgan_path
    list = os.listdir(lr_path)
    list.sort()
    listsr = os.listdir(sr_esrgan_path)
    listsr.sort()
    count = len(list)
    srpath = sr_esrgan_path.replace("Backend","static")
    lrpath=lr_path.replace("Backend","static")
    sizesr = dirsize(sr_esrgan_path,'MB')
    sizelr = dirsize(lr_path,'MB')
    return render(request,'local.html',{'algorithm':"ESRGAN",'psnr':esrpsnr,'ssim':esrssim,'list':list,'count':count,
                                        'lrpath':lrpath,'srpath':srpath,'listsr':listsr,'sizelr':sizelr,'sizesr':sizesr})

def dirsize(dir,unit):
    HOME_FOLDER = dir
    key = unit
    directory_size = 0

    fsizedicr = {'B': 1, 'KB': float(1) / 1024, 'MB': float(1) / (1024 * 1024),
                 'GB': float(1) / (1024 * 1024 * 1024)}

    for (path, dirs, files) in os.walk(HOME_FOLDER):
        for file in files:
            filename = os.path.join(path, file)
            directory_size += os.path.getsize(filename)

    print("Folder Size: " + str(round(fsizedicr[key] * directory_size, 2)) + " " + key)
    return (str(round(fsizedicr[key] * directory_size, 2)) + " " + key)

def transfer(request):
    global lr_path,msg
    list = os.listdir(lr_path)
    list.sort()
    count = len(list)
    lrpath = lr_path.replace("Backend", "static")
    sizelr = dirsize(lr_path, 'MB')
    msg = msg
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)

    return render(request,"send.html",{'lrpath':lrpath,'list':list,'totimg':count,'size':sizelr,'ip':IPAddr,'msg':msg})

def stop(request):
    socket.socket().close()
    socket.socket.shutdown()
    return render(request,"send.html")

def clientrequest(request):
    s = socket.socket()
    s.connect(("localhost", 4000))
    msg = bytes('Ready to Connect','utf-8')
    s.send(msg)
    #l = s.recv(4096)
    i=1
    #while (l):
        #f = open("img_"+str(i)+".png",'wb')
        #i=i+1;
        #f.write(l)
        #f.close()
    return render(request,'receive.html')

def localclient(request):
    global msg
    port = request.GET['portno']
    ipadd = request.GET['ipaddr']
    user = request.GET['username']

    net_img = "Backend/socket/sr"
    list = os.listdir(net_img)
    list.sort()
    count = len(list)
    imgpath = net_img.replace("Backend", "static")
    size = dirsize(net_img, 'MB')

    return render(request,"receive.html",{'usr':user,'ipad':ipadd,'list':list,'path':imgpath,'totimg':count,'size':size})


def sendtoclient(request):
    global lr_path
    list = os.listdir(lr_path)
    list.sort()
    s = socket.socket()
    s.connect(("localhost", 4000))
    for index,image in enumerate(list):
        f = open(f"Backend/ESRGAN/datasets/TEST/lr/{image}", "rb")
        l = f.read()
        while (l):
            s.send(l)

def listenclient(request):
    global msg
    s = socket.socket()
    s.bind(("localhost", 4000))
    s.listen(10)  # Accepts up to 10 connections.

    while (s.accept()):
        sc, address = s.accept()

        print(address)
        l = sc.recv(4096)
        msg = l
        print(msg)
        sc.close()
        return transfer(request)
