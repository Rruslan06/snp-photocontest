from django.urls import path

# Импорты фоток
from api.views.photo.list import PhotoListAPIView
from api.views.photo.create import PhotoCreateAPIView
from api.views.photo.detail import PhotoDetailAPIView
from api.views.photo.my_photos import ProfilePhotoListAPIView
from api.views.vote.views import VoteAPIView

# Импорты комментов
from api.views.comment.views import CommentApiView
from api.views.comment.detail import CommentDetailAPIView 

from api.views.photo.restore import PhotoRestoreAPIView
from api.views.auth.register import RegisterAPIView


app_name = "api"

urlpatterns = [

    path('register/', RegisterAPIView.as_view(), name='api_register'),

    # Фото
    path('photos/', PhotoListAPIView.as_view(), name='api_photos_list'),
    path('photos/create/', PhotoCreateAPIView.as_view(), name='api_photos_create'),

        # Обновление/удаление/показ
    path('photos/<int:photo_id>/', PhotoDetailAPIView.as_view(), name='api_photo_detail'),

    # Профиль
    path('profile/photos/', ProfilePhotoListAPIView.as_view(), name='api_profile_photos'),

    # Лайки и Комменты к фотке
    path('photos/<int:photo_id>/comments/', CommentApiView.as_view(), name='api_photo_comments'),
    path('photos/<int:photo_id>/vote/', VoteAPIView.as_view(), name='api_photo_vote'),
    

    # Комментарии(обновление/удаление)
    path('comments/<int:comment_id>/', CommentDetailAPIView.as_view(), name='api_comment_detail'),

    
    path('photos/<int:photo_id>/restore/', PhotoRestoreAPIView.as_view(), name='api_photo_restore'),    
]


