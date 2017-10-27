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

def main():
    
    face_settings = {
            'scaleFactor'   : 1.3,
            'minNeighbors'  : 1,
            'minSize'       : (5,5),
            'flags'         :  cv2.cv.CV_HAAR_SCALE_IMAGE|cv2.cv.CV_HAAR_DO_ROUGH_SEARCH
    }
    
    eye_settings = {
            'scaleFactor'   : 1.3,
            'minNeighbors'  : 3,
            'minSize'       : (5,5),
            'flags'         :  cv2.cv.CV_HAAR_SCALE_IMAGE
    }

    # Other flags: 
    # cv2.cv.CV_HAAR_SCALE_IMAGE
    # cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT
    # cv2.cv.CV_HAAR_DO_ROUGH_SEARCH



    ## Obama - works
    #IMAGE_FILE                    = "images/obama.jpg"
    #face_settings['scaleFactor']  = 1.3
    #face_settings['minNeighbors'] = 1
    #eye_settings['scaleFactor']   = 1.3
    #eye_settings['minNeighbors']  = 3
    
    # GWBush - works
    IMAGE_FILE                    = "images/bush.jpg"
    face_settings['scaleFactor']  = 1.3
    face_settings['minNeighbors'] = 1
    eye_settings['scaleFactor']   = 1.3
    eye_settings['minNeighbors']  = 3
    
    ## Me - works
    #IMAGE_FILE                    = "images/me.jpg"
    #face_settings['scaleFactor']  = 1.3
    #face_settings['minNeighbors'] = 1
    #eye_settings['scaleFactor']   = 1.3
    #eye_settings['minNeighbors']  = 3
    
    ## Me too - works
    #IMAGE_FILE                    = "images/opencvT.png"
    #face_settings['scaleFactor']  = 1.3
    #face_settings['minNeighbors'] = 1
    #eye_settings['scaleFactor']   = 1.3
    #eye_settings['minNeighbors']  = 3
    
    draw_face_boxes(IMAGE_FILE, face_settings, eye_settings)



def draw_face_boxes(filename, face_settings, eye_settings):

    image = img2np_opencv(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    face_classifier  = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
    #eye_classifier   = cv2.CascadeClassifier("haarcascade_eye.xml")
    eye_classifier   = cv2.CascadeClassifier("haarcascade_mcs_eyepair_big.xml")
    left_classifier  = cv2.CascadeClassifier("haarcascade_lefteye_2splits.xml")
    right_classifier = cv2.CascadeClassifier("haarcascade_righteye_2splits.xml")

    # --------
    # FACES:

    # Get rectangle for entire face
    print("From faces:")
    rects = detect(gray, face_classifier, face_settings)

    # Draw face rectangles
    vis = image.copy()
    draw_rects(vis, rects, (255, 0, 0))

    # --------
    # EYES:

    # Look for eyes in each face rectangle
    for i, (x1, y1, x2, y2) in enumerate(rects):
        # Crop to just this face
        grayface = gray[y1:y2, x1:x2]
        visface  = vis[y1:y2,  x1:x2]

        # Get rectangle for eye
        print("From inside:")

        #subrects  = detect(grayface,   eye_classifier, eye_settings)
        subrects  = detect(grayface,   eye_classifier, {})#, eye_settings)
        draw_rects(visface, subrects, (50,50,255))

        #subrectsL = detect(grayface,  left_classifier, eye_settings)
        #subrectsR = detect(grayface, right_classifier, eye_settings)

        #draw_rects(visface, subrectsL, (100, 100, 255))
        #draw_rects(visface, subrectsR, (100, 255, 100))


    cv2.imwrite("detected_faces.png", vis)
    #cv2.imshow('facedetect', vis)
    #cv2.waitKey()



def detect(img, cascade, settings):
    """
    Given an image and a cascade object,
    detect features.
    """
    # Parameters taken verbatim from OpenCV 2.4 example:
    # https://github.com/opencv/opencv/blob/2.4/samples/python2/facedetect.py
    rects = cascade.detectMultiScale(img, 
                        **settings)

    if len(rects) == 0:
        return []

    print(rects)

    # Turn width and height of box
    # into plot-ready image coordinates.
    # rects contains (x,y),(w,h), return (x,y),(x+w,x+h)

    rects[:,2:] += rects[:,:2]
    return rects



def img2np_pillow(filename):
    """
    Load an image using Pillow 
    and convert it to a 3D Numpy array
    with shape (W, H, 3)
    """
    with Image.open(filename) as image:
        nparr = np.fromstring(image.tobytes(), dtype=np.uint8)
        nparr = im_arr.reshape((image.size[1], image.size[0], 3))
    return nparr 

def img2np_opencv(filename):
    """
    Load an image using OpenCV
    and convert it to a 3D Numpy array
    with shape (W, H, 3)
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

if __name__=="__main__":
    main()

