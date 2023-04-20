# Ecological Mapping Using Satellite Imagery

## Project Brief 

### Overview
The Earth's surface is continually changing and it is concerning how quickly such environmental issues are intensifying as a result of unsustainable patterns of consumption and production by humans. It is clear that we are in the midst of a global climate crisis, one that will only worsen if nothing is done to stop its effects. This report's goal is to offer a technology-driven recommendation that will help educate the public and the appropriate decision-makers on the effects of the climate disaster that human activity is causing.

Using Deep Convolutional Neural Network Models and Remote Sensing Change Detection techniques, we offer a method in this paper to measure changes in geographic features seen in high resolution multi-temporal satellite data. So far, we have experimented with various image segmentation models to obtain the most accurate results and predictions. Our deliverable model will take as input satellite imagery from publicly available sources and produce segmentation masks of geographical features present in these images, such as forest cover and water bodies. These segmentation masks will then be used by our Remote Sensing Change Detection algorithms to generate a percentage value showing how the particular feature has changed over time. We are optimistic that the deliverables of this project will contribute in the development of policies to tackle the problem by assisting policymakers in understanding the relationship between unsustainable human activities and environmental deterioration.

# Code Setup 

## Scripts
For the GPT_RSCD notebook, install the following libraries before use: openai, numpy, opencv

For the training model notebooks, install mmcv and mmsegmentation and run the programs. 

## Frontend 
Install angular
$npm install -g @angular/cli

Install Dependencies
$npm install --save ol @planet/client

Run the frontend
$ng serve --open

It runs on http://localhost:4200/

## Backend 
NOTE: Run the backend using conda
Activate the virtual env 'backendenv'
$conda activate backendenv
In case virtual env is not working create a new one and add following dependencies

create new env
$pip install virtualenv
$virtualenv <my_env_name>
$<my_env_name>/Scripts/activate

Install dependencies
$pip install django
$pip install planet
$pip install geojsonio
$pip install django-ninja
$python -m pip install django-cors-headers
$pip install numpy
$pip install pillow
$pip install boto3
$pip install matplotlib
$pip install --upgrade openai
$pip install opencv-python
$pip install torch==1.12.0 torchvision --extra-index-url https://download.pytorch.org/whl/cu113
$pip3 install mmcv-full==1.6.0 -f https://download.openmmlab.com/mmcv/dist/cpu/torch1.8.0/index.html
$pip install openmim
$!mim install mmcv-full==1.6.0

Run the backend server
$python manage.py runserver

Runs on http://localhost:8000/

## Loaders 
For the data loader APIs, install the following libraries: boto3, pillow, matplotlib, numpy, BytesIO, opencv
