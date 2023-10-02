from django.urls import path
from .views import UserListView, CreateUserView, CreateIOUView

urlpatterns = [
    path('users/', UserListView.as_view()),
    path('add/', CreateUserView.as_view()),
    path('iou/', CreateIOUView.as_view())
]
