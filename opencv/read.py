import cv2 as cv

# reading images
#img = cv.imread("images/1.png")
#cv.imshow("read image", img)

# reading videos
capture = cv.VideoCapture("videos/1.mp4")

while True:
    isTrue, frame = capture.read()
    cv.imshow("read video", frame)

    if cv.waitKey(20) & 0xFF==ord('d'):
        break

capture.release()
cv.destroyAllWindows()

cv.waitKey(0)

