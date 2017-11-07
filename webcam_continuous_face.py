import time
from datetime import datetime
import json
import subprocess
import cv2
import cv2.cv as cv
import numpy as np
from PIL import Image

"""
Take images from a webcam, 
look for faces.

All photos go into raw/
Photos with faces go into faces/

Basic workflow:
    * Take photo with webcam every N seconds
    * Put into raw/
    * Look for faces
    * If faces found, put into faces/
"""

def main():

    N = 3
    raw_dir = "raw/"
    faces_dir = "faces/"
    
    face_settings = {
            'scaleFactor'   : 1.3,
            'minNeighbors'  : 1,
            'minSize'       : (10,10),
            'flags'         :  cv2.cv.CV_HAAR_SCALE_IMAGE|cv2.cv.CV_HAAR_DO_ROUGH_SEARCH
    }
    
    # Other flags: 
    # cv2.cv.CV_HAAR_SCALE_IMAGE
    # cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT
    # cv2.cv.CV_HAAR_DO_ROUGH_SEARCH

    camera_port = 0
    camera = cv2.VideoCapture(camera_port)

    subprocess.call(["mkdir","-p",raw_dir])
    subprocess.call(["mkdir","-p",faces_dir])

    write_index(faces_dir, False)
    
    while(True):
        # Take photo every N seconds
        time.sleep(N)
        print("Photobomb!")
        img = take_photo(camera)
        
        # Create a timestamp on each image
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%m-%S")
        filename = "img_"+timestamp+".jpg"

        # Save image to raw/
        save_image(raw_dir+filename, img)

        # If faces, save image to faces/
        # (ideally, save location of faces to json file - not implemented)
        jsonfilename = "img_"+timestamp+".json"
        faces_were_found = save_faces(img, faces_dir+filename, faces_dir+jsonfilename, face_settings)

        # If we found faces, create symlink to latest face capture
        if(faces_were_found):
            subprocess.call(["ln", "-fs", filename, faces_dir+"last_face.jpg"])
            write_index(faces_dir, True)


def take_photo(camera):
    """
    Captures an image from a web camera using OpenCV
    """

    # Wait, otherwise the image will be over-dark
    time.sleep(0.3)
    return_value, image = camera.read()

    ### imageT = transpose_photo(image)

    return image

def transpose_photo(image):
    """
    Transposes the first two axes of an image (diagonal reflection)
    """
    imageT = np.transpose(image, axes=(1,0,2))
    return imageT

def save_image(filename, image):
    """
    Saves an image array to a file
    """
    cv2.imwrite(filename, image)

def save_faces(image, filename, jsonfilename, face_settings):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    face_classifier0    = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    face_classifier1    = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    face_classifier2    = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")

    # Get rectangle for entire face
    rects = detect(gray, face_classifier2, face_settings)

    if len(rects) != 0:
        # Found a face:
        # Draw face rectangles
        print("Found a face")
        vis = image.copy()
        draw_rects(vis, rects, (255, 0, 0))
        save_image(filename, vis)

        ## rects is a numpy array, not serializable
        # with open(jsonfilename,'a') as f:
        #     json.dumps({'boundaries':rects})

        return True
    else:
        return False

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

    # Turn width and height of box
    # into plot-ready image coordinates.
    # rects contains (x,y),(w,h), return (x,y),(x+w,x+h)

    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    """
    Use OpenCV to draw rectangles 
    on top of image
    """
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

def write_index(faces_dir, face_is_present):
    """Write an index file to display the last face present.
    If face_is_present is False, 
    no faces have been found yet, 
    so use an empty placeholder.
    """
    with open(faces_dir+"index.html", "w") as f:
        f.write("<html>")
        f.write("<body>")
        
        if(face_is_present):
            f.write('<img width="500px" src="last_face.jpg" />')
        else:
            f.write("<p>No faces found yet.</p>")

        f.write("</body>")
        f.write("</html>")



if __name__=="__main__":
    main()

