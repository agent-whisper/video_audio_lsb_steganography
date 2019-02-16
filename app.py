#!/usr/bin/env python3

import os
from flask import Flask, url_for, request, render_template, redirect

app = Flask(__name__)

UPLOAD_FOLDER = 'fariz_test'
FILE_TYPES = ['video', 'audio']
FUNC_TYPES = ['insert', 'extract']

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'super secret key'

@app.route('/')
def index():
  return 'index page'

# Insertion forms
@app.route('/insert/video/')
def insert_video_form():
  api_url = url_for('insert_video_api', _external=True)
  return render_template('insert/video.html', api_url=api_url)

@app.route('/insert/audio/')
def insert_audio_form():
  return ' insert to audio form'

# Extraction forms
@app.route('/extract/video/')
def extract_video_form():
  return 'extract from video form'

@app.route('/extract/audio/')
def extract_audio_form():
  return ' extract from audio form'

# Insertion API
@app.route('/insert/video/api/', methods=['GET', 'POST'])
def insert_video_api():
  if request.method != 'POST':
    return redirect(url_for('insert_video_form'))

  file_requirements = {'cover_file': 'Cover file', 'hidden_file': 'File to be hidden'}
  form_requirements = {'key': 'Stegano key', 'lsb_type': 'LSB variant type (sequential | random)'}
  for req in file_requirements:
    if req not in request.files:
      return '[Error] function requires => {}'.format(file_requirements[req])
  for req in form_requirements:
    if req not in request.form:
      return '[Error] function requires => {}'.format(form_requirements[req])

  cover_file = request.files['cover_file']
  hidden_file = request.files['hidden_file']
  stegano_key = request.form['key']
  random_options = request.form.getlist('randomized_aspects')

  # How to read the file:
  # test = hidden_file.read()
  # print(test)
  # cover_file.close()
  # hidden_file.close()
  return 'insert to video api'

@app.route('/insert/audio/api/', methods=['GET', 'POST'])
def insert_audio_api():
  if request.method != 'POST':
    return redirect(url_for('insert_audio_form'))
  return ' insert to audio'

# Extraction API
@app.route('/extract/video/api/', methods=['GET', 'POST'])
def extract_video_api():
  if request.method != 'POST':
    return redirect(url_for('extract_video_form'))
  return 'extract from video api'

@app.route('/extract/audio/api/', methods=['GET', 'POST'])
def extract_audio_api():
  if request.method != 'POST':
    return redirect(url_for('extract_audio_form'))
  return ' extract from audio'