from django.urls import path
from . import views

app_name = 'friends'

urlpatterns = [
    path('', views.FriendsListView.as_view(), name='list'),
    path('requests/', views.FriendRequestsView.as_view(), name='requests'),
    path('send/<int:user_id>/', views.send_friend_request, name='send'),
    path('accept/<int:request_id>/', views.accept_request, name='accept'),
    path('reject/<int:request_id>/', views.reject_request, name='reject'),
    path("remove/<int:user_id>/", views.remove_friend, name="remove"), 


]
