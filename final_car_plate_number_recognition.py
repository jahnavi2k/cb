# -- coding: utf-8 --
"""FINAL CAR PLATE NUMBER RECOGNITION

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dWyreN1962LUNGVNbHY4Be1LbbtKwVa_

# Car plate number Recognition Model
"""

# !nvcc --version ## 3 7 10 11 13 14 17 22 23 24 32 33 41

# !pip install easyocr
# !pip install imutils
# !pip install opencv-python-headless==4.1.2.30
# !pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113

import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr
# import main
# from main import *
import os
import streamlit as st
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# preprocessing
img = cv2.imread(
    r'C:/Users/jahna/Dropbox/My PC (DESKTOP-UKVOUSD)/Desktop/cb/carplatenumber3.jpg')
# due red green blue, pixel increase so that is why convert to gray

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))  # savetime

"""*Apply Filters and edge detection*"""

bfilter = cv2.bilateralFilter(gray, 11, 17, 17)  # noise reduced
edged = cv2.Canny(bfilter, 30, 200)  # DETECT EDGE
# plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))
# when we converted color->gray a lot of data/pixels got reduced due to which the analysis took less time
# now that we have used bfliter so that more time is reduced

"""*Find contours and apply mask*"""

# contours stroes polygons in a pic seperatly we can easily detect no. plate
keypoints = cv2.findContours(
    edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(keypoints)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
# the sorting in descending order so that better shapes come first
# chain_approx line is used to simplofy the data ie if we dont use it then even pixels of line would get stored but we need proper polygons

location = None
for contour in contours:
    # how many approx values if we increase value the result would be more rough accordingly
    approx = cv2.approxPolyDP(contour, 10, True)
    if len(approx) == 4:
        location = approx
        break

location

# will finally mask
mask = np.zeros(gray.shape, np.uint8)
new_image = cv2.drawContours(mask, [location], 0, 255, -1)
new_image = cv2.bitwise_and(img, img, mask=mask)

# plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))

(x, y) = np.where(mask == 255)
(x1, y1) = (np.min(x), np.min(y))
(x2, y2) = (np.max(x), np.max(y))
cropped_image = gray[x1:x2+1, y1:y2+1]

# plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))

"""*Easy OCR use*"""

reader = easyocr.Reader(['en'])  # english
result = reader.readtext(cropped_image)
result

"""*Plot the Model*"""

# if (len(result) == 1):
#     text = result[0][-2]
# else:
#     text = result[1][-2]
# print(text)

if (len(result) == 1):
    text = result[0][-2]
else:
    text = result[1][-2]
# text = result[0][-2]
st.write(text)
font = cv2.FONT_HERSHEY_SIMPLEX
# res=cv2.putText(img,text=text, org=(approx[0][0][0], approx[1][0][1]+60), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=1)
res = cv2.rectangle(img, tuple(approx[0][0]), tuple(
    approx[2][0]), (0, 255, 0), 3)
img = cv2.putText(img, text, tuple(
    approx[0][0]), font, 0.5, (0, 255, 0), 2, cv2.LINE_AA)
# plt.imshow(cv2.cvtColor(res, cv2.COLOR_BGR2RGB))
