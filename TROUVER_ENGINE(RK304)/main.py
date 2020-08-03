"""
    Author - Devesh
    Team TURING
"""
######################################################
import dlib
from flask import * 
from flask_ngrok import run_with_ngrok
from flask import Flask , render_template 
from flask_ngrok import run_with_ngrok
from flask import session, url_for 
from flask import * 
from tqdm import tqdm
from flask import request, redirect
from flask_dropzone import Dropzone
import os
######################################################
from devCore import create_CMFD_model
from matplotlib import pyplot as plt
import warnings
from pylab import *
import re
from PIL import Image, ImageChops, ImageEnhance
######################################################
import cv2
import numpy as np
from keras.preprocessing import image
from keras.models import model_from_json
# Imports PIL module  
from PIL import Image 
import tensorflow as tf
import pickle
#####################################################
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup
from newspaper import Article
#####################################################
app = Flask(__name__)
dropzone = Dropzone(app)    # INIT DROPZONE FOR FILE UPLOAD
#run_with_ngrok(app)  
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

""" LOADING DEVNET -- """
cmfdModel = create_CMFD_model('./pretrained_devNet.hd5')
print("------- DevNet Loaded from Disk --------")
# load model from JSON file
with open("modela.json", "r") as json_file:
    loaded_model_json = json_file.read()
    loaded_model = model_from_json(loaded_model_json)

# load weights into the new model
loaded_model.load_weights("modelNNa.h5")
print("-------- Model loaded from disk --------")
#loaded_model.summary()
model = pickle.load(open('final_model.sav', 'rb'))
############# HELPER ################################
from interface import predict_video, predict_youtube

# Note the curr DIR
APP_ROOT = os.path.abspath(app.root_path)
#print(APP_ROOT, file=sys.stderr)
#print(resource_path, file=sys.stderr)
VideoDir = APP_ROOT
#print(VideoDir, file=sys.stderr)
app.config.update(
    UPLOADED_PATH=os.path.join(APP_ROOT, 'static\images'),
    # Flask-Dropzone config:
    DROPZONE_MAX_FILE_SIZE=3000000,
    DROPZONE_MAX_FILES=20,
    DROPZONE_UPLOAD_MULTIPLE = True
)

app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config["DROPZONE_ALLOWED_FILE_TYPE"] = 'image/*, .mp4'
#app.config['DROPZONE_REDIRECT_VIEW'] = 'upload_image'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

""" Init some thingys """
storeResult = {}    # store img result 
sNo = 1
storeResultVid = {} # store vid result
res = 0
conf = 0
OP = ["1", "2", "3", "4", "5"]
NETWORK_LIST = ["facebook", "flickr", "twitter"]
res = ""
var = ""
ans = []
"""                   """

############################################
from newsapi import NewsApiClient
newsapi = NewsApiClient(api_key='e122d722038042529cf99dba207ca492')
dictNEWS = {}

#################CAN ADD THIS FEATURE##########################
def getNEWS(a):
    news_sources = newsapi.get_sources()
    for source in news_sources['sources']:
        print(source['name'])

    all_articles = newsapi.get_everything(
        q=a,
        language='en',   
    )

    # Extracting all realted news article
    for article in all_articles['articles']:
        print('Source : ',article['source']['name'])
        print('Title : ',article['title'])
        print('Description : ',article['description'],'\n\n')
        dictNEWS['Source']

#################################################################

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/text_forensic')
def text_forensic():
    return render_template('text_forensic.html')

@app.route('/image_forensic')
def image_forensic():
    return render_template('image_forensic.html')

@app.route('/video_forensic')
def video_forensic():
    return render_template('video_forensic.html')

@app.route('/viral_forensic')
def viral_forensic():
    return render_template('viral_forensic.html')

