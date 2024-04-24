import cv2
import numpy as np

image = cv2.imread('./images/positions/test-1.JPG')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

def filter_contours(contours):
    square_contours = []
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        if len(approx) == 4:  
            square_contours.append(contour)
    return square_contours

filtered_contours = filter_contours(contours)
largest_contour = max(filtered_contours, key=cv2.contourArea)

x, y, w, h = cv2.boundingRect(largest_contour)
cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow("Chess", image)
# cv2.imshow("Chess gray", gray)
cv2.waitKey(0)
cv2.destroyAllWindows()