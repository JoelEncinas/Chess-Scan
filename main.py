import cv2
from utils.load_pieces import get_pieces

# url for pieces
# https://images.chesscomfiles.com/chess-themes/pieces/classic/150/wp.png

# template and image to match size
square_size = 50
board_size = 400

# load image to match
image_gray = cv2.imread('./images/positions/test-5.PNG', cv2.IMREAD_GRAYSCALE)

# load pieces
template_pieces = get_pieces()

# find chessboard
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
resized_roi = cv2.resize(roi, (board_size, board_size))

threshold = 0.8  # Threshold for template matching

# Piece types in the given order
piece_types = [
    'black pawn  ', 'black rook  ', 'black knight', 'black bishop', 'black queen ', 'black king  ',
    'white pawn  ', 'white rook  ', 'white knight', 'white bishop', 'white queen ', 'white king  ',
]

board = [['empty' for _ in range(8)] for _ in range(8)]

# Loop through each square of the chessboard
for row in range(0, resized_roi.shape[0], square_size):
    for col in range(0, resized_roi.shape[1], square_size):
        roi = resized_roi[row:row+square_size, col:col+square_size]  # Define ROI for current square

        # Initialize variables to keep track of the maximum match score and corresponding piece template
        max_match_score = -1
        best_piece_template = None

        # Loop through each template piece
        for template_index, template_piece in enumerate(template_pieces):
            # Perform template matching
            res = cv2.matchTemplate(roi, template_piece, cv2.TM_CCOEFF)
            _, max_val, _, _ = cv2.minMaxLoc(res)

            # If the match score is above threshold and higher than previous matches
            if max_val > threshold and max_val > max_match_score:
                max_match_score = max_val
                best_piece_template_index = template_index

        # If a piece template was found for the square
        if best_piece_template_index is not None:
            if best_piece_template_index == 8 and max_match_score < 8666666.0:
                matched_piece_type = 'empty square'
            else:
                # Get the corresponding piece type based on the index
                matched_piece_type = piece_types[best_piece_template_index]

            # save to board
            board[row // 50][ col // 50] = matched_piece_type

            # Print the matched piece type and draw a rectangle around it
            cv2.rectangle(resized_roi, (col, row), (col + square_size, row + square_size), (0, 255, 0), 3)

print("Chessboard")
for row in board:
    print(row)

# Display the chessboard image with rectangles drawn around matched pieces
cv2.imshow('Chessboard with matched pieces', resized_roi)
cv2.waitKey(0)
cv2.destroyAllWindows()