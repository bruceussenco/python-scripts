import cv2 as cv
import numpy

path = "images/export.png"

img = numpy.zeros((360, 640, 3), dtype="uint8")
cv.rectangle(img, (20, 20), (100, 40), (0,255,0), thickness=2)

cv.imwrite(path, img)
