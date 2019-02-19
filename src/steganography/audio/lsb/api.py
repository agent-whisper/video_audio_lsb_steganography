import base64
import os

import src.steganography.audio.lsb.inserter as audio_ins
import src.steganography.audio.lsb.extractor as audio_ext

def hide_message(cover_file_dir, secret_message_dir, key, output_filename, is_random_byte, is_random_frame, lsb_bit_mode, encrypt, is_mono):
    e = audio_ins.MessageInserter()
    frame_bytes = e.read_frame_file(cover_file_dir)
    params = e.get_params(cover_file_dir)
    message, ext = e.read_files(secret_message_dir)

    # Base64 encode first to handle any files before insert to audio
    message = base64.b64encode(message).decode('utf-8')

    frame_modified = e.insert_message(
        ext,
        message,
        frame_bytes,
        key,
        is_mono,
        lsb_bit_mode=lsb_bit_mode,
        randomize_bytes=is_random_byte,
        randomize_frames=is_random_frame,
        encrypted=encrypt,
    )
    if frame_modified is None : 
        result = {
            'result' : 'failed',
        }
        return result
    output_filename += ('.wav')
    e.write_file(output_filename, frame_modified, params)
    result = {
        'result' : 'success',
        'output_dir' : '{}/{}'.format(os.getcwd(), output_filename),
    }
    return result

def extract_message(stegano_audio_dir, key, output_filename):
    d = audio_ext.MessageExtractor()
    filebytes = d.read_encrypted_file(stegano_audio_dir)
    lsb = d.get_lsb(filebytes,key)
    length, ext = d.get_info_message(lsb)
    complete_output_filename = '{}'.format(output_filename)
    if ext != '':
        complete_output_filename += '.' + ext
    print(ext)
    d.write_secret_message(length, ext, lsb, complete_output_filename)
    result = {
        'result' : 'success',
        'output_dir' : '{}/{}'.format(os.getcwd(), complete_output_filename),
    }
    return result

def check_is_mono(stegano_audio_dir):
    d = audio_ins.MessageInserter()
    param = d.get_params(stegano_audio_dir)
    return (param[0] == 1)