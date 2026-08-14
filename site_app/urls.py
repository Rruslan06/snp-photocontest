
from django.urls import path

from site_app import views

app_name = "site_app" #Пространство имен ссылок, чтобы потом использовать в связке с name и не хардкордить шаблоны

urlpatterns = [
    #http:127.0.0.1:8000/
    path('', views.PhotoListView.as_view(), name='master_page'),

    #http:127.0.0.1:8000/photo/номер PK
    path('photo/<int:pk>/', views.PhotoDetailView.as_view(), name='detail_page'),

    #http:127.0.0.1:8000/profile/
    path('profile/', views.UserProfileView.as_view(), name='profile'),

    #http:127.0.0.1:8000/upload/
    path('upload/', views.PhotoCreateView.as_view(), name='photo_upload'),

    #http:127.0.0.1:8000/photo/номер PK/comment
    path('/<int:pk>/comment/', views.AddCommentView.as_view(), name="add_comment"),

    #http:127.0.0.1:8000/photo/номер PK/comment
    path('comment/<int:pk>/delete/', views.DeleteCommentView.as_view(), name='delete_comment'),

    #http:127.0.0.1:8000/photo/номер PK/vote
    path('photo/<int:pk>/vote/', views.ToggleVoteView.as_view(), name="toggle_vote"),


    path('photo/<int:pk>/edit', views.PhotoUpdateView.as_view(), name="edit_photo"),

]
