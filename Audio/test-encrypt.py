from encrypt import Encrypt
import base64

e = Encrypt()
frame_bytes = e.read_frame_file('1.wav')
params = e.get_params('1.wav')
message, ext = e.read_files("1.wav")

# Base64 encode first to handle any files before insert to audio
message = base64.b64encode(message).decode('utf-8')

frame_modified = e.insert_message(ext,False, False, True, message, frame_bytes, 'test', 1)
if frame_modified is not None : e.write_file('coba2',frame_modified,params)