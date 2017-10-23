import time
import cv2
import cv2.cv as cv
import numpy as np
from PIL import Image

def jpg_image_to_array(image_path):
    """
    Loads JPEG image into 3D Numpy array of shape 
    (width, height, channels)
    """
    with Image.open(image_path) as image:         
        im_arr = np.fromstring(image.tobytes(), dtype=np.uint8)
        im_arr = im_arr.reshape((image.size[1], image.size[0], 3))                                   
    return im_arr

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

def detect(img, cascade):
    # Parameters taken verbatim from OpenCV 2.4 example:
    # https://github.com/opencv/opencv/blob/2.4/samples/python2/facedetect.py
    rects = cascade.detectMultiScale(gray, 
                        scaleFactor=1.3, 
                        minNeighbors=4, 
                        minSize=(30, 30), 
                        flags = cv.CV_HAAR_SCALE_IMAGE)

    if len(rects) == 0:
        return []

    # Turn width and height of box
    # into plot-ready image coordinates.
    rects[:,2:] += rects[:,:2]
    return rects



if __name__=="__main__":
    filename = "face.jpeg"
    image = jpg_image_to_array(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    nested = cv2.CascadeClassifier("haarcascade_eye.xml")

    # Get rectangle for entire face
    rects = detect(gray, cascade)
    print(len(rects))

    # Get rectangles for subfeatures (eyes)
    vis = gray.copy()
    draw_rects(vis, rects, (0, 255, 0))

    for x1, y1, x2, y2 in rects:
        roi = gray[y1:y2, x1:x2]
        vis_roi = vis[y1:y2, x1:x2]
        subrects = detect(roi.copy(), nested)
        draw_rects(vis_roi, subrects, (255, 0, 0))
        print(len(subrects))

    cv2.imshow('facedetect', vis)
    cv2.waitKey()


