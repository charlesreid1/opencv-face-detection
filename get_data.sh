#!/bin/bash

# Target face image
mkdir images/
cd images/
wget -O bush.jpeg https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/George-W-Bush.jpeg/580px-George-W-Bush.jpeg
cd ../

# Haar face detection parameters
wget https://raw.githubusercontent.com/opencv/opencv/2.4/data/haarcascades/haarcascade_frontalface_default.xml
wget https://raw.githubusercontent.com/opencv/opencv/2.4/data/haarcascades/haarcascade_frontalface_alt.xml
wget https://raw.githubusercontent.com/opencv/opencv/2.4/data/haarcascades/haarcascade_frontalface_alt2.xml

# Haar eye detection parameters
wget https://raw.githubusercontent.com/opencv/opencv/2.4/data/haarcascades/haarcascade_eye.xml
https://raw.githubusercontent.com/opencv/opencv/2.4/data/haarcascades/haarcascade_righteye_2splits.xml
https://raw.githubusercontent.com/opencv/opencv/2.4/data/haarcascades/haarcascade_lefteye_2splits.xml
https://raw.githubusercontent.com/opencv/opencv/2.4/data/haarcascades/haarcascade_mcs_righteye.xml
https://raw.githubusercontent.com/opencv/opencv/2.4/data/haarcascades/haarcascade_mcs_lefteye.xml

# These two are different
# wget https://raw.githubusercontent.com/opencv/opencv/2.4/data/haarcascades/haarcascade_mcs_eyepair_big.xml
# This one works better (I think?):
wget https://raw.githubusercontent.com/opencv/opencv_contrib/master/modules/face/data/cascades/haarcascade_mcs_eyepair_big.xml

