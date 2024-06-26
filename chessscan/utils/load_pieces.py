import os
import cv2

# todo add piece type as args
def get_pieces(w, h, piece_material):
    piece_templates = []
    template_size = (w, h)  

    for color in ['b', 'w']:
        for piece_type in ['p', 'r', 'n', 'b', 'q', 'k']:
            template_path = os.path.join(f'images/pieces/{piece_material}/', f'{color}{piece_type}.png')
            template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
            template = cv2.resize(template, template_size)
            piece_templates.append(template)

    return piece_templates