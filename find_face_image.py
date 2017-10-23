import time
import cv2
import cv2.cv as cv
import numpy as np
from PIL import Image

"""
Find a face in an image using OpenCV.

Basic workflow:
    * Use Haar facial detection algorithm to find faces
    * For each face, use Haar eye detection algorithm to find eyes
    * Draw the picture and draw bounding boxes around faces and eyes
"""

def jpeg_to_np(filename):
    """
    Loads jpeg image using Pillow,
    converts to a 3D Numpy array
    with shape (width, height, channels)
    """
    with Image.open(filename) as image:
        nparr = np.fromstring(image.tobytes(), dtype=np.uint8)
        nparr = im_arr.reshape((image.size[1], image.size[0], 3))
    return nparr 

def jpeg_to_np2(filename):
    """
    Loads jpeg image as a Numpy array
    using OpenCV
    """
    img = cv2.imread(filename)
    return img

def draw_rects(img, rects, color):
    """
    Use OpenCV to draw rectangles 
    on top of image
    """
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

def detect(img, cascade):
    """
    Given an image and a cascade object,
    detect features.
    """
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
    # rects contains (x,y),(w,h), return (x,y),(x+w,x+h)
    rects[:,2:] += rects[:,:2]
    return rects

if __name__=="__main__":
    filename = "face.jpeg"
    image = jpeg_to_np2(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    nested = cv2.CascadeClassifier("haarcascade_eye.xml")

    # Get rectangle for entire face
    rects = detect(gray, cascade)
    print("Number of faces: %d"%(len(rects)))

    # Draw face rectangles
    vis = image.copy()
    draw_rects(vis, rects, (0,255,0))

    subrects = detect(gray, nested)
    draw_rects(vis, subrects, (255, 0, 0))

    ### for i, (x1, y1, x2, y2) in enumerate(rects):
    ###     # Crop to just this face
    ###     grayeye = gray[y1:y2, x1:x2]
    ###     viseye  = vis[y1:y2,  x1:x2]
    ###     cv2.imshow('duh',viseye)
    ###     cv2.waitKey()

    ###     # Get rectangle for eye
    ###     subrects = detect(grayeye.copy(), nested)

    ###     print(subrects)

    ###     draw_rects(viseye, subrects, (255, 0, 0))
    ###     print("    Number of eyes in rectangle %d: %d"%(i+1,len(subrects)))

    cv2.imshow('facedetect', vis)
    cv2.waitKey()


