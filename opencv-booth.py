import cv2
import os
import time
from datetime import datetime
import numpy as np

# import RPi.GPIO as GPIO

# GPIO.setmode(GPIO.BCM)

# buttonInputPin = 2
# buttonLedPin = 4

# GPIO.setwarnings(False)
# GPIO.setup(buttonInputPin, GPIO.IN)
# GPIO.setup(buttonLedPin, GPIO.OUT)

windowName = 'Photo Booth'
state = 'idle'
slideshowStartedAt = None

# cv2.namedWindow(windowName, cv2.WND_PROP_FULLSCREEN)
# cv2.setWindowProperty(windowName,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

cam = cv2.VideoCapture(0)

def photoBooth():
    global state
    
    while True:
        if state == 'idle':
            showImage('images/press-the-button.png')

        if cv2.waitKey(1) == 32: # button pressed
            buttonPressed()

        if state == 'slideshow':
            continueSlideshow()

        if cv2.waitKey(1) == 27:
            if cam.isOpened():
                cam.release()

            break  # esc to quit

    cv2.destroyAllWindows()

def buttonPressed():
    global state
    if state == 'idle':
        state = 'slideshow'
        startSlideshow()

def startSlideshow():
    global slideshowStartedAt

    print('start slideshow')
    if not os.path.exists('tmp'):
        os.mkdir('tmp')

    removeImage('tmp/photo-1.jpg')
    removeImage('tmp/photo-2.jpg')
    removeImage('tmp/photo-3.jpg')
    removeImage('tmp/photo-4.jpg')
    slideshowStartedAt = currentTimeMilliseconds()

def removeImage(path):
    if os.path.exists(path):
        os.remove(path)

previousMs = 0

def continueSlideshow():
    global state
    global previousMs

    ms = currentTimeMilliseconds() - slideshowStartedAt
    if 1000 <= ms < 2000:
        showImage('images/photo-1.png')
    elif 2000 <= ms < 3000:
        showImage('images/countdown-3.png')
    elif 3000 <= ms < 4000:
        showImage('images/countdown-2.png')
    elif 4000 <= ms < 5000:
        showImage('images/countdown-1.png')
    elif 5000 <= ms < 6000:
        showImage('images/cheese.png')
    elif 6000 <= ms < 7000:
        showCamera()
    elif ms > 7000 and previousMs < 7000:
        takePicture(1)
    elif 7000 <= ms < 8000:
        showPhotoSheet()
    elif 8000 <= ms < 9000:
        state = 'idle'

    previousMs = ms
    
def showImage(filename):
    img = cv2.imread(filename, 1)
    cv2.imshow(windowName, img)

def showCamera():
    _, img = cam.read()
    # if mirror: 
    #     img = cv2.flip(img, 1)
    cv2.imshow(windowName, img)

def takePicture(number):
    _, img = cam.read()
    cv2.imwrite('tmp/photo-' + str(number) + '.jpg', img)

def showPhotoSheet():
    img = cv2.imread('tmp/photo-1.jpg', 1)
    cv2.imshow(windowName, img)

def currentTimeMilliseconds():
    return int(round(time.time() * 1000))

def main():
    photoBooth()

if __name__ == '__main__':
    main()