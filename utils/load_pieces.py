import cv2

def get_pieces():
    piece_templates = []
    template_size = (50, 50)  
    
    for color in ['b', 'w']:
        for piece_type in ['p', 'r', 'n', 'b', 'q', 'k']:
            template_path = f'./images/pieces/classic/{color}{piece_type}.png'
            template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
            template = cv2.resize(template, template_size)
            piece_templates.append(template)

    return piece_templates
