import numpy as np
import cv2
import time

"""
Take A Photo

This script uses OpenCV to take a picture
from a webcam or USB camera device.
"""

def take_photo(camera_port=0):
    """
    Captures an image from a web camera using OpenCV
    """
    camera = cv2.VideoCapture(camera_port)

    print("Say cheese")
    time.sleep(3)
    
    # Wait, otherwise the image will be over-dark
    time.sleep(0.3)
    return_value, image = camera.read()

    # Make sure you show the image 
    # before the camera is deleted,
    # otherwise you will get a segfault
    imageT = transpose_photo(image)
    show_image('cam', image)
    show_image('camT', imageT)

    print("Done")
    del(camera)

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

def show_image(windowname, image):
    """
    Show the image in a new window using OpenCV imshow
    """
    # Make the window resizable
    cv2.namedWindow('cam', cv2.WINDOW_NORMAL)
    cv2.imshow('cam',image)
    cv2.waitKey()

if __name__=="__main__":

    # Take
    img = take_photo(1)
    imgT = transpose_photo(img)

    # Save
    save_image("opencv.png", img)
    save_image("opencvT.png", imgT)


