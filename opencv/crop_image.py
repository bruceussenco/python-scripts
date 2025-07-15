import cv2 as cv

img = cv.imread("images/1.png")
xb, yb, xe, ye = 200, 200, 500, 500
cropped_img = img[yb:ye, xb:xe]

cv.imshow("original", img)
cv.imshow("cropped", cropped_img)
cv.waitKey(0)
cv.destroyAllWindows()
