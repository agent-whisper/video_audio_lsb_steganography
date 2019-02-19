import math
import os
import random
import shutil

import cv2
import numpy as np

def vigenere_encrypt(message, key) :
	return(message)

def video_to_image(path, temp_folder) :
	try :
		os.mkdir(temp_folder)
	except OSError:
		remove(temp_folder)
		os.mkdir(temp_folder)

	count = 0

	success = True

	vidcap = cv2.VideoCapture(path)
	info_image = {}
	info_image['width'] = int(vidcap.get(3))
	info_image['height'] = int(vidcap.get(4))
	info_image['fps'] = int(vidcap.get(5))
	info_image['fourcc'] = int(vidcap.get(6))
	while success:
		success,image = vidcap.read()
		if (success) :
			cv2.imwrite(os.path.join(temp_folder, "{:d}.png".format(count)), image)
			count += 1

	info_image['total_image'] = count	
	return(info_image)

def remove(path):
  if os.path.isfile(path):
      os.remove(path)
  elif os.path.isdir(path):
      shutil.rmtree(path)
  else:
      raise ValueError("file {} is not a file or dir.".format(path))

def generate_random_order_pixel(seed, need_pixel, need_frame, frame_sequencial, pixel_sequencial, pixel_range, frame_range, pixel_per_image) :
	random.seed(seed)
	pixel_order = np.array([])
	if ((not frame_sequencial) and (not pixel_sequencial)) :
		pixel_order = random.sample(range(pixel_range[0],pixel_range[1]), need_pixel)
	if (pixel_sequencial and frame_sequencial) :
		pixel_order = list(range (0, need_pixel))
	if (pixel_sequencial and (not frame_sequencial)) :
		frame_order = random.sample(range(frame_range[0],frame_range[1]), need_frame)
		for frame_idx in frame_order :
			pixel_in_frame = list(range (frame_idx * pixel_per_image, (frame_idx+1) * pixel_per_image))
			pixel_order = np.append(pixel_order, pixel_in_frame)
		pixel_order = pixel_order[:need_pixel]
	if (not(pixel_sequencial) and frame_sequencial) :
		frame_order = list(range (0,need_frame))
		for frame_idx in frame_order :
			# print(frame_idx)
			pixel_in_frame = random.sample(range(frame_idx * pixel_per_image, (frame_idx+1) * pixel_per_image), pixel_per_image)
			pixel_order = np.append(pixel_order, pixel_in_frame)
		pixel_order = pixel_order[:need_pixel]
	return (pixel_order)