import base64
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import json
import requests
import sys
# import geojsonio
import time
import mmsegmentation.mmseg
from mmsegmentation.mmseg.apis import inference_segmentor, init_segmentor, show_result_pyplot
from mmsegmentation.mmseg.core.evaluation import get_palette
import torch, torchvision
import os
import boto3
from io import BytesIO
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import mmcv
import matplotlib.image as mpimg
import openai
import cv2
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import zipfile



# private variables

# variables for bucket client
s3 = boto3.client('s3',
                  aws_access_key_id='AKIAX6WZFGHPXA6ZBNII',
                  aws_secret_access_key='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')

# variable setting the bucket to be accessed
bucket_name = 'open-sentinnel-map-images'

# variable to authorise openAI API
openai.api_key = "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"

# variable setting the class labels for rscd
class_labels = {
            "unknown": np.array([0, 0, 0]),
            "Bareland": np.array([128, 0, 0]),
            "Grass": np.array([0, 255, 36]),
            "Pavement": np.array([148, 148, 148]),
            "Road": np.array([255, 255, 255]),
            "Tree": np.array([34, 97, 38]),
            "Water": np.array([0, 69, 255]),
            "Cropland": np.array([75, 181, 73]),
            "buildings": np.array([222, 31, 7]),
        }

disaster_dict = { "33.0,-116.0": "Socal Fire, South California", "38.46914,-122.731547" : "Santa Rosa Wildfire, Santa Rosa California", "-0.834806,119.889349" : "Palu Tsunami, Palu Indonesia", "46.18715,-90.670364" : "Midwest floods, Midwestern USA", 
					"18.87477,-101.44576" : "Mexico Earthquake, Michoacan Mexico", "28.034882,-80.860251" : "Hurricane Micheal, Florida USA", "19.810257,-73.158462" : "Hurricane Matthew, Haiti", "29.912784,-92.314043" : "Hurricane Harvey, Louisiana USA",
					"34.925975,-76.997224" : "Hurricane Florence, North Carolina", "14.474586,-90.880957" : "Guatemala Volcano, Guatemala" }
# setup function to setup the bucket for image retrieval
#returns the pre and post disaster images of selected region
def setupBucket():
	#This is for retrieving label (masked) images of Open Sentinnel Map Dataset
	paginator = s3.get_paginator('list_objects_v2')
	#change directory name to xBDtargets/ to get the black images
	directory_name = 'xBDimages/'
	# set initial parameters for pagination
	paginator = s3.get_paginator('list_objects')
	page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=directory_name)
	file_list = []
	for page in page_iterator:
		if 'Contents' in page:
			for obj in page['Contents']:
				file_list.append(obj)
	return file_list


# A function to retrieve images of key disaster areas, pre- and post- disaster from bucket
# returns the coordinates and disaster names. Set in dictionary for the demo
# params: coordinates selected on the frontend
def pre_post_disaster_img(cordX, cordY):
	file_list = setupBucket()
	coord = str(cordX) + "," + str(cordY)
	# A dictionary of Key-Disaster areas to be used for demo
	dict = {
		"14.474586,-90.880957" : "guatemala-volcano", # Guatamela
		"34.925975,-76.997224" : "hurricane-florence", # North Carolina, USA
		"29.912784,-92.314043" : "hurricane-harvey_00000000", # Louisiana, USA
		"19.810257,-73.158462" : "hurricane-matthew", # Haiti
		"18.87477,-101.44576" : "mexico-earthquake", # Michoacan Mexico
		"28.034882,-80.860251" : "hurricane-michael", # Florida, USA
		"46.18715,-90.670364" : "midwest-flooding", # Midwestern, USA
		"-0.834806,119.889349" : "palu-tsunami", # Palu, Indonesia
		"38.46914,-122.731547" : "santa-rosa-wildfire", # Santa Rosa California, USA
		"33.0,-116.0" : "socal-fire", # South California, USA
	}

	for k,v in dict.items():		
		if coord == k:
			count = 0
			for file in file_list:
				if v in file['Key']: 
					print(v)          
					image_object = s3.get_object(Bucket=bucket_name, Key=file['Key'])
					image_content = image_object['Body'].read()
					image = Image.open(BytesIO(image_content))
					image.save("outputBucket/" + file['Key'][10:])
					count += 1
					if count == 2:
						return k


