# pets/urls.py
from django.urls import path
from . import views

app_name = 'pets'

urlpatterns = [
    path('lost/<int:pet_id>/', views.mark_pet_lost, name='pet-lost'),
    path('normal/<int:pet_id>/', views.mark_pet_normal, name='pet-normal'), 
    path("pets/<int:pk>/edit/", views.edit_pet, name="edit-pet"),
    path("pets/<int:pk>/delete/", views.delete_pet, name="delete-pet"),
    path('dating/<int:pet_id>/', views.mark_pet_dating, name='pet-dating'),

]