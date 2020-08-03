'''
    DEVNET REFFFFFFFFFFFFF
    An API for predicting an inputted video from path or youtube url
    CF DEV CF DEV
'''
from keras.models import model_from_json
import pathlib
import cv2
import cvlib as cv
import random
import numpy as np
import os
import pafy
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
# Load model
current_dir = f'{str(pathlib.Path(__file__).parent.absolute())}'
with open(f'{current_dir}/model/model.json', 'r') as json_file:
    model = model_from_json(json_file.read())
    model.load_weights(f'{current_dir}/model/model.h5')

# Note the curr DIR
APP_ROOT = os.getcwd()

def get_votes(video, model=model, sample=39):
    '''
        Samples a video capture into frames, run prediction with model on frames and returns a list of the predictions (votes)
    '''
    votes = []
    flag = 1
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    frames = random.sample([i for i in range(frame_count)], min(sample, frame_count))
    for i in frames:
        detections = []
        video.set(1,i)
        _, frame = video.read() 
        if flag < 6:
            plt.imshow(frame)
            plt.savefig(os.path.join(APP_ROOT+'/static/images/') + str(flag) + "vid")
            flag += 1
        try:
            faces, _ = cv.detect_face(frame, threshold=0.9)
            for j, (x0,y0,x1,y1) in enumerate(faces):
                    face = frame[y0:y1, x0:x1]
                    #cv2.imwrite('C:/Users/loner/Desktop/Deepfake-Detection', face)
                    #plt.imshow(frame)
                    #plt.savefig("output" + str(i) + "png")
                    #plt.imshow(cv2.cvtColor(face, cv2.BGR2RGB))
                    #plt.show()
                    #flag = False
                    face = cv2.resize(face, (100,100), interpolation = cv2.INTER_AREA)
                    face = face.astype(np.float32)
                    face /= 255
                    detections.append(face)
        except Exception:   # Error in face detection or dimensions
            pass
        vote = 0
        for face in detections:
            face = face.reshape((1,len(face[0]),len(face[1]),3))
            prediction = model.predict(face)[0][0]
            vote += int(prediction >= 0.5)
        votes.append(int(vote >= 1))
    return votes

def get_prediction(votes, id, is_youtube, printing=False):
    '''
    Aggregates the votes (predictions) and outputs an answer

    Args:
        votes: predictions
        id: path or url
        is_youtube: if it is a youtube video
    
    Returns:
        (REAL/FAKE, confidence%)
    '''
    reals = votes.count(1)
    fakes = votes.count(0)
    try:
        if reals >= fakes:
            result = 'REAL'
            conf = (reals/(reals+fakes))*100
        else:
            result = 'FAKE'
            conf = (fakes/(reals+fakes))*100
    except Exception:   # Found no faces
        return -1, 0.0
    if printing:
        if is_youtube:
            print(f'{id}: {result} {round(conf,2)}%')
        else: 
            video_name = os.path.basename(id)
            print(f'{video_name}: {result} {round(conf,2)}%')
    return 1 if result == 'REAL' else 0, conf


def predict_video(path, printing=False):

    video = cv2.VideoCapture(path)
    votes = get_votes(video)
    return get_prediction(votes,path,is_youtube=False, printing=printing)

def predict_youtube(url, printing=False):

    vPafy = pafy.new(url)
    name = f'{vPafy.title} ({url})'
    play = vPafy.getbestvideo(preftype='mp4')
    video = cv2.VideoCapture(play.url)
    votes = get_votes(video)
    return get_prediction(votes, name, is_youtube=True, printing=printing)
