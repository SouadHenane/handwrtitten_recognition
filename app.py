# our web app framework!

# you could also generate a skeleton from scratch via
# http://flask-appbuilder.readthedocs.io/en/latest/installation.html

# Generating HTML from within Python is not fun, and actually pretty
# cumbersome because you have to do the
# HTML escaping on your own to keep the application secure.
# Because of that Flask configures the Jinja2 template engine
# for you automatically.
# requests are objects that flask handles (get set post, etc)
import sys
import os
sys.path.append(os.path.abspath("./model"))
from load import *
from flask import Flask, render_template, request
# scientific computing library for saving, reading, and resizing images
import cv2
import numpy as np
#from scipy.misc import imresize
from imageio import imwrite
from binascii import a2b_base64
from keras.preprocessing.image import save_img
from keras.preprocessing import image
# for matrix math
import numpy as np
# for importing our keras model
from skimage.transform import resize

import keras.models
# for regular expressions, saves time dealing with string data
import re

# system level operations (like loading files)

# for reading operating system data
import os

# tell our app where our saved model is
import base64

# initalize our flask app
app = Flask(__name__)
# global vars for easy reusability
global model, graph
# initialize these variables
model = init()


def convertImage(imgData1):
    imgstr = re.search(b'base64,(.*)', imgData1).group(1) #print(imgstr)
    with open('output.png', 'wb') as output:
        output.write(base64.b64decode(imgstr))

# decoding an image from base64 into raw representation
#def convertImage(imgData1):
 #   #imgstr = re.search(r'base64,(.*)', imgData1).group(1)
    #binary_data = a2b_base64(imgData1)
    #fd = open('output.png', 'wb')
    #fd.write(binary_data)
    #fd.close()
    # print(imgstr)
    #with open('output.png', 'wb') as output:
  #  with open('output.png', 'wb') as output:
  #      output.write(base64.b64decode(imgData1))


@app.route('/')
def index():
    # initModel()
    # render out pre-built HTML file right on the index page
    return render_template("index.html")


@app.route('/predict/', methods=['GET', 'POST'])
def predict():
    # whenever the predict method is called, we're going
    # to input the user drawn character as an image into the model
    # perform inference, and return the classification
    # get the raw data format of the image
    imgData = request.get_data()
    # encode it into a suitable format
    convertImage(imgData)
    print("debug")
    # read the image into memory
    #x = mimread('output.png')
    #x = image.load_img('output.png')
    x = cv2.imread('output.png', cv2.IMREAD_GRAYSCALE)
    # compute a bit-wise inversion so black becomes white and vice versa
    #x = np.invert(x)
    # make it the right size
    #x = imresize(x, (28, 28))
    #x = cv2.resize(x, dsize=(28, 28), interpolation=cv2.INTER_CUBIC)
    #x = resize(x, (28, 28))
    x = cv2.resize(255-x, (28, 28))
    #x.resize(28, 28)
    # imshow(x)
    x = x.flatten() / 255.0
    # convert to a 4D tensor to feed into our model
    x = x.reshape(-1, 28, 28, 1)
    print("debug2")
    # in our computation graph
    #with graph.as_default():
    # perform the prediction
    out = model.predict(x)
    print(out)
    print(np.argmax(out, axis=1))
    print("debug3")
    # convert the response to a string
    response = np.array_str(np.argmax(out, axis=1))
    return response


if __name__ == "__main__":
    # decide what port to run the app in
    port = int(os.environ.get('PORT', 5000))
    # run the app locally on the given port
    app.run(host='0.0.0.0', port=port)
# optional if we want to run in debugging mode
# app.run(debug=True)