# Segmentation Model
# returns changes thorugh rscd of segmented images
# params: path of the folder to accesss images to be segmented - depending on upload or disaster display
def segmentationModel():
	config_file = './mmsegmentation/configs/deeplabv3plus/YashConfig.py'
	checkpoint_file = './mmsegmentation/iter_64000.pth'
	classes = ['unknown', 'Bareland', 'Grass', 'Pavement', 'Road', 'Tree', 'Water', 'Cropland', 'buildings']
	palette = [[0, 0, 0], [128, 0, 0], [0, 255, 36], [148, 148, 148], [255, 255, 255], [34, 97, 38], [0, 69, 255], [75, 181, 73], [222, 31, 7]]
	# build the model from a config file and a checkpoint file
	model = init_segmentor(config_file, checkpoint_file, device='cuda')
	image_list = os.listdir("outputBucket/") 
	ctr=0
	for i in image_list:
		img = "outputBucket/" + i
		result = inference_segmentor(model, img)[0]
		seg_img = Image.fromarray(result.astype(np.uint8)).convert('P')
		seg_img.putpalette(np.array(palette, dtype=np.uint8))
		seg_img_np = np.array(seg_img.convert('RGB'))
		if (ctr==0):
			after_img = seg_img_np
			seg_img.save(f"segmentedImages/after.png")	
			ctr += 1
		else:
			before_img = seg_img_np
			seg_img.save(f"segmentedImages/before.png")
	changes = ''
	changes = RSCDmodel(before_img, after_img)
	return changes

# This function calculates the change b/w inital and final image
# returns the feature, the inital area, the final area and the area change calculated
# params: the feature, the inital area, the final area, the inital image, the final image, the color
def compare_images(initial_image, final_image, color, feature, initial_area, final_area):
    initial_image = cv2.convertScaleAbs(initial_image)
    final_image = cv2.convertScaleAbs(final_image)
    # Resize the images to the same size
    initial_image = cv2.resize(initial_image, (final_image.shape[1], final_image.shape[0]))

    # Convert images to grayscale
    initial_gray = cv2.cvtColor(initial_image, cv2.COLOR_BGR2GRAY)
    final_gray = cv2.cvtColor(final_image, cv2.COLOR_BGR2GRAY)

    # Calculate the absolute difference between the two images
    diff = cv2.absdiff(initial_gray, final_gray)

    # Create a binary mask for pixels of the desired color
    color_mask = np.all(final_image == color, axis=-1)

    # Threshold the difference image to find pixels of the desired color
    _, color_mask = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    color_mask = cv2.bitwise_and(color_mask, color_mask, mask=np.uint8(color_mask))

    # Find contours of pixels of the desired color
    contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    area_change = ((final_area - initial_area)/initial_area)*100
    return feature, initial_area, final_area, area_change

# this function uses OpenAI API to generate GPT response
# Return the first choice's text
# params: the user text request
def generate_gpt3_response(user_text, print_output=False):
    completions = openai.Completion.create(
        engine='text-davinci-003',  # Determines the quality, speed, and cost.
        temperature=0.5,            # Level of creativity in the response
        prompt=user_text,           # What the user typed in
        max_tokens=500,             # Maximum tokens in the prompt AND response
        n=1,                        # The number of completions to generate
        stop=None,                  # An optional setting to control response generation
    )
    return completions.choices[0].text

def gpt_map(coordinates):
	for k,v in disaster_dict.items():
		if k==coordinates:
			disaster = v
	user_text = f"For the natural disaster '{disaster} that occured in the coordinates '{coordinates}', describe the environmental and geographical conditions pre and post disaster."
	res1 = generate_gpt3_response(user_text, print_output=False)
	return res1

def gpt_both(changes):
  user_text = f"I am providing this python dictionary: {changes}, where the key is the geographical feature and the value is the initial area, final area, and percentage in square meters in order. Describe the dictionary in a paragraph format to describe the value (area changes) for each key (geographical feature). Do not provide the text in a way that it is obvious you are describing a python dictionary. After that, given the data in the dictionary of the area change of each geographical feature in the region, give recommendations on the measures that should be taken in this region to conserve the environment."
  res2 = generate_gpt3_response(user_text, print_output=False)
  return res2

def gpt_agriculture(coordinates, changes):
  for k,v in disaster_dict.items():
    if k==coordinates:
      disaster = v
  user_text = f"Suggest how more agriculture or green farming can be promoted in {coordinates}, provided information in this python dictionary: {changes}, where the key is the geographical feature and the value is the initial area, final area, and percentage in square meters in order for the region: {coordinates}."
  res1 = generate_gpt3_response(user_text, print_output=False)
  return res1

