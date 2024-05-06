from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def index(request):    
    return render(request, 'chessscan/index.html', {})

def about(request):    
    return render(request, 'chessscan/about.html', {})

def upload_image(request):
    # Your backend logic goes here
    # For example, let's say you want to return some JSON data
    data = {'message': 'Backend stuff executed successfully'}
    return JsonResponse(data)