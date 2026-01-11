# messaging/urls.py
from django.urls import path
from . import views

app_name = "messaging"

urlpatterns = [
    path("start/<str:username>/", views.start_conversation, name="start"),
    path("<int:pk>/", views.conversation_detail, name="conversation_detail"),
    path("", views.inbox, name="inbox"),
    
    # acciones
    path("<int:pk>/archive/", views.archive_conversation, name="archive"),
    path("<int:pk>/delete/", views.delete_conversation, name="delete"),
    path("archived/", views.archived_inbox, name="archived_inbox"),
    path("<int:pk>/unarchive/", views.unarchive_conversation, name="unarchive_conversation"),



]