def gpt_urban_planning(coordinates, changes):
  for k,v in disaster_dict.items():
    if k==coordinates:
      disaster = v
  user_text = f"Curate recommendations for urban planning in {coordinates}, provided information in this python dictionary: {changes}, where the key is the geographical feature and the value is the initial area, final area, and percentage in square meters in order for the region: {coordinates}."
  res1 = generate_gpt3_response(user_text, print_output=False)
  return res1

def gpt_env_conservation(coordinates, changes):
  for k,v in disaster_dict.items():
    if k==coordinates:
      disaster = v
  user_text = f"Suggest environmental conservation policies that can be implement in {coordinates}, provided this python dictionary: {changes}, where the key is the geographical feature and the value is the initial area, final area, and percentage in square meters in order for the region: {coordinates}."
  res1 = generate_gpt3_response(user_text, print_output=False)
  return res1

def gpt_disaster_management(coordinates, changes):
  for k,v in disaster_dict.items():
    if k==coordinates:
      disaster = v
  user_text = f"Give pointwise disaster management measures for {disaster} in {coordinates}, provided this python dictionary: {changes}, where the key is the geographical feature and the value is the initial area, final area, and percentage in square meters in order for {disaster} in {coordinates}. "
  res1 = generate_gpt3_response(user_text, print_output=False)
  return res1

# this function returns the unique colours of the image
# params: the image
def get_unique_colors(img):
    img = np.asarray(img)
    # Calculate the unique colors in the image
    unique_colors = np.unique(img.reshape(-1, img.shape[-1]), axis=0)
    before_colors = {}

    for color in unique_colors:
        for key, value in class_labels.items():
            if (color[0] <= value[0]+40 and color[0] >= value[0]-40 and color[1] <= value[1]+40 and color[1] >= value[1]-40 and color[2] <= value[2]+40 and color[2] >= value[2]-40).all():
                # Create a binary mask for the current color
                mask = np.where(np.all(img == color, axis=-1), 1, 0)

                # Calculate the area of the mask
                area = np.sum(mask)

                # Apply the binary mask to the input image
                masked_img = img * mask[..., np.newaxis]
                before_colors[key]=[masked_img,area]
    return before_colors

# The RSCD Model
# Retruns the changes, which is a key-value variable of features and related intial area, final area and area change
# params: the before and after images
def RSCDmodel(before, after):
	before_colors = get_unique_colors(before)
	after_colors = get_unique_colors(after)
	overlays = {}
	for k1, v1 in before_colors.items():
		for k2, v2 in after_colors.items():
			if k1 == k2:
				img1 = before_colors[k1][0]
				img2 = after_colors[k1][0]
				img1 = cv2.convertScaleAbs(img1)
				img2 = cv2.convertScaleAbs(img2)
				img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
				img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

				# Resize the images to the same size
				img1 = cv2.resize(img1, (img2.shape[1], img2.shape[0]))

				# Subtract one array from the other
				diff1 = img1.astype(np.int16) - img2.astype(np.int16)
				diff2 = img2.astype(np.int16) - img1.astype(np.int16)

				# Create binary masks for the lighter pixels
				mask1 = np.zeros_like(diff1)
				mask2 = np.zeros_like(diff2)
				_, mask1_thresh = cv2.threshold(diff1, 20, 255, cv2.THRESH_BINARY)
				mask1[mask1_thresh == 255] = 255
				_, mask2_thresh = cv2.threshold(diff2, 20, 255, cv2.THRESH_BINARY)
				mask2[mask2_thresh == 255] = 255

				# Create a 3-channel RGB image
				result = np.zeros((diff1.shape[0], diff1.shape[1], 3), dtype=np.uint8)
				# Set the red and green channels to the binary masks
				result[mask1 == 255, 0] = 255
				result[mask2 == 255, 1] = 255
				
				overlays[k1] = result
	
	before_img_true = ''
	for file in os.listdir("./outputBucket/"):
		if "pre" in file:
			before_img_true = "./outputBucket/" + file
		elif "before" in file:
			before_img_true = "./outputBucket/" + file
	for k,v in overlays.items():
		image = np.array(mpimg.imread(before_img_true))
		result = overlays[k]
		image *= 255
		image = image.astype(np.uint8)
		output = cv2.resize(image, (result.shape[1], result.shape[0]))
		tasnia = cv2.bitwise_or(output, result)
		result = Image.fromarray(tasnia)
		result.save(f"finalOutput/{k}.png")
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	changes = {}
	for k1, v1 in before_colors.items():
		for k2, v2 in after_colors.items():
			if k1 == k2:
				initial_image = before_colors[k1][0]
				final_image = after_colors[k1][0]
				color = class_labels[k1]
				feature, initial_area, final_area, area_change = compare_images(initial_image, final_image, color, k1, before_colors[k1][1], after_colors[k1][1])
				changes[feature] = [round(initial_area,2)*0.25, round(final_area,2)*0.25, area_change]
	return changes

