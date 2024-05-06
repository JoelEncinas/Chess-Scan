import os, base64

from django.shortcuts import render
from django.http import JsonResponse
from chessscan.utils.process_image import process_image

# Create your views here.

def index(request):    
    return render(request, 'chessscan/index.html', {})

def about(request):    
    return render(request, 'chessscan/about.html', {})

def upload_image(request):
    image_path = os.path.join('images/positions', 'test-2.PNG')

    # Your backend logic goes here
    # For example, let's say you want to return some JSON data
    image_data, fen = process_image(image_path)

    print(image_data)

    data = {
        'message': 'Backend stuff executed successfully',
        'image': image_data,
        'fen': fen
    }
    
    return JsonResponse(data)