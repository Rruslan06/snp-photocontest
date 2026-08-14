from django.urls import path
from api import views

from api.views import PhotoDetailAPIView, CommentApiView, ShowPhotoView, PhotoListAPIView, VoteAPIView


app_name = "api"

urlpatterns = [

    #http:127.0.0.1:8000/api/photos/
    path('photos/', PhotoListAPIView.as_view(), name='photo_list_api'),

    #http:127.0.0.1:8000/api/photos/ЧИСЛО/
    path('photos/<int:id>/', ShowPhotoView.as_view()),


    path('photos/<int:photo_id>/comments/', CommentApiView.as_view(), name='api_photo_comments'),

    path('photos/<int:photo_id>/vote/', VoteAPIView.as_view(), name='api_photo_vote'),

]