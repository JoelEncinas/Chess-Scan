from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('upload_image/', views.upload_image, name='upload_image'),
]
