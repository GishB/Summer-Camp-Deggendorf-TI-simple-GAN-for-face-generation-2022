#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import numpy as np
from PIL import Image
import time


# In[2]:




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

def request_image():
    image_url = 'https://thispersondoesnotexist.com/image'
    req = requests.get(image_url).content
    with open('image_name.jpg', 'wb') as handler:
        handler.write(req)
        
def show_img():
    img = Image.open('image_name.jpg')
    img.show()
    
def request_face(path): #we need a model to chekc image in general
    # 1 is human / 0 is a fake
    face_number = 1 #initial state
    return face_number
def request_sex(path): #we need a model to check sex 
    # 0 is a male / 1 is a female
    sex_number = 1 #initial state
    return sex_number
def request_age(path): #we need a model to check age 
    # 0 is young / 1 is old
    age_number = 0
    return age_number


sex, years = str(input('Write male or female - ')), str(input('Write young or old - '))
input_user = vectorizer(sex, years)


# In[3]:


valid = False #initial state

while valid != True: # here is important for models!
    try:
        request_image() #download image from website
        
        model_face = request_face('image_name.jpg') #check if it is a human face. Always should be 1
        model_sex = request_sex('image_name.jpg') #check if it is a man or female
        model_age = request_age('image_name.jpg') #check if is old or young
        
        if model_sex == input_user[0] and model_age == input_user[1] and model_face == 1: #check parameters
            valid = True #changed main parameter to finish loop
            show_img() #look at GAN image
        else:
            time.sleep(1) #just to be sure we do not have ban because of surfing
    except:
        print('Something goes wrong with request_image')


# In[ ]:




