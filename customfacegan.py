# -*- coding: utf-8 -*-
"""CustomFaceGAN

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ltzK5VeFsffMg_igUOk6CNtLu_KmrfIr

# Import files
"""

!pip install MTCNN
!git clone https://github.com/NVlabs/stylegan3.git
!pip install ninja

import requests #take an image from website
import numpy as np
from PIL import Image # print image in collab
import time
import tensorflow as tf
from mtcnn.mtcnn import MTCNN #detect face
import cv2 # for images
import subprocess #bash script in python code
import glob

from IPython.display import display, Image

"""# Functions"""

detector = MTCNN() #detect faces

age_model = tf.keras.models.load_model("/content/256-binary_age.h5")
gender_model = tf.keras.models.load_model("/content/256-binary_gender.h5")

age_labels = [0, 1] # 0 is young and 1 is old
gender_labels = [0, 1] # 0 is male and 1 is female

def vectorizer(sex, years):
    if sex == 'male':
        sex_number = 0
    elif sex == 'female':
        sex_number = 1
    if years == 'young':
        years_number = 0
    elif years == 'old':
        years_number = 1
    return sex_number, years_number

def request_image(user_number=0):
    if user_number == 0:
      image_url = 'https://thispersondoesnotexist.com/image'
      req = requests.get(image_url).content
      with open('image_name.jpg', 'wb') as handler:
          handler.write(req)
      path = '/content/image_name.jpg'

    else:
      seed = np.random.randint(0,500) # or random
      print(seed)
      bashCommand = "python3 /content/stylegan3/gen_images.py --outdir=out --trunc=1 --seeds=" + str(seed) + \
    " --network=https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan3/versions/1/files/stylegan3-r-ffhq-1024x1024.pkl"
      process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
      output, error = process.communicate()

      path = glob.glob('/content/out/*' + str(seed) + '.png')[0]
      print(path)
    return cv2.imread(path)


def show_img():
    display(Image(filename='/content/image_name.jpg'))
    
def request_face(img): #we need a model to chekc image in general
    # 1 is human / 0 is a fake
    coordinate_faces = detector.detect_faces(img)
    if len(coordinate_faces) == 1:
      face_number = 1 #initial state
    else:
      face_number = 0
    return face_number

def request_sex(img): #we need a model to check sex 
    # 0 is a male / 1 is a female
    genderPred = gender_model.predict(img)
    gender_label = gender_labels[genderPred[0].argmax()]
    return gender_label
            
def request_age(img): #we need a model to check age 
    # 0 is young / 1 is old
    agePred = age_model.predict(img)
    age_label = age_labels[agePred[0].argmax()]
    return age_label

"""# inputs"""

sex, years, generate_number = str(input('Write male or female - ')), str(input('Write young or old - ')), int(input('Chose GAN model 0 or 1 - '))
input_user = vectorizer(sex, years)

"""# run

"""

valid = False #initial state

while valid != True: # here is important for models!
    try:
        img = request_image(generate_number) #download image from website
        face = cv2.resize(img, (256,256)).reshape(-1,256,256,3)

        model_face = request_face(img) #check if it is a human face. Always should be 1
        model_sex = request_sex(face) #check if it is a man or female
        model_age = request_age(face) #check if is old or young

        print(model_sex, model_age)
        if model_sex == input_user[0] and model_age == input_user[1] and model_face == 1: #check parameters
            valid = True #changed main parameter to finish loop
            show_img() #look at GAN image
        else:
            print('in progress...')
    except:
        print('Something goes wrong with request_image')
