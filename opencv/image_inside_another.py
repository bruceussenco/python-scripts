import cv2 as cv
import numpy

img1 = cv.imread("images/1.png")
img2 = cv.imread("images/cropped_1.png")

img1_gray = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
img2_gray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)

res = cv.matchTemplate(img1_gray, img2_gray, cv.TM_CCOEFF_NORMED)
if numpy.any(res > 0.9):
    print("Image2 is in Image1.")
