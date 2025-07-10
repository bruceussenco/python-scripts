import cv2 as cv

capture = cv.VideoCapture("videos/1.mp4")

while True:
    ret, frame = capture.read()

    if not ret: break

    w = frame.shape[1]
    h = frame.shape[0]
    center = (w//2, h//2)
    cv.circle(frame, center, 40, (127, 0, 0), 3)
    cv.rectangle(frame, (0, 0), (w-1, h-1), (0,255,0), thickness=4)
    frame[center[1]:center[1]+20, w//8:w//4] = 0, 0, 255
    cv.line(frame, (0, h-1), (w-1, 0), (0,255,255), 2)
    cv.imshow("edited video", frame)

    if cv.waitKey(20) & 0xFF==ord('q'): break

capture.release()
cv.destroyAllWindows()

cv.waitKey(0)
