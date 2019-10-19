import cv2
import os
import time
from datetime import datetime

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
    global slideshowStartedAt
    if state == 'idle':
        state = 'slideshow'
        slideshowStartedAt = datetime.now()

def startSlideshow():
    print('start slideshow')

def continueSlideshow():
    showCamera()
    time = datetime.now() - slideshowStartedAt
    print('continue slideshow')
    print(str(time))
    
def showImage(filename):
    img = cv2.imread(filename, 1)
    cv2.imshow(windowName, img)

def showCamera():
    _, img = cam.read()
    # if mirror: 
    #     img = cv2.flip(img, 1)
    cv2.imshow(windowName, img)

def takePicture():
    _, img = cam.read()
    cv2.imwrite('img.jpg', img)

def main():
    photoBooth()

if __name__ == '__main__':
    main()