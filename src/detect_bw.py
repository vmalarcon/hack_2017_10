# import the necessary packages
from imutils import paths
import argparse
import cv2
from PIL import Image, ImageStat

def detect_color_image(file, thumb_size=40, MSE_cutoff=22, adjust_color_bias=True):
    pil_img = Image.open(file)
    bands = pil_img.getbands()
    if bands == ('R','G','B') or bands== ('R','G','B','A'):
        thumb = pil_img.resize((thumb_size,thumb_size))
        SSE, bias = 0, [0,0,0]
        if adjust_color_bias:
            bias = ImageStat.Stat(thumb).mean[:3]
            bias = [b - sum(bias)/3 for b in bias ]
        for pixel in thumb.getdata():
            mu = sum(pixel)/3
            SSE += sum((pixel[i] - mu - bias[i])*(pixel[i] - mu - bias[i]) for i in [0,1,2])
        MSE = float(SSE)/(thumb_size*thumb_size)
        print "( MSE=",MSE,")"
        if MSE <= MSE_cutoff:
            print "grayscale\t",
            return "Grayscale"
        else:
            print "Color\t\t\t",
            return "Color"
    elif len(bands)==1:
        print "Black and white", bands
        return "Black and white"
    else:
        print "Don't know...", bands
        return "???"
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True,
	help="path to input directory of images")
ap.add_argument("-t", "--threshold", type=float, default=100.0,
	help="focus measures that fall below this value will be considered 'blurry'")
args = vars(ap.parse_args())

# loop over the input images
for imagePath in paths.list_images(args["images"]):
    color_result = detect_color_image(imagePath)	
        
    image = cv2.imread(imagePath) 
    cv2.putText(image, "Detect B/W: {}".format(color_result), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
    cv2.imshow("Image", image)
    key = cv2.waitKey(0)