# A function to delete all files in specified folder
# params: folder path
def deleteFiles(path):
	for file in os.listdir(path):
		file_path = os.path.join(path, file)
		try:
			if os.path.isfile(file_path):
				os.remove(file_path)
		except Exception as e:
			print(f"Failed to delete file {file_path}: {e}")

# a function to apend all image files in a folder into a json obj
# params: path of oflder with images
def getFiles(path):
	image_paths = []
	images = []
	i=0
	for img in os.listdir(path):
		image_paths.append(path + img)
	for img in image_paths:
		with open(img, 'rb') as f:
			image_data = f.read()
			encoded_data = base64.b64encode(image_data).decode('utf-8')
			
			images.append({
				'id': str(i),
				"name": os.path.basename(img),
				'data': 'data:image/jpeg;base64,' + encoded_data
			})
			i = i+1
	return images

# the main function which carries out the function calls for the Map feature from the frontend
def main(x,y):
	# clear all folders
	deleteFiles("outputBucket/")
	deleteFiles("finalOutput/")
	deleteFiles("segmentedImages/")
	torch.cuda.empty_cache()
	
	
	# retrive images and disaster name
	coords = pre_post_disaster_img(x,y) # retrieve imgs from bucket

	# check if disaster image or planetImg
	# if coords == 0:
	# 	#planetMain()		
	# 	return JsonResponse(coords) #temp
	
	changes = segmentationModel()
	del changes['unknown']
	res1 = gpt_map(coords)
	res2 = gpt_both(changes)
	res3 = gpt_agriculture(coords,changes)
	res4 = gpt_disaster_management(coords,changes)
	res5 = gpt_env_conservation(coords,changes)
	res6 = gpt_urban_planning(coords,changes)
	
	
	# Retrieve images from all relevant folders
	RSCDimages = getFiles("finalOutput/")
	MLimages = getFiles("segmentedImages/")
	OGimages = getFiles("outputBucket/")

	resp = [] # response array which contains json objs of all relevant data
	resp.append({
		"gpt_pre_post": res1,
		"gpt_rec": res2,
		"gpt_agri": res3,
		"gpt_dis": res4,
		"gpt_con" : res5,
		"gpt_urb":res6,
		"rscd" : RSCDimages,
		"ml" : MLimages,
		"og": OGimages
	})
	return JsonResponse(resp, safe=False)

# a function which saves the file in directory uploadedImages/
# return boolean value to signify process completed
# params: file to be saved
def saveUploadedFile(file):
	with open('outputBucket/' + file.name,'wb+') as destination:
		for chunk in file.chunks():
			destination.write(chunk)
	return True

# Main function which carries out the function calls for the upload functionality from frontend
# returns a response if completed
# params: an array of files to be uploaded
def upload(files):
	# remove all existing files
	deleteFiles("finalOutput/")
	deleteFiles("segmentedImages/")
	deleteFiles("outputBucket/")

	# save uploaded files
	torch.cuda.empty_cache()
	for file in files:
		saved = saveUploadedFile(file)
		if (saved == False):
			return HttpResponse("Failed to Upload Image")
	return HttpResponse("uploaded")
		
		
# returns a json response of segmented images, rscd images and gpt response
def returnUploaded():
	torch.cuda.empty_cache()
	changes = segmentationModel()
	res = gpt_both(changes)

	# Retrieve images from all relevant folders
	RSCDimages = getFiles("finalOutput/")
	MLimages = getFiles("segmentedImages/")
	OGimages = getFiles("outputBucket/")

	resp = [] # response array which contains json objs of all relevant data
	resp.append({
		"gpt_res": res,
		"rscd" : RSCDimages,
		"ml" : MLimages,
		'og' : OGimages
	})
	return JsonResponse(resp, safe=False)