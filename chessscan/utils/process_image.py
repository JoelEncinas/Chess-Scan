import cv2, base64
import numpy as np
from chessscan.utils.load_pieces import get_pieces
from chessscan.utils.piece_types import get_piece_types
from chessscan.utils.filter_contours import filter_contours
from chessscan.utils.board_to_fen import board_to_fen

square_size = 50
board_size = 400
threshold = 0.99
empty_square_max_match_score = 8666666.0
board = [['empty' for _ in range(8)] for _ in range(8)]
piece_types = get_piece_types()

def process_image(uploaded_file, piece_material):
    nparr = np.fromstring(uploaded_file.read(), np.uint8)
    image_gray = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

    _, thresh = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    filtered_contours = filter_contours(contours)

    if not filtered_contours:  
        return None, None  

    template_pieces = get_pieces(50, 50, piece_material)

    largest_contour = max(filtered_contours, key=cv2.contourArea)

    x, y, w, h = cv2.boundingRect(largest_contour)

    roi = image_gray[y:(y + h), x:(x + w)]
    resized_roi = cv2.resize(roi, (board_size, board_size))

    for row in range(0, resized_roi.shape[0], square_size):
        for col in range(0, resized_roi.shape[1], square_size):
            roi = resized_roi[row:row+square_size, col:col+square_size]

            max_match_score = -1

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

    fen = board_to_fen(board)
    _, im_arr = cv2.imencode('.jpg', resized_roi)
    im_bytes = im_arr.tobytes()
    im_b64 = base64.b64encode(im_bytes).decode('utf-8')

    return im_b64, fen
