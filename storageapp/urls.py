"""
URLs for storageapp
"""
from django.urls import path
from storageapp import views

urlpatterns = [
    path('presign-put/', views.presign_put_url, name='presign-put'),
]
