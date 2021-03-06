"""
emotions will be displayed on your face from the webcam feed
"""

import os

import cv2
import numpy as np

import global_variables as gv

# set tensorflow log level
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# build the model
model = gv.build_model()
# and load it into structure
model.load_weights('model.h5')

# prevents openCL usage and unnecessary logging messages
cv2.ocl.setUseOpenCL(False)

# start the webcam feed
cap = cv2.VideoCapture(0)
while True:
    # Find haar cascade to draw bounding box around face
    ret, frame = cap.read()
    if not ret:
        break
    facecasc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facecasc.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # loop through all faces, crop, draw a rectangle and predict
    # then draw prediction in text
    prediction = None
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y - 50), (x + w, y + h + 10), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
        prediction = model.predict(cropped_img)
        maxindex = int(np.argmax(prediction))
        cv2.putText(frame, gv.emotion_names[maxindex], (x + 20, y - 60), cv2.QT_FONT_NORMAL, 1,
                    (255, 255, 255),
                    2, cv2.LINE_AA)

    # show the frame
    cv2.imshow('Video', cv2.resize(frame, (1600, 960), interpolation=cv2.INTER_CUBIC))

    # if q is pressed quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release cams and destroy windows
cap.release()
cv2.destroyAllWindows()
