import cv2

windowName = 'Photo Booth'

# cv2.namedWindow(windowName, cv2.WND_PROP_FULLSCREEN)
# cv2.setWindowProperty(windowName,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

def show_webcam(mirror=False):
    cam = cv2.VideoCapture(0)
    while True:
        ret_val, img = cam.read()
        if mirror: 
            img = cv2.flip(img, 1)
        cv2.imshow(windowName, img)
        if cv2.waitKey(1) == 27:
            if cam.isOpened():
                cam.release()
                cv2.imwrite('img.jpg', img)

            break  # esc to quit

    cv2.destroyAllWindows()


def main():
    show_webcam(mirror=True)


if __name__ == '__main__':
    main()