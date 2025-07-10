import cv2 as cv

video_name = "1"
cap = cv.VideoCapture(f"videos/{video_name}.mp4")

fps = cap.get(cv.CAP_PROP_FPS)
w = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
center = (w//2, h//2)

fourcc = cv.VideoWriter_fourcc(*'MP4V')
out = cv.VideoWriter(f"videos/edited_{video_name}.mp4", fourcc, fps, (w, h))

while True:
    ret, frame = cap.read()

    if not ret: break

    cv.circle(frame, center, 40, (127, 0, 0), 3)
    cv.putText(frame, "edited", center, cv.FONT_HERSHEY_TRIPLEX, 1.0, (255, 0, 0), 2)

    out.write(frame)
    cv.imshow("edited video", frame)

    if cv.waitKey(20) & 0xFF==ord('q'): break

cap.release()
out.release()
cv.destroyAllWindows()

cv.waitKey(0)
