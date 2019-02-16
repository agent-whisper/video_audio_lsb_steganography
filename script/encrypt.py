from function2 import *
import math

key = "ferdi"
byte_per_pixel = 3
lsm_byte = 1
frame_sequencial = True
pixel_sequencial = False

info_image = video_to_image('../video/test3.avi')


# contoh input text
message = "ferdi ghozali keren"
extension_message = 'plain'
byte_message = ''.join('{0:08b}'.format(ord(x)) for x in vigenere_encrypt(message, key))

# # contoh input file
file_name = 'input.png'
extension_message = ''
for character_idx in range (len(file_name)-1, -1, -1) :
	if (file_name[character_idx] == '.') :
		break
	extension_message = file_name[character_idx] + extension_message


ord_bytes = []
message = ''
with open(file_name, "rb") as input:
	while True :
		word = input.read(1)
		if (word == b'') :
			break
		ord_bytes.append(word)
		message = message + chr(ord(word))

byte_message = ''.join('{0:08b}'.format(ord(x)) for x in ord_bytes)




key_int = 0
for i in key :
	key_int += ord(i)

image_index = 0
save_config(image_index, frame_sequencial, pixel_sequencial)


len_message = len(byte_message)


message = str(len_message) + '|' + extension_message + '|' + vigenere_encrypt(message, key)

byte_message = ''.join('{0:08b}'.format(ord(x)) for x in message)


informationa_max_per_image = info_image['width']*info_image['height']*byte_per_pixel*lsm_byte

if ((informationa_max_per_image * info_image['total_image']) < len(byte_message)) :
	print('message too long')
	exit()

import math
need_pixel = math.ceil(len(byte_message) / (byte_per_pixel * lsm_byte))
need_frame = math.ceil(need_pixel / (info_image['width'] * info_image['height']))
need_pixel = int(need_pixel)
need_frame = int(need_frame)
pixel_range = (0, info_image['width']*info_image['height']*info_image['total_image'])
frame_range = (0, info_image['total_image'])
pixel_per_image = info_image['width'] * info_image['height']

print(key_int, need_pixel, need_frame, frame_sequencial, pixel_sequencial, pixel_range, frame_range, pixel_per_image)
pixel_order = generate_random(key_int, need_pixel, need_frame, frame_sequencial, pixel_sequencial, pixel_range, frame_range, pixel_per_image)
temp_pixel_order = pixel_order

steganography(info_image, pixel_order, byte_message, byte_per_pixel, lsm_byte)

from subprocess import call,STDOUT

output_folder = 'output'
try :
	os.mkdir(output_folder)
except OSError:
	remove(output_folder)
	os.mkdir(output_folder)

call(["ffmpeg", "-i", "temp/%d.png" , "-r", str(info_image['fps']), "-vcodec", "png", "output/video.avi", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)
remove('temp')