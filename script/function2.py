import shutil
import cv2
import os
from PIL import Image

def extract_config(image_index) :
	temp_folder = 'temp'
	image = cv2.imread(temp_folder + "/" + str(image_index) + ".png", 1 )
	int_lsb = image[0,0]
	byte_lsb = ['{0:08b}'.format(x) for x in int_lsb]
	frame_sequencial = ((byte_lsb[0])[-3] == '1')
	pixel_sequencial = ((byte_lsb[1])[-3] == '1')
	return(frame_sequencial, pixel_sequencial)

def save_config(image_index, frame_sequencial, pixel_sequencial) :
	temp_folder = 'temp'
	image = cv2.imread(temp_folder + "/" + str(image_index) + ".png", 1 )
	int_lsb = image[0,0]
	byte_lsb = ['{0:08b}'.format(x) for x in int_lsb]
	
	third_byte = byte_lsb[0][-2:]
	byte_lsb[0] = byte_lsb[0][:-3]
	if (frame_sequencial) :
		byte_lsb[0] = byte_lsb[0] + '1' + third_byte
	else :
		byte_lsb[0] = byte_lsb[0] + '0' + third_byte
	third_byte = byte_lsb[1][-2:]
	byte_lsb[1] = byte_lsb[1][:-3]
	if (pixel_sequencial) :
		byte_lsb[1] = byte_lsb[1] + '1' + third_byte
	else :
		byte_lsb[1] = byte_lsb[1] + '0' + third_byte
	int_lsb = tuple([int(x, 2) for x in byte_lsb])

	
	image[0,0] = int_lsb
	cv2.imwrite(temp_folder + "/" + str(image_index) + ".png",image)


def change_lsb(image_index, height_img, width_img, byte_message, byte_per_pixel, lsm_byte) :
	temp_folder = 'temp'
	image = cv2.imread(temp_folder + "/" + str(image_index) + ".png", 1 )
	int_lsb = image[height_img, width_img]

	byte_lsb = ['{0:08b}'.format(x) for x in int_lsb]
	for byte in range (0, byte_per_pixel) :
		byte_lsb[byte] = (byte_lsb[byte])[:-1*(lsm_byte)]
		byte_lsb[byte] = byte_lsb[byte] + byte_message[:lsm_byte]
		byte_message = byte_message[lsm_byte:]
	int_lsb = tuple([int(x, 2) for x in byte_lsb])
	
	image[height_img, width_img] = int_lsb
	cv2.imwrite(temp_folder + "/" + str(image_index) + ".png",image)

def steganography(info_image, pixel_order, byte_message, byte_per_pixel, lsm_byte) :
	for message_idx in range (0, len(byte_message),lsm_byte*byte_per_pixel) :
		# print(message_idx)
		message = ''
		byte_idx = pixel_order[int(message_idx/(lsm_byte*byte_per_pixel))]
		for idx in range (message_idx, message_idx+(lsm_byte*byte_per_pixel)) :
			if (idx < len(byte_message)) :
				message = message + str(byte_message[idx])
			else :
				message = message + str('0')
		
		pixel_each_img = info_image['width']*info_image['height']
		img_idx = byte_idx // pixel_each_img
		height_img = (byte_idx % pixel_each_img) // (info_image['width'])
		width_img = (byte_idx % pixel_each_img) % (info_image['width'])
		img_idx = int(img_idx)
		height_img = int(height_img)
		width_img = int(width_img)
		change_lsb(img_idx, height_img, width_img, message, byte_per_pixel, lsm_byte)

def extract_lsb(image_index, height_img, width_img, byte_per_pixel, lsm_byte) :
	temp_folder = 'temp'
	image = cv2.imread(temp_folder + "/" + str(int(image_index)) + ".png", 1 )
	int_lsb = image[int(height_img), int(width_img)]
	message = ''
	byte_lsb = ['{0:08b}'.format(x) for x in int_lsb]
	for byte in range (0, byte_per_pixel) :
		message += (byte_lsb[byte])[-1*(lsm_byte):]
	return(message)

def get_extension_len_message(info_image, pixel_order, byte_per_pixel, lsm_byte) :
	message = ''
	is_len = True
	is_extension = False
	extension = ''
	len_message = 0
	xi = 1
	len_total_message = 0
	for message_idx in range (0, len(pixel_order)*lsm_byte*byte_per_pixel,lsm_byte*byte_per_pixel) :
		byte_idx = pixel_order[int(message_idx/(lsm_byte*byte_per_pixel))]		
		pixel_each_img = info_image['width']*info_image['height']
		img_idx = byte_idx // pixel_each_img
		height_img = (byte_idx % pixel_each_img) // (info_image['width'])
		width_img = (byte_idx % pixel_each_img) % (info_image['width'])
		message = message + extract_lsb(img_idx, height_img, width_img, byte_per_pixel, lsm_byte)
		
		if (len(message) // 8 == xi) :
			xi += 1
			plain = ''
			for i in range (0,len(message) // 8) :
				a = message[i*8:i*8 + 8]
				x = int(a, 2)
				plain = plain + chr(x)
			if (plain[-1] == '|') :
				if (is_extension) :
					extension = plain[y:-1]
					y = len(plain)
					is_extension = False
					len_total_message = len(plain) * 8 + len_message
				if (is_len) :
					len_message = int(plain[:-1])
					y = len(plain)
					is_len = False
					is_extension = True
		if (not(is_extension) and not(is_len)) :
			range_message = (y*8, (y*8)+len_message)
			break
	return(len_message, len_total_message, extension, range_message)

def steganoanalytic(info_image, pixel_order, byte_per_pixel, lsm_byte, range_message) :
	message = ''
	is_message = False
	is_len = True
	is_extension = False
	extension = ''
	len_message = 0
	x = 1
	for message_idx in range (0, len(pixel_order)*lsm_byte*byte_per_pixel,lsm_byte*byte_per_pixel) :
		byte_idx = pixel_order[int(message_idx/(lsm_byte*byte_per_pixel))]		
		pixel_each_img = info_image['width']*info_image['height']
		img_idx = byte_idx // pixel_each_img
		height_img = (byte_idx % pixel_each_img) // (info_image['width'])
		width_img = (byte_idx % pixel_each_img) % (info_image['width'])
		message = message + extract_lsb(img_idx, height_img, width_img, byte_per_pixel, lsm_byte)

	return(message[range_message[0]:range_message[1]])

def vigenere_encrypt(message, key) :
	return(message)

def remove(path):
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)
    else:
        raise ValueError("file {} is not a file or dir.".format(path))

def video_to_image(path) :
	temp_folder = 'temp'
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

import random
import math
import numpy as np

def generate_random(seed, need_pixel, need_frame, frame_sequencial, pixel_sequencial, pixel_range, frame_range, pixel_per_image) :
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