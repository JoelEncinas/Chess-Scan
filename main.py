import cv2
import numpy as np

# Load the chessboard image
image = cv2.imread('./images/image1.JPG')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Preprocess the image
gray = cv2.GaussianBlur(gray, (5, 5), 0)
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter contours to find the largest square-like contour
def filter_contours(contours):
    square_contours = []
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        if len(approx) == 4:  # Check if contour is approximately square
            square_contours.append(contour)
    return square_contours

filtered_contours = filter_contours(contours)
largest_contour = max(filtered_contours, key=cv2.contourArea)

# Draw the bounding box around the chessboard
x, y, w, h = cv2.boundingRect(largest_contour)
cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Display the image with bounding box
cv2.imshow('Chessboard', image)
cv2.waitKey(0)
cv2.destroyAllWindows()