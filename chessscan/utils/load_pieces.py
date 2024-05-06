import os
import cv2
from django.templatetags.static import static

# todo add piece type as args
def get_pieces(w, h):
    piece_templates = []
    template_size = (w, h)  

    for color in ['b', 'w']:
        for piece_type in ['p', 'r', 'n', 'b', 'q', 'k']:
            template_path = os.path.join('images/pieces/classic/', f'{color}{piece_type}.png')
            print(template_path)
            template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
            template = cv2.resize(template, template_size)
            piece_templates.append(template)

    return piece_templates