"""
    Upload Image
"""
@app.route('/upload_image', methods=['POST', 'GET'])
@cross_origin()
def upload_image():
    #flash("HERE")
    global filename
    file = None
    if request.method == 'POST':
        file_obj = request.files
        for key, f in request.files.items():
            if key.startswith('file'):
                #name = f.filename
                global sNo
                global storeResult
                imgDir = os.path.join(app.config["UPLOADED_PATH"], f.filename)
                f.save(imgDir)   # save image

                img = image.load_img(imgDir)
                img = image.img_to_array(img)
                img = np.expand_dims(img, axis = 0)
                data = cmfdModel.predict(img)
                plt.imshow(data.squeeze())
                modDir = os.path.join(app.config["UPLOADED_PATH"], str(sNo) + 'img')
                plt.savefig(modDir) 
                plt.close()
                # Store RESULTS
                imgDirx = "/static/images/" + f.filename
                modDirx = "/static/images/" + str(sNo) + 'img'
                print(imgDirx, file=sys.stderr)
                print(modDirx, file=sys.stderr)
                storeResult[imgDirx] = modDirx
                sNo += 1
                #f = request.files.get(f)
                #print (f.filename)
    return jsonify("1")

"""
    Return Image Analysis Result
"""
@app.route('/image_result')
def image_result():
    print(len(storeResult), file=sys.stderr)
    dict = storeResult.copy()
    storeResult.clear()
    return render_template('image_result.html', len = len(dict), storeResult = dict)


#####################################################


"""
    Upload Video
"""
@app.route('/upload_video', methods=['POST', 'GET'])
def upload_video():
    global filename
    global res
    global conf
    if request.method == 'POST':
        for key, f in request.files.items():
            if key.startswith('file'):
                # Change PATH accordingly -----------------
                # Wherever the folder Lies
                dd = "C:/Users/loner/Desktop/TROUVER_ENGINE(RK304)/static/videos/" + f.filename
                f.save(dd)
                res, conf = predict_video(dd)
                ddx = "/static/videos/" + f.filename
                storeResultVid[ddx] = [res, conf]
    return jsonify("1")

"""
    Return Video Analysis Result
"""
@app.route('/video_result')
def video_result():
    dict = storeResultVid.copy()
    storeResultVid.clear()
    return render_template('video_result.html', storeResultVid = dict, OP = OP)

###### HELPER FN ############
def predictSite(img):
    preds = loaded_model.predict(img)
    #return self.preds
    return NETWORK_LIST[np.argmax(preds)]

@app.route('/upload_viral', methods = ['POST', 'GET'])
def upload_viral():
    global filename
    file = None
    if request.method == 'POST':
        file_obj = request.files
        for key, f in request.files.items():
            if key.startswith('file'):
                #name = f.filename
                print("IM HERE", file=sys.stderr)
                global sNo
                global storeResult
                imgDir = os.path.join(app.config["UPLOADED_PATH"], f.filename)
                f.save(imgDir)   # save image

                # predicting images
                print(imgDir, file=sys.stderr)
                img_width, img_height = 64, 64
                img = image.load_img(imgDir, target_size = (img_width, img_height))
                img = image.img_to_array(img)
                img = np.expand_dims(img, axis = 0)
                print("IM HERE2", file=sys.stderr)
                global res
                res = predictSite(img)
                print(res, file=sys.stderr)
                #f = request.files.get(f)
                #print (f.filename)
    return jsonify("1")
#########################################################

@app.route('/viral_result')
def viral_result():
    print("HEREEEEEEEEEEEEEEEEEE" + res, file=sys.stderr)
    return render_template("viral_result.html", recv = res)

@app.route('/upload_text', methods = ['POST', 'GET'])
def upload_text():
    global ans
    if request.method == 'POST':
        url = request.form['url']
        print(url, file=sys.stderr)
        print("Yo valid string " + url)
        article = Article(url)
        article.download()
        article.parse()
        j = article.title
        #getNEWS(j)      # HERE YOU GET ALL THE RELATED NEWS ARTICLE
        var = str(article.text)
        #except:
        #    print("Yo not a string i guess")
        #    var = str(url)
    
        prediction = model.predict([var])
        prob = model.predict_proba([var])
        # truth = prob[0][1]
        ans =  [prediction[0], prob[0][1]]
    return render_template('text_result.html', ans = ans)

@app.route('/text_result', methods = ['POST', 'GET'])
def text_result():
    print(ans, file=sys.stderr)
    return render_template('text_result.html', ans = ans)

if __name__ == "__main__":
    app.run()
