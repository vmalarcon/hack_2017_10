from imutils import paths
import cv2
import numpy as np
import argparse

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True,
	help="path to input directory of images")
ap.add_argument("-t", "--threshold", type=float, default=100.0,
	help="focus measures that fall below this value will be considered 'blurry'")
args = vars(ap.parse_args())

# loop over the input images
for imagePath in paths.list_images(args["images"]):
    image = cv2.imread(imagePath)

    cv2.imshow('uncropped_image', image)
    cv2.waitKey()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray,50,250,0)
    im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(gray, contours, -1, (0,255,0), 3)

    area = 0
    x=0
    y=0
    h=0
    w=0
    bigCnt=0
    for cont in contours:
        x1, y1, w1, h1 = cv2.boundingRect(cont)
        areaTmp = (x1+w1) * (y1 + h1)
        if areaTmp > area:
            area = areaTmp
            x=x1
            y=y1
            h=h1
            w=w1
            bigCnt=cont
    
    crop = image[y:y+h,x:x+w]

    cv2.imshow('cropped_result', crop)
    cv2.waitKey()
