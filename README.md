# ESRGAN-Super-Resolution-Application

This is an Image SuperResolution project which can upscale low resolution images upto 4 times its resoltion.

TechStack
WebDev - CSS, Bootstrap, HTML, JS
Backend - Python, ML
Framwork - Django

Flow:
1. Download the datasets by running the prepare_datsets.py from the datasets folder
2. Once the images are downloaded from the cloud run the main.py in the root folder(ESRGAN-pytorch-master)
3. The main.py runs runs the trainer which trains the algorithm based on the images.
4. The trainer runs on the ESRGAN network present in the models folder.

UserInterface:

Image Enhancing Tool - this is the homepage of the application
![Image Enhancing Utility](https://user-images.githubusercontent.com/31624329/195983153-023db0c1-8787-4e33-b75c-282c658fc538.png)

Features of this page
(pre-requisites) - before clicking the start button. Ensure that you have clicked both the green buttons in order(i.e. 1st * then Construct LR)(this will be more optimized in the future and the application will do it automatically)
1. The start button runs the main.py in the backend so that the application generated the Super Resoluted image of the Low Resolution images present in the lr folder of the datasets folder
2. As soon as the SR process is completed you will be able to see many images upscaled based on different algorithms (ESRGAN is shown at the last). This is to show the results of the upscaling as well as compare it with other leading SR algorithms.
3. You will also see the values of Peak-Signal-to-Noise Ratio(PSNR) and SSIM(Structural Similarity Index compared to its original HR image) to be able to mathematically
determine the results;

Save Locally or Transfer to another pc
![SR img remote transfer](https://user-images.githubusercontent.com/31624329/195984075-db2e18e1-6f43-4e57-93da-6480ce7bdd4f.png)
![SR image receiver](https://user-images.githubusercontent.com/31624329/195984069-43d0c6c3-95bb-41e2-9bf2-a145f498d714.png)
![SR Img preview](https://user-images.githubusercontent.com/31624329/195984071-645912d9-acde-4d75-a1de-b562bcc187b9.png)

After the SR process is over the application provides features to either save the images locally to some predefined folder or transfer the images to another computer on the network via sockets.
