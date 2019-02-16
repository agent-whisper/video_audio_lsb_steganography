# Using wave to read wav file
import wave
import random
import base64

# Read audio file
song = wave.open("test.wav", mode='rb')

# Split array
def split_array(seq, num):
    out = []
    last = 0

    while last < len(seq):
        out.append(seq[int(last):int(last + num)])
        last += num
    return out

# Read frame as bytes
def read_as_bytes(fileaudio):
    frame_bytes = bytearray(list(fileaudio.readframes(fileaudio.getnframes())))
    frame_bytes = split_array(frame_bytes,4)
    return frame_bytes

def read_files(file):
    ext = file.split(".")[-1]
    with open(file, "rb") as f:
        byte_file = f.read()
    return (byte_file, ext)

# Insert message to 
def insert_message(extension, encrypted, randomize_bytes, randomize_frames, message, frame, key=None, opt=1):
    len_message = str(len(message))
    string = len_message + '#' + extension + '#' + message
    if key is not None:
        key = key.upper()
        seed = 0
        for i in key:
            seed = ord(i)
    
    # Give sign if encrypted
    if encrypted:
        frame[0][0] = frame[0][0] & 254 | 1
        # encrypt string with key
    else:
        frame[0][0] = frame[0][0] & 254 | 0

    # Convert text to bit array
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string])))

    if randomize_frames:
        frame[0][1] = frame[0][1] & 254 | 1
        random.seed(seed)
        frame_list = list(range(len(frame)))
        random.shuffle(frame_list)
    else:
        frame [0][1] = frame[0][1] & 254 | 0
        frame_list = list(range(len(frame)))
    
    if randomize_bytes:
        frame[0][2] = frame[0][2] & 254 | 1
        random.seed(seed)
        bytes_list = list(range(len(frame[0])))
        random.shuffle(bytes_list)
    else:
        frame[0][2] = frame[0][2] & 254 | 0
        bytes_list = list(range(len(frame[0])))
    
    index = 0
    if opt==2:
        frame[0][3] = frame[0][3] & 254 | 1
        for i in frame_list:
            for j in bytes_list:
                if index >= len(bits):
                    break
                if i != 0:
                    frame[i][j] = frame[i][j] & 252 | (2*bits[index] + bits[index+1])
                    index += 2
    else:
        frame[0][3] = frame[0][3] & 254 | 0
        for i in frame_list:
            for j in bytes_list:
                if index >= len(bits):
                    break
                if i != 0:
                    frame[i][j] = frame[i][j] & 252 | bits[index]
                    index+=1

    frame_modified = bytes()
    merged_array = bytearray()

    for i in frame:
        merged_array += i

    # Convert to bytes 
    frame_modified += bytes(merged_array)
    return frame_modified



frame_bytes = read_as_bytes(song)
message, ext = read_files("test.png")
message = base64.b64encode(message).decode('utf-8')
frame_modified = insert_message(ext,True, False, True, message, frame_bytes, 'test', 1)

# Write bytes to a new wave audio file
with wave.open('song_embedded.wav', 'wb') as fd:
    fd.setparams(song.getparams())
    fd.writeframes(frame_modified)
song.close()