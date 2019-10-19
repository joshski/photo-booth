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

windowWidth = 800
windowHeight = 600

cam = cv2.VideoCapture(0)

cam.set(cv2.CAP_PROP_FRAME_WIDTH, windowWidth)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, windowHeight)

# cv2.namedWindow(windowName, cv2.WND_PROP_FULLSCREEN)
# cv2.setWindowProperty(windowName,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)



def photoBooth():
    global state
    
    while True:
        if state == 'idle':
            showImage('images/press-the-button.png')

        if cv2.waitKey(1) == 32: # button pressedwindowHeght
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

    if not os.path.exists('photos'):
        os.mkdir('photos')

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
    if ms < 10000:
        continueSlideshowStep(1, ms, previousMs)
    elif ms < 20000:
        continueSlideshowStep(2, ms - 10000, previousMs - 10000)
    elif ms < 30000:
        continueSlideshowStep(3, ms - 20000, previousMs - 20000)
    elif ms < 40000:
        continueSlideshowStep(4, ms - 30000, previousMs - 30000)
    elif ms > 40000 and previousMs < 40000:
        savePhotoSheet()
    elif ms > 50000:
        state = 'idle'

    previousMs = ms

def continueSlideshowStep(step, ms, previousMs):
    if ms < 1000:
        showImage('images/photo-' + str(step) + '.png')
    elif ms < 2000:
        showImage('images/countdown-3.png')
    elif ms < 3000:
        showImage('images/countdown-2.png')
    elif ms < 4000:
        showImage('images/countdown-1.png')
    elif ms < 4500:
        showImage('images/cheese.png')
    elif ms < 7500:
        showCamera()
    elif ms >= 7500 and previousMs < 7500:
        takePhoto(step)
    elif ms < 8000:
        showPhoto(step)
    elif ms < 9000:
        showPhotoSheet()

def showImage(filename):
    img = cv2.imread(filename, 1)
    cv2.imshow(windowName, img)

def showCamera():
    _, img = cam.read()
    # if mirror: 
    img = cv2.flip(img, 1)
    cv2.imshow(windowName, img)

def takePhoto(number):
    _, img = cam.read()
    img = cv2.flip(img, 1)
    cv2.imwrite('tmp/photo-' + str(number) + '.jpg', img)

def showPhotoSheet():
    photoSheetTop = np.concatenate((photoSheetImage(1), photoSheetImage(2)), axis=1)
    photoSheetBot = np.concatenate((photoSheetImage(3), photoSheetImage(4)), axis=1)
    photoSheet = np.concatenate((photoSheetTop, photoSheetBot), axis=0)
    cv2.imshow(windowName, photoSheet)

def savePhotoSheet():
    photoSheetTop = np.concatenate((readPhoto(1), readPhoto(2)), axis=1)
    photoSheetBot = np.concatenate((readPhoto(3), readPhoto(4)), axis=1)
    photoSheet = np.concatenate((photoSheetTop, photoSheetBot), axis=0)
    cv2.imwrite('photos/photo-' + str(currentTimeMilliseconds()) + '.jpg', photoSheet)

def photoSheetImage(number):
    image = None
    if os.path.exists('tmp/photo-' + str(number) + '.jpg'):
        image = cv2.imread('tmp/photo-' + str(number) + '.jpg', 1)
    else:
        image = cv2.imread('images/4up-background.png', 1)

    return cv2.resize(image, (int(windowWidth / 2), int(windowHeight / 2)))

def readPhoto(number):
    return cv2.imread('tmp/photo-' + str(number) + '.jpg', 1)

def showPhoto(number):
    img = readPhoto(number)
    cv2.imshow(windowName, cv2.resize(img, (windowWidth, windowHeight)))

def currentTimeMilliseconds():
    return int(round(time.time() * 1000))

def main():
    photoBooth()

if __name__ == '__main__':
    main()