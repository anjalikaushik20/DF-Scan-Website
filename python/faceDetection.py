import cv2
from tensorflow import keras 
from mtcnn import MTCNN
import sys, os.path
import json
from keras import backend as K
import tensorflow as tf
import math
import numpy as np
from PIL import Image, ImageChops, ImageEnhance
from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img

_base_path = 'videos'
model = load_model('python/deepfake-detection-model.h5')

def get_filename_only(file_path):
    file_basename = os.path.basename(file_path)
    _filename_only = file_basename.split('.')[0]
    return _filename_only

def FaceDetect(_filename_only):
    count0 = 0
    count1 = 0
    c1 = np.array([1])
    c0 = np.array([0])
    tmp_path = os.path.join(_base_path, _filename_only)
    print('Processing Directory: ' + tmp_path)
    frame_images = [x for x in os.listdir(tmp_path) if os.path.isfile(os.path.join(tmp_path, x))]
    faces_path = os.path.join(tmp_path, 'faces')
    print('Creating Directory: ' + faces_path)
    os.makedirs(faces_path, exist_ok=True)
    print('Cropping Faces from Images...')

    for frame in frame_images:
        #print('Processing ', frame)
        detector = MTCNN()
        image = cv2.cvtColor(cv2.imread(os.path.join(tmp_path, frame)), cv2.COLOR_BGR2RGB)
        results = detector.detect_faces(image)
        #print('Face Detected: ', len(results))
        count = 0
        
        for result in results:
            bounding_box = result['box']
            #print(bounding_box)
            confidence = result['confidence']
            #print(confidence)
            if len(results) < 2 or confidence > 0.95:
                margin_x = bounding_box[2] * 0.3  # 30% as the margin
                margin_y = bounding_box[3] * 0.3  # 30% as the margin
                x1 = int(bounding_box[0] - margin_x)
                if x1 < 0:
                    x1 = 0
                x2 = int(bounding_box[0] + bounding_box[2] + margin_x)
                if x2 > image.shape[1]:
                    x2 = image.shape[1]
                y1 = int(bounding_box[1] - margin_y)
                if y1 < 0:
                    y1 = 0
                y2 = int(bounding_box[1] + bounding_box[3] + margin_y)
                if y2 > image.shape[0]:
                    y2 = image.shape[0]
                #print(x1, y1, x2, y2)
                crop_image = image[y1:y2, x1:x2]
                new_filename = '{}-{:02d}.png'.format(os.path.join(faces_path, get_filename_only(frame)), count)
                count = count + 1
                cv2.imwrite(new_filename, cv2.cvtColor(crop_image, cv2.COLOR_RGB2BGR))

                # #resizing & data split
                # if metadata[filename]['label'] == 'REAL':
                #     cv2.imwrite('/content/drive/MyDrive/Capstone/dataset/real/'+filename.split('.')[0]+'_'+str(count)+'.png', cv2.resize(crop_image, (128, 128)))
                # elif metadata[filename]['label'] == 'FAKE':
                #     cv2.imwrite('/content/drive/MyDrive/Capstone/dataset/fake/'+filename.split('.')[0]+'_'+str(count)+'.png', cv2.resize(crop_image, (128, 128)))
                # #count+=1
                data = img_to_array(cv2.resize(crop_image, (128, 128))).flatten() / 255.0
                data = data.reshape(-1, 128, 128, 3)
                print(np.argmax(model.predict(data), axis=-1))
                if np.array_equal(np.argmax(model.predict(data), axis=-1), c1):
                    count1 = count1 + 1
                elif np.array_equal(np.argmax(model.predict(data), axis=-1), c0):
                    count0 = count0 + 1

            else:
                print('...')

    print(count0)
    print(count1)
    total = count0 + count1
    if count0 > count1:
        fp = (count0/total)*100
        print(f"{fp}% Fake")
        return 'DeepFake Video'
    else:
        rp = (count1/total)*100
        print(f"{rp}% Real")
        return 'Real Video'