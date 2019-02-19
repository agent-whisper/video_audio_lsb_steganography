#!/usr/bin/python3
import getopt
import json
import sys

def read_input_bytes(ifile):
  plaintext = bytes('', 'utf-8')
  try:
    with open(ifile, 'rb') as f:
      for line in f.readlines():
        plaintext += line
  except FileNotFoundError:
    print('[get_input_bytes] file not found')
  return plaintext

def save_output_bytes(data, output_dir):
  with open(output_dir, 'wb+') as f:
    f.write(data)
