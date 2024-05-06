import os

from django.shortcuts import render
from django.http import JsonResponse
from chessscan.utils.process_image import process_image

# Create your views here.

def index(request):    
    return render(request, 'chessscan/index.html', {})

def about(request):    
    return render(request, 'chessscan/about.html', {})

def upload_image(request):
    image_path = os.path.join('images/positions', 'test-1.PNG')

    # Your backend logic goes here
    # For example, let's say you want to return some JSON data
    resized_roi, fen = process_image(image_path)
    data = {
        'message': 'Backend stuff executed successfully',
        'position': fen
    }

    
    return JsonResponse(data)