from video_lsb import *

key = "ferdi"

byte_per_pixel = 3
lsm_byte = 1

info_image = video_to_image('./output/video.avi')


image_index = 0
frame_sequencial, pixel_sequencial = extract_config(image_index)

key_int = 0
for i in key :
	key_int += ord(i)

import math
need_pixel = 240
need_frame = math.ceil(need_pixel / (info_image['width'] * info_image['height']))
pixel_range = (0, info_image['width']*info_image['height']*info_image['total_image'])
frame_range = (0, info_image['total_image'])
pixel_per_image = info_image['width'] * info_image['height']
need_pixel = int(need_pixel)
need_frame = int(need_frame)
pixel_order = generate_random_order_pixel(key_int, need_pixel, need_frame, frame_sequencial, pixel_sequencial, pixel_range, frame_range, pixel_per_image)
ledcn_message, len_total_message, extension, range_message = get_extension_len_message(info_image, pixel_order, byte_per_pixel, lsm_byte)
need_pixel = math.ceil(len_total_message / (byte_per_pixel * lsm_byte))
print(key_int, need_pixel, need_frame, frame_sequencial, pixel_sequencial, pixel_range, frame_range, pixel_per_image)
pixel_order = generate_random_order_pixel(key_int, need_pixel, need_frame, frame_sequencial, pixel_sequencial, pixel_range, frame_range, pixel_per_image)
pixel_order = np.array(pixel_order)
print(range_message)
message = steganoanalytic(info_image, pixel_order, byte_per_pixel, lsm_byte, range_message)


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
	with open('decrypt.' + extension,'wb') as f:
	    f.write(bytearray(plain))

remove('temp')


