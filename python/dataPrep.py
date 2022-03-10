import cv2
from tensorflow import keras 
from mtcnn import MTCNN
import sys, os.path
import json
from keras import backend as K
import tensorflow as tf
import math
import python.faceDetection as fd


print(tf.__version__)
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

_base_path = 'videos'
_fname = ''

def dataProcess(_filename_only):

    _fname = _filename_only
    _filename = _filename_only + '.mp4'

    tmp_path = os.path.join(_base_path, _filename_only)
    print('Creating Directory: ' + tmp_path)
    os.makedirs(tmp_path, exist_ok=True)
    print('Converting Video to Images...')
    count = 0
    video_file = os.path.join(_base_path, _filename)
    cap = cv2.VideoCapture(video_file)
    frame_rate = cap.get(5) #frame rate
    while(cap.isOpened()):
        frame_id = cap.get(1) #current frame number
        ret, frame = cap.read()
        if (ret != True):
            break
        if (frame_id % math.floor(frame_rate) == 0):
            print('Original Dimensions: ', frame.shape)
            if frame.shape[1] < 300:
                scale_ratio = 2
            elif frame.shape[1] > 1900:
                scale_ratio = 0.33
            elif frame.shape[1] > 1000 and frame.shape[1] <= 1900 :
                scale_ratio = 0.5
            else:
                scale_ratio = 1
            print('Scale Ratio: ', scale_ratio)

            width = int(frame.shape[1] * scale_ratio)
            height = int(frame.shape[0] * scale_ratio)
            dim = (width, height)
            new_frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
            print('Resized Dimensions: ', new_frame.shape)

            new_filename = '{}-{:03d}.png'.format(os.path.join(tmp_path, _filename_only), count)
            count = count + 1
            cv2.imwrite(new_filename, new_frame)
    cap.release()
    print("Done!")
    result = fd.FaceDetect(_fname)
    return result


