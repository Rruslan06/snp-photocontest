from django.urls import path
from api import views

app_name = "api"

urlpatterns = [

    #http:127.0.0.1:8000/api/photos/
    path('photos/', views.PhotoListAPIView.as_view(), name='photo_list_api'),

    #http:127.0.0.1:8000/api/photos/ЧИСЛО/
    path('photos/<int:pk>', views.PhotoDetailAPIView.as_view(), name='photo_detail_api'),


    path('photos/<int:photo_id>/comments/', views.CommentApiView.as_view(), name='api_photo_comments'),

]