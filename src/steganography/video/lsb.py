import shutil
import cv2
import math
import os
from subprocess import call,STDOUT

import numpy as np
import src.steganography.video.utilities as utils

BYTE_PER_PIXEL = 3
HIDE_TEMP_FOLDER = 'steganography_temp'
HIDE_OUTPUT_FOLDER = 'steganography_output'
EXTRACT_TEMP_FOLDER = 'steganoanalysis_temp'
EXTRACT_OUTPUT_FOLDER = 'steganoanalysis_output'

def hide_secret(cover_video_dir, secret_msg_dir, key, output_file_name, lsm_byte, is_seq_frame=True, is_seq_pixel=True):
  # Load the cover video
  info_image = utils.video_to_image(cover_video_dir, HIDE_TEMP_FOLDER)

  # Read the extension of secret message
  message_extension = ''
  for character_idx in range (len(secret_msg_dir)-1, -1, -1) :
    if (secret_msg_dir[character_idx] == '.') :
      break
    message_extension = secret_msg_dir[character_idx] + message_extension
  # Load the secret message
  ord_bytes = []
  message = ''
  with open(secret_msg_dir, "rb") as input:
    while True :
      word = input.read(1)
      if (word == b'') :
        break
      ord_bytes.append(word)
      message = message + chr(ord(word))
  message_in_bytes = ''.join('{0:08b}'.format(ord(x)) for x in ord_bytes)

  len_message = len(message_in_bytes)
  extra_message = str(len_message) + '|' + message_extension + '|'
  # print(extra_message)
  extra_message = ''.join('{0:08b}'.format(ord(x)) for x in extra_message)

  message_in_bytes = extra_message + message_in_bytes

  # Generate seed from key
  seed_from_key = generate_seed(key)

  # Configuration setting
  image_index = 0
  save_config(image_index, is_seq_frame, is_seq_pixel, lsm_byte, HIDE_TEMP_FOLDER)

  # Message size validation
  max_information_per_image = info_image['width'] * info_image['height'] * BYTE_PER_PIXEL * lsm_byte
  is_msg_too_long = (max_information_per_image * info_image['total_image']) < len(message_in_bytes)
  if (is_msg_too_long) :
    print('message too long')
    return {'result': 'failed'}
  
  # Checking execution requirements
  required_pixel_count = math.ceil(len(message_in_bytes) / (BYTE_PER_PIXEL * lsm_byte))
  required_frame_count = math.ceil(required_pixel_count / (info_image['width'] * info_image['height']))
  required_pixel_count = int(required_pixel_count)
  required_frame_count = int(required_frame_count)
  pixel_range = (0, info_image['width']*info_image['height']*info_image['total_image'])
  frame_range = (0, info_image['total_image'])
  pixel_per_image = info_image['width'] * info_image['height']
  
  pixel_order = utils.generate_random_order_pixel(
    seed_from_key,
    required_pixel_count,
    required_frame_count,
    is_seq_frame,
    is_seq_pixel,
    pixel_range,
    frame_range,
    pixel_per_image
  )

  # Start steganography process
  apply_steganography(info_image, pixel_order, message_in_bytes, BYTE_PER_PIXEL, lsm_byte, HIDE_TEMP_FOLDER)
  try :
    os.mkdir(HIDE_OUTPUT_FOLDER)
  except OSError:
    utils.remove(HIDE_OUTPUT_FOLDER)
    os.mkdir(HIDE_OUTPUT_FOLDER)
  call(["ffmpeg", "-i", "{}/%d.png".format(HIDE_TEMP_FOLDER) , "-r", str(info_image['fps']), "-vcodec", "png", "{}/{}".format(HIDE_OUTPUT_FOLDER, output_file_name), "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)
  utils.remove(HIDE_TEMP_FOLDER)

  output_result = {
    'result': 'success',
    'output_dir': '{}/{}/{}'.format(os.getcwd(), HIDE_OUTPUT_FOLDER, output_file_name)
  }
  return output_result

def extract_secret(stegano_video_dir, key, output_file_name):
  info_image = utils.video_to_image(stegano_video_dir, EXTRACT_TEMP_FOLDER)
  image_index = 0
  is_seq_frame, is_seq_pixel, lsm_byte = extract_config(image_index, EXTRACT_TEMP_FOLDER)
  seed_from_key = generate_seed(key)

  need_pixel = 240
  need_frame = math.ceil(need_pixel / (info_image['width'] * info_image['height']))
  pixel_range = (0, info_image['width']*info_image['height']*info_image['total_image'])
  frame_range = (0, info_image['total_image'])
  pixel_per_image = info_image['width'] * info_image['height']
  need_pixel = int(need_pixel)
  need_frame = int(need_frame)
  pixel_order = utils.generate_random_order_pixel(seed_from_key, need_pixel, need_frame, is_seq_frame, is_seq_pixel, pixel_range, frame_range, pixel_per_image)
  len_message, len_total_message, extension, range_message = get_extension_len_message(info_image, pixel_order, BYTE_PER_PIXEL, lsm_byte, EXTRACT_TEMP_FOLDER)
  need_pixel = math.ceil(len_total_message / (BYTE_PER_PIXEL * lsm_byte))
  
  pixel_order = utils.generate_random_order_pixel(seed_from_key, need_pixel, need_frame, is_seq_frame, is_seq_pixel, pixel_range, frame_range, pixel_per_image)
  pixel_order = np.array(pixel_order)
  message = apply_steganoanalytic(info_image, pixel_order, BYTE_PER_PIXEL, lsm_byte, range_message, EXTRACT_TEMP_FOLDER)
  if (extension == 'plain') :
    plain = ''
    for i in range (0,len(message) // 8) :
      a = message[i*8:i*8 + 8]
      x = int(a, 2)
      plain = plain + chr(x)
    print(plain)
  else :
    plain = []
    for i in range (0,len(message) // 8) :
      a = message[i*8:i*8 + 8]
      plain.append(int(a, 2))
    if extension != '':
      output_file_name += '.' + extension
    with open(output_file_name,'wb') as f:
        f.write(bytearray(plain))
  utils.remove(EXTRACT_TEMP_FOLDER)
  
  output_result = {
    'result' : 'success',
    'output_dir' : '{}/{}.{}'.format(os.getcwd(), output_file_name, extension),
  }
  return output_result

def generate_seed(key):
  seed_from_key = 0
  for i in key:
    seed_from_key += ord(i)
  return seed_from_key

def apply_steganography(info_image, pixel_order, byte_message, byte_per_pixel, lsm_byte, temp_folder) :
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
    change_lsb(img_idx, height_img, width_img, message, byte_per_pixel, lsm_byte, temp_folder)

def change_lsb(image_index, height_img, width_img, byte_message, byte_per_pixel, lsm_byte, temp_folder) :
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

def apply_steganoanalytic(info_image, pixel_order, byte_per_pixel, lsm_byte, range_message, temp_folder) :
  message = ''
  for message_idx in range (0, len(pixel_order)*lsm_byte*byte_per_pixel,lsm_byte*byte_per_pixel) :
    byte_idx = pixel_order[int(message_idx/(lsm_byte*byte_per_pixel))]		
    pixel_each_img = info_image['width']*info_image['height']
    img_idx = byte_idx // pixel_each_img
    height_img = (byte_idx % pixel_each_img) // (info_image['width'])
    width_img = (byte_idx % pixel_each_img) % (info_image['width'])
    message = message + extract_lsb(img_idx, height_img, width_img, byte_per_pixel, lsm_byte, temp_folder)

  return(message[range_message[0]:range_message[1]])

def extract_lsb(image_index, height_img, width_img, byte_per_pixel, lsm_byte, temp_folder) :
  image = cv2.imread(temp_folder + "/" + str(int(image_index)) + ".png", 1 )
  int_lsb = image[int(height_img), int(width_img)]
  message = ''
  byte_lsb = ['{0:08b}'.format(x) for x in int_lsb]
  for byte in range (0, byte_per_pixel) :
    message += (byte_lsb[byte])[-1*(lsm_byte):]
  return(message)

def get_extension_len_message(info_image, pixel_order, byte_per_pixel, lsm_byte, temp_folder) :
  message = ''
  is_len = True
  is_extension = False
  extension = ''
  len_message = 0
  xi = 1
  len_total_message = 0
  extension_idx = 0
  for message_idx in range (0, len(pixel_order)*lsm_byte*byte_per_pixel,lsm_byte*byte_per_pixel) :
    byte_idx = pixel_order[int(message_idx/(lsm_byte*byte_per_pixel))]    
    pixel_each_img = info_image['width']*info_image['height']
    img_idx = byte_idx // pixel_each_img
    height_img = (byte_idx % pixel_each_img) // (info_image['width'])
    width_img = (byte_idx % pixel_each_img) % (info_image['width'])
    message = message + extract_lsb(img_idx, height_img, width_img, byte_per_pixel, lsm_byte, temp_folder)
    range_message = (0, 0)
    if (len(message) // 8 == xi) :
      xi += 1
      plain = ''
      for i in range (0,len(message) // 8) :
        a = message[i*8:i*8 + 8]
        x = int(a, 2)
        plain = plain + chr(x)
      if (plain[-1] == '|') :
        if (is_extension) :
          extension = plain[extension_idx:-1]
          extension_idx = len(plain)
          is_extension = False
          len_total_message = len(plain) * 8 + len_message
        if (is_len) :
          len_message = int(plain[:-1])
          extension_idx = len(plain)
          is_len = False
          is_extension = True
    if (not(is_extension) and not(is_len)) :
      range_message = (extension_idx*8, (extension_idx*8)+len_message)
      break
  return(len_message, len_total_message, extension, range_message)

def extract_config(image_index, temp_folder) :
  image = cv2.imread(temp_folder + "/" + str(image_index) + ".png", 1 )
  int_lsb = image[0,0]
  byte_lsb = ['{0:08b}'.format(x) for x in int_lsb]
  frame_sequencial = ((byte_lsb[0])[-3] == '1')
  pixel_sequencial = ((byte_lsb[1])[-3] == '1')
  lsm_byte = int(str((byte_lsb[2])[-3])) + 1
  return(frame_sequencial, pixel_sequencial, lsm_byte)

def save_config(image_index, frame_sequencial, pixel_sequencial, lsm_byte, temp_folder) :
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
  third_byte = byte_lsb[2][-2:]
  byte_lsb[1] = byte_lsb[2][:-3]
  if (lsm_byte == 2) :
    byte_lsb[2] = byte_lsb[2] + '1' + third_byte
  else :
    byte_lsb[2] = byte_lsb[2] + '0' + third_byte


  int_lsb = tuple([int(x, 2) for x in byte_lsb])

  
  image[0,0] = int_lsb
  cv2.imwrite(temp_folder + "/" + str(image_index) + ".png",image)