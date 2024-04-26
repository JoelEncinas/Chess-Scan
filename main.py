import cv2
from utils.load_pieces import get_pieces
from utils.piece_types import get_piece_types
from utils.filter_contours import filter_contours
from utils.board_to_fen import board_to_fen
from utils.get_url_from_position import get_url_from_position

# url for pieces
# https://images.chesscomfiles.com/chess-themes/pieces/classic/150/wp.png

# settings
square_size = 50
board_size = 400
threshold = 0.8 
empty_square_max_match_score = 8666666.0
board = [['empty' for _ in range(8)] for _ in range(8)]
template_pieces = get_pieces(50, 50)
piece_types = get_piece_types()


image_gray = cv2.imread('./images/positions/test-4.PNG', cv2.IMREAD_GRAYSCALE)

_, thresh = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

filtered_contours = filter_contours(contours)
largest_contour = max(filtered_contours, key=cv2.contourArea)

x, y, w, h = cv2.boundingRect(largest_contour)

roi = image_gray[y:(y + h), x:(x + w)]
resized_roi = cv2.resize(roi, (board_size, board_size))

for row in range(0, resized_roi.shape[0], square_size):
    for col in range(0, resized_roi.shape[1], square_size):
        roi = resized_roi[row:row+square_size, col:col+square_size]

        max_match_score = -1
        best_piece_template = None

        for template_index, template_piece in enumerate(template_pieces):
            res = cv2.matchTemplate(roi, template_piece, cv2.TM_CCOEFF)
            _, max_val, _, _ = cv2.minMaxLoc(res)

            if max_val > threshold and max_val > max_match_score:
                max_match_score = max_val
                best_piece_template_index = template_index

        if best_piece_template_index is not None:
            if best_piece_template_index == 8 and max_match_score < empty_square_max_match_score:
                matched_piece_type = '.'
            else:
                matched_piece_type = piece_types[best_piece_template_index]

            board[row // 50][ col // 50] = matched_piece_type

            cv2.rectangle(resized_roi, (col, row), (col + square_size, row + square_size), (0, 255, 0), 3)

# print("Chessboard")
for row in board:
    pass
    # print(row)

fen = board_to_fen(board)
# print(fen)

# print(get_url_from_position(fen))

# Display the chessboard image with rectangles drawn around matched pieces
cv2.imshow('Chessboard with matched pieces', resized_roi)
cv2.waitKey(0)
cv2.destroyAllWindows()