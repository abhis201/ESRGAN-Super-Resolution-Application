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

## Project Structure (Reorganized)

```
ESRGAN-Super-Resolution-Application/
│
├── README.md
├── requirements.txt
├── build.sh
├── db.sqlite3
│
├── backend/
│   ├── bicubic/
│   │   ├── bicubic_upscale.py
│   │   ├── lr_images/
│   │   └── sr_images/
│   ├── esrgan/
│   │   ├── main.py
│   │   ├── test_main.py
│   │   ├── config/
│   │   ├── dataloader/
│   │   ├── datasets/
│   │   ├── image/
│   │   ├── loss/
│   │   ├── model/
│   │   ├── parameters/
│   │   ├── samples/
│   │   ├── src/
│   │   └── util/
│   ├── sftgan/
│   │   ├── README.md
│   │   ├── data/
│   │   ├── figures/
│   │   ├── pretrained_models/
│   │   └── pytorch_test/
│   ├── scripts/
│   │   ├── calculate_psnr_ssim.py
│   │   └── image_resize.py
│   └── css/
│       ├── send.css
│       └── style_new.css
│
├── webapp/
│   ├── manage.py
│   ├── db.sqlite3
│   ├── core/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── wsgi.py
│   └── templates/
│       ├── home.html
│       ├── local.html
│       ├── receive.html
│       └── send.html
```

## Overview

This project is an Image Super-Resolution application using ESRGAN and other algorithms to upscale low-resolution images up to 4x. It provides a web interface for image enhancement, comparison, and transfer.

### Tech Stack
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Backend:** Python (Django), Machine Learning (ESRGAN, Bicubic, SFTGAN)

### Main Components
- **backend/**: Contains all ML models, upscaling scripts, and supporting code.
  - `bicubic/`: Bicubic upscaling implementation and images.
  - `esrgan/`: ESRGAN model, training, and testing code.
  - `sftgan/`: SFTGAN model and resources.
  - `scripts/`: Utility scripts for PSNR/SSIM calculation and image resizing.
  - `css/`: Stylesheets for the web interface.
- **webapp/**: Django web application.
  - `core/`: Django project files (settings, views, URLs, etc.).
  - `templates/`: HTML templates for the web interface.

## Usage Instructions

### 1. Setup
1. Clone the repository and navigate to the project root.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Prepare datasets:
   ```bash
   python backend/esrgan/datasets/prepare_datasets.py
   ```

### 2. Training ESRGAN
1. Run the ESRGAN trainer:
   ```bash
   python backend/esrgan/main.py
   ```
   - This will train the ESRGAN model using images in the datasets folder.

### 3. Running the Web Application
1. Start the Django server:
   ```bash
   cd webapp
   python manage.py runserver
   ```
2. Access the web interface at `http://localhost:8000`.

### 4. Image Enhancement Workflow
1. On the homepage, follow the steps:
   - Click the green buttons in order to construct LR images.
   - Click 'Start' to run the super-resolution process.
   - View upscaled images and compare results (ESRGAN, Bicubic, etc.).
   - Check PSNR and SSIM values for quality assessment.

### 5. Saving and Transferring Images
- Save upscaled images locally or transfer them to another computer via sockets (see web interface for options).

## Screenshots

![Image Enhancing Utility](https://user-images.githubusercontent.com/31624329/195983153-023db0c1-8787-4e33-b75c-282c658fc538.png)
![SR img remote transfer](https://user-images.githubusercontent.com/31624329/195984075-db2e18e1-6f43-4e57-93da-6480ce7bdd4f.png)
![SR image receiver](https://user-images.githubusercontent.com/31624329/195984069-43d0c6c3-95bb-41e2-9bf2-a145f498d714.png)
![SR Img preview](https://user-images.githubusercontent.com/31624329/195984071-645912d9-acde-4d75-a1de-b562bcc187b9.png)

## Notes
- Ensure all required datasets are downloaded before training.
- For custom models or scripts, refer to the respective folders in `backend/`.
- For troubleshooting, check logs and error messages in the terminal.
