# OpenCV Face Detection

This repository contains utility scripts for doing facial detection in images using OpenCV.

Most of these scripts are experiments. The goal is to incorporate these scripts
into scripts for a Raspberry Pi facial detection device - see the [pi-opencv](https://github.com/charlesreid1-raspberry-pi/pi-opencv) 
repository.

## Repository Organization

Completed tasks:
* <s>Take a photo using a webcam</s>
* <s>Basic face-finding code</s>

In-progress tasks:
* Find a face in a photograph (using test images from internet)
* Find a face in a webcam photograph (using webcam photos)
* Find eyes in a photograph (using test images from internet)
* Find eyes in a webcam photograph (using webcam photos)
* Find a face that may be rotated up to N degrees (using webcam)
* Detect sideways faces using eyes angle

## Take a Photo Using Webcam

**STATUS: DONE**

`take_photo.py`
* Imports OpenCV
* Captures an image from the specified camera device
* Transposes the image (rotate right)
* Saves the images to a file
* Uses imshow to show the images on screen
* (Future work) image is a numpy array, so do further processing/exports

## Basic Facial Recognition

**STATUS: DONE**

`basic_face_detection.py`
* Illustrates facial detection in the simplest script possible
* Cascade classifier is sensitive to parameter choices
* Does not generalize

**Expected output:**

<img src="images/output_basic_face_detection.jpg" width="300px"/>

## Find a Face

**STATUS: DONE**

`find_face_image.py`
* More generalized face-finding script
* Opens an image on disk using OpenCV or Pillow
* Create cascade classifier to find faces
* Get rectangles containing faces
* Draw rectangles around faces
* Get rectangles containing eyes
* Draw rectangles around eyes
* Show the image of the face with rectangles

This script works on a photograph of Pres. Obama, Pres. Bush, and 
two facial images taken by the webcam that will be used with the 
final Raspberry Pi setup (one low-res, one high-res).

## Find Face in Webcam Photograph

`webcam_face.py`
* Stream images from a webcam continuously
* Search for faces
* If faces detected, output detected faces and bounding boxes to image

## Find Rotated Face

Notes:
* https://stackoverflow.com/questions/5015124/rotated-face-detection#15997139

## Detect 



## Notes

Notes:
* It's easy to write a script that *usually* detects faces, or detects *one* eye, but 
    getting the task to work consistently, and always find a face and two eyes, is a pain.
* The process is extremely sensitive to the parameters used for the cascading classifier.
    Each different photo of a face requires different `scaleFactor` and `minNeighbors` settings
* Eyes are also difficult to detect without fiddling with settings that are specific to each image.
* [This](https://stackoverflow.com/questions/16128637/opencv-haarlike-eye-detection#16131846) SO question mentions an eye pair Haar cascade file.
* [opencv-contrib](https://github.com/opencv/opencv_contrib) repo has additional cascade .xml files
* See [opencv-contrib modules/face/data/cascades](https://github.com/opencv/opencv_contrib/tree/master/modules/face/data/cascades)


