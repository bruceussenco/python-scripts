import cv2 as cv
import numpy

blank = numpy.zeros((360, 640, 3), dtype="uint8")
blank_center = (blank.shape[1]//2, blank.shape[0]//2)
cv.imshow("blank", blank)

# fill image
# blank[:] = 255, 255, 255
# blank[100:200, 200:300] = 255, 0, 0 # square
# cv.imshow("square", blank)

# draw rect
cv.rectangle(blank, (20, 20), (100, 40), (0,255,0), thickness=2)
cv.rectangle(blank, (100, 200), (120, 220), (0,255,0), thickness=cv.FILLED)

# draw circle
cv.circle(blank, blank_center, 40, (127, 127, 0))

# draw line
cv.line(blank, (20, 20), (300, 250), (0, 0, 255), thickness=3)

# write text
cv.putText(blank, "text writing", (100, 100), cv.FONT_HERSHEY_TRIPLEX, 1.0, (255, 0, 0), 2)

cv.imshow("drawing", blank)


cv.waitKey(0)

