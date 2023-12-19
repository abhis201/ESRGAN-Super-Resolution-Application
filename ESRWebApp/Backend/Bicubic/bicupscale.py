import os
import cv2

def bicupscale(pathlr,pathsr):
	lrpath = os.listdir(pathlr)
	for index,imagename in enumerate(lrpath):
		img = cv2.imread(os.path.join(pathlr,imagename))
		img_resized = cv2.resize(img,(128,128), fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
		cv2.imwrite(os.path.join(pathsr,imagename),img_resized)

