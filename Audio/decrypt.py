# Use wave package (native to Python) for reading the received audio file
import wave
import random
import base64
song = wave.open("song_embedded.wav", mode='rb')

def split_array(seq, num):
    out = []
    last = 0

    while last < len(seq):
        out.append(seq[int(last):int(last + num)])
        last += num
    return out

# Convert audio to byte array
frame_bytes = bytearray(list(song.readframes(song.getnframes())))

def get_string(frame_bytes):
    opt = 1
    encrypted = bin(frame_bytes[0])[-1] == '1'
    random_frames = bin(frame_bytes[1])[-1] == '1'
    random_bytes = bin(frame_bytes[2])[-1] == '1'
    opt = 2 if bin(frame_bytes[3])[-1] == '1' else 1

    index = 0 
    temp = ""
    string = ""
    mod_index = 8
    if opt==2 :
        mod_index = 4

    # Extract the LSB of each byte
    if opt==1:
        extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
        extracted = split_array(extracted, 4)

    # Extract the 2 LSB of each byte
    if opt==2:
        extracted = [bin(frame_bytes[i] & 3).lstrip('0b').rjust(2,'0') for i in range(len(frame_bytes))]
        extracted = split_array(extracted, 4)

    # random frame case
    if random_frames:
        random.seed(84)
        frame_list = list(range(len(extracted)))
        random.shuffle(frame_list)
    else:
        frame_list = range(len(extracted))

    # random bytes case
    if random_bytes:
        random.seed(84)
        byte_list = list(range(len(extracted[0])))
        random.shuffle(byte_list)
    else:
        byte_list = range(len(extracted[0]))

    for i in frame_list:
        for j in byte_list:
            if i!=0:
                if index % mod_index != (mod_index - 1):
                    temp += str(extracted[i][j])
                else:
                    temp += str(extracted[i][j])
                    # print(temp)
                    string += chr(int(temp,2))
                    # print(string)
                    temp = ""
                index += 1
    
    return string

# Get the sign of message in audio
def get_info_message(string):
    length = ""
    extension = ""
    i = 0
    while string[i] != '#':
        length += string[i]
        i += 1
    i+=1
    while string[i] != '#':
        extension += string[i]
        i += 1

    return (int(length), extension)

string = get_string(frame_bytes)
length, ext = get_info_message(string)
init = len(str(length)) + len(str(ext)) + 2
decoded = string[init:init+length]
bytes_file = decoded.encode('utf-8')
bytes_file = base64.b64decode(bytes_file)

with open('result' + '.' + ext, 'wb') as fd:
    fd.write(bytes_file)


# Print the extracted text
print("Decrypted!!")
print('Your Message : ' +decoded)
song.close()