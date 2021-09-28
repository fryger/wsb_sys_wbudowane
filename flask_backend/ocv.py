import tensorflow_hub as hub
import cv2
import numpy
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import os

def calculateSpots(width,height, y, x, url):
    i = 0
    vcap = cv2.VideoCapture(url)

    while(True):
        ret, frame = vcap.read()
        if frame is not None:
            img = frame
            break

    img = img[y:y+height, x:x+width]
    inp = cv2.resize(img, (width, height))

    rgb = cv2.cvtColor(inp, cv2.COLOR_BGR2RGB)
    
    rgb_tensor = tf.convert_to_tensor(rgb, dtype=tf.uint8)
    
    rgb_tensor = tf.expand_dims(rgb_tensor, 0)
    
    detector = hub.load(
        os.path.abspath('./flask_backend/model/'))

    labels = pd.read_csv(os.path.abspath('./flask_backend/model/labels.csv'), sep=';', index_col='ID')
    labels = labels['OBJECT (2017 REL.)']

    boxes, scores, classes, num_detections = detector(rgb_tensor)

    pred_labels = classes.numpy().astype('int')[0]
    pred_labels = [labels[i] for i in pred_labels]
    pred_boxes = boxes.numpy()[0].astype('int')
    pred_scores = scores.numpy()[0]

    for score, (ymin, xmin, ymax, xmax), label in zip(pred_scores, pred_boxes, pred_labels):
        if score < 0.3:
            continue
        if label == 'car' or label == 'bus' or label == 'motorcycle' or label == 'truck':
            i+=1
    
        score_txt = f'{100 * round(score)}%'
        img_boxes = cv2.rectangle(rgb, (xmin, ymax), (xmax, ymin), (0, 255, 0), 2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img_boxes, label, (xmin, ymax-10),
                    font, 1.5, (255, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(img_boxes, score_txt, (xmax, ymax-10),
                    font, 1.5, (255, 0, 0), 1, cv2.LINE_AA)
    #plt.imshow(img_boxes)
    #plt.show()
    
    cv2.imwrite('./output.jpg', img_boxes)
    return i

if __name__ == '__main__':
    print(calculateSpots(1920,1080, 300, 0, 'https://imageserver.webcamera.pl/rec/lanckorona/latest.mp4'))
    