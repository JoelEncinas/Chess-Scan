import json

from django.shortcuts import render
from django.http import JsonResponse
from chessscan.utils.process_image import process_image
from chessscan.utils.get_url_from_position import get_url_from_position

def index(request):    
    return render(request, 'chessscan/index.html', {})

def about(request):    
    return render(request, 'chessscan/about.html', {})

def upload_image(request):
    if request.method == 'POST':
        uploaded_file = ''
        piece_material = ''

        if 'image' not in request.FILES:
            return JsonResponse({'error': 'No image uploaded'}, status=400)
        
        else:
            uploaded_file = request.FILES['image']

        piece_material = request.POST['piece_material']
        image_data, fen = process_image(uploaded_file, piece_material)

        if image_data == None and fen == None:
            return JsonResponse({'error': 'No chessboard detected'}, status=418)

        data = {
            'image': image_data,
            'fen': fen,
            'lichess': get_url_from_position(fen),
            'piece_material': piece_material
        }
        
        return JsonResponse(data)
    
    return JsonResponse({'error': 'No file uploaded'}, status=400)