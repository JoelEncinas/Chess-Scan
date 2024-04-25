import cv2

def filter_contours(contours):
    square_contours = []
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        if len(approx) == 4:  
            square_contours.append(contour)
    return square_contours