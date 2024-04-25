import cv2

image = cv2.imread('./images/positions/test-2.png')
template = cv2.imread('./images/pieces/classic/wq.png')

image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
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

roi = image_gray[y:(y + h), x:(x + w)]
resized_roi = cv2.resize(roi, (400, 400))
resized_template = cv2.resize(template_gray, (50, 50))

# template matching
res = cv2.matchTemplate(resized_roi, resized_template, cv2.TM_CCOEFF)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

x1, y1 = max_loc
x2, y2 = max_loc[0] + resized_template.shape[1], max_loc[1] + resized_template.shape[0]

cv2.rectangle(resized_roi, (x1, y1), (x2, y2), (0, 255, 0), 3)

cv2.imshow("Chess", resized_roi)
cv2.waitKey(0)
cv2.destroyAllWindows()