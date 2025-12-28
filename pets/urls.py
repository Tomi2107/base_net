# pets/urls.py
from django.urls import path
from . import views

app_name = 'pets'

urlpatterns = [
    path('lost/<int:pet_id>/', views.mark_pet_lost, name='pet-lost'),
    path('normal/<int:pet_id>/', views.mark_pet_normal, name='pet-normal'),
